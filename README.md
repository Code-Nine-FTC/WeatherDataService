<!--
This file contains the README documentation for the recommendation-service project.
-->

Para rodar o serviço `devops-testes`, siga as instruções abaixo:

1. **Criar o ambiente virtual**:
    ```bash
    python -m venv .venv
    ```

2. **Ativar o ambiente virtual**:
    - No Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    - No macOS ou Linux:
        ```bash
        source .venv/bin/activate
        ```

3. **Instalar as dependências necessárias**:
    ```bash
    pip install -r requirements.txt
    ```
    Obs: Caso o projeto não reconheça as dependências instaladas, confira o interpretador Python:
    ```bash
    Ctrl + P e depois `> Python: Select Interpreter 3.12.5`
    ```

4. **Configurar o VSCode**:
    - Crie uma pasta `.vscode` na raiz do projeto.
    - Dentro da pasta `.vscode`, crie o arquivo `settings.json` e adicione:
    ```json
    {
        "terminal.integrated.env.windows": {
            "PYTHONPYCACHEPREFIX": "${workspaceFolder}/.pycache_global"
        },
        "terminal.integrated.env.linux": {
            "PYTHONPYCACHEPREFIX": "${workspaceFolder}/.pycache_global"
        },
        "terminal.integrated.env.osx": {
            "PYTHONPYCACHEPREFIX": "${workspaceFolder}/.pycache_global"
        }
    }
    ```
    - Dentro da pasta `.vscode`, crie o arquivo `launch.json` e adicione:
    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "FastAPI Debug",
                "type": "debugpy",
                "request": "launch",
                "module": "uvicorn",
                "args": [
                    "main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "5050",
                ],
                "env": {
                    "PYTHONPYCACHEPREFIX": "${workspaceFolder}/.pycache_global"
                },
                "console": "integratedTerminal"
            }
        ]
    }
    ```
5. **Iniciar o submódulo**:
    - Para inicializar o submódulo, execute o comando:

    ```bash
    git submodule update --init
    ```

    - Para atualizar o submódulo para a última versão, execute:

    ```bash
    git submodule update --remote
    ```

6. **Iniciando ruff e mypy**:
    ## Antes de cada commit, use os seguintes comandos:
    - Para rodar o `ruff` e corrigir os problemas encontrados, siga os passos abaixo:

        - Formate o código para o padrão configurado:
        ```bash
        ruff format .
        ```
        - Verifique se o código possui algum problema relatado:
        ```bash
        ruff check .
        ```
        caso possua:
        ```bash
        ruff check . --fix
        ```

        - Para rodar o `mypy` e corrigir problemas encontrados, siga os passos abaixo:
        ```bash
        mypy .
        ```
        Se aparecer problemas, você deve resolvê-los um a um.

7. **Instalando Docker**:
    - Siga as instruções para instalar o Docker no seu sistema operacional:
        - [Windows](https://docs.docker.com/desktop/install/windows-install/)
        - [Linux](https://docs.docker.com/desktop/install/linux-install/)
        - [Mac](https://docs.docker.com/desktop/install/mac-install/)

    - Rode o comando para criar o container:

    ```bash
    docker run -d --name api-tecsus \
       -e POSTGRES_USER=codenine \
       -e POSTGRES_PASSWORD=codenine2025 \
       -e POSTGRES_DB=tecsus \
       -p 5432:5432 \
        postgres:16
    ```
    - Após criado, modifique o arquivo `.env` colocando a URL do seu container:
        ```env
        DATABASE_URL=postgresql+asyncpg://codenine:codenine2025@localhost:5432/tecsus
        ```
    - Use o DBeaver para se conectar ao banco de dados.

8. **Configurando o Alembic**:
    - Inicie o Alembic: 
    ```bash
    alembic init alembic
    ```

    - Modifique o arquivo `alembic/env.py`:

    ```python
	from logging.config import fileConfig
	from alembic import context
	from sqlalchemy.ext.asyncio import create_async_engine
	from sqlalchemy.ext.asyncio import AsyncConnection
	from app.config.settings import settings
	from app.core.models.db_model import Base
	import asyncio
	from app.core.models.db_model import User
	from app.modules.security import PasswordManager
	from sqlalchemy.future import select


	config = context.config


	config.set_main_option("sqlalchemy.url", settings.DATABASE_URL if not settings.TEST_ENV else settings.DATABASE_URL_TEST)

	if config.config_file_name is not None:
		fileConfig(config.config_file_name)

	target_metadata = Base.metadata

	async def create_user(connection: AsyncConnection) -> None:
		result = await connection.execute(select(User).where(User.email == "admcodenine@gmail.com"))
		existing_user = result.scalar()

		if not existing_user:
			hashed_password = PasswordManager().password_hash("adm2025")
			await connection.execute(
				User.__table__.insert().values(
					email="admcodenine@gmail.com",
				password=hashed_password,
				name="Admin"
				)
			)
			await connection.commit()
			print("Usuário inicial criado com sucesso.")
		else:
			print("Usuário já existe.")

	def run_migrations_offline() -> None:
		url = config.get_main_option("sqlalchemy.url")
		context.configure(
			url=url,
			target_metadata=target_metadata,
			literal_binds=True,
			dialect_opts={"paramstyle": "named"},
		)

		with context.begin_transaction():
			context.run_migrations()

	async def run_async_migrations() -> None:
		try:
			connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

			async with connectable.connect() as connection:
				await connection.run_sync(do_run_migrations)
				try:
					await create_user(connection)
					print("User creation process completed.")
				except Exception as user_error:
					print(f"User creation error: {user_error}")
		except ConnectionRefusedError as e:
			print(f"Database connection refused: {e}")
			print("Please check if the database server is running and the connection details are correct.")
			raise
		except Exception as e:
			print(f"An error occurred while running migrations: {e}")
			raise

	def do_run_migrations(connection: AsyncConnection) -> None:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			compare_type=True,
			compare_server_default=True,
		)

		with context.begin_transaction():
			context.run_migrations()

	def run_migrations_online() -> None:
		asyncio.run(run_async_migrations())

	if context.is_offline_mode():
		run_migrations_offline()
	else:
		run_migrations_online()
    ```

    - Gerar revisão do banco de dados:
    ```bash
        alembic revision --autogenerate -m "frase de exemplo"
    ```
    
    - Rodar as migrações do banco de dados:
    ```bash
        alembic upgrade head
    ```

9. **Rodar a aplicação**:
    - Para rodar a aplicação:
    ```bash
    python -m main
    ```
    ou
    ```bash
    uvicorn main:app --reload --port 5000
    ```
    - Para rodar com o modo debugger, basta apertar `F5` no VSCode.

10. **Executar o Ambiente de Testes**
    - Para iniciar o ambiente de testes, utilize:
    ```bash
    docker compose up
    ```
    - Para rodar os testes automatizados:
    ```bash
    pytest
    ```
    - Para rodar os testes com relatório de cobertura:
    ```bash
    task test 
    ```
    ou 
    ```bash
    pytest --cov 
    ```

