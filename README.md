<!--
This file contains the README documentation for the recommendation-service project.
-->

Para rodar o serviço `WealtherDataService`, siga as instruções abaixo:

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
    Ctrl + P e depois > Python: Select Interpreter
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
                    "app.main:app",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "5060",
                    "--reload"
                ],
                "env": {
                    "PYTHONPYCACHEPREFIX": "${workspaceFolder}/.pycache_global"
                },
                "console": "integratedTerminal"
            }
        ]
    }
    ```

5. **Rodar a aplicação**:
    - Para rodar a aplicação:
    ```bash
    python -m app.main
    ```
    ou
    ```bash
    uvicorn app.main:app --reload --port 5000
    ```

    - Para rodar com o modo debugger, basta apertar `F5` no VSCode.

