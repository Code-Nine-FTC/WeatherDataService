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