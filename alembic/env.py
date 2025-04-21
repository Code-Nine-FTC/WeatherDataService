from logging.config import fileConfig
from alembic import context
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncConnection
from app.config.settings import settings
from app.core.models.db_model import Base
import asyncio
from app.core.models.db_model import User
from app.modules.security import PasswordManager
from sqlalchemy.future import select

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set the database URL from your settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

async def create_user(connection: AsyncConnection) -> None:
    """Criar um usuário inicial no banco de dados se ele não existir."""
    # Verificar se o usuário já existe
    result = await connection.execute(select(User).where(User.email == "admcodenine@gmail.com"))
    existing_user = result.scalar()

    if not existing_user:
        # Criar um novo usuário
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

async def table_exists(connection: AsyncConnection, table_name: str) -> bool:
    """Check if a table exists in the database."""
    result = await connection.execute(
        text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :table_name)"),
        {"table_name": table_name}
    )
    return result.scalar()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode using an asynchronous engine."""
    try:
        # Create an asynchronous engine
        connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

        async with connectable.connect() as connection:
            # Configure the context with the connection
            await connection.run_sync(do_run_migrations)

            # Check if the 'users' table exists before creating the admin user
            if await table_exists(connection, "users"):
                try:
                    await create_user(connection)
                    print("User creation process completed.")
                except Exception as user_error:
                    print(f"User creation error: {user_error}")
                    # Don't raise the error - this allows migrations to succeed even if user creation fails

    except ConnectionRefusedError as e:
        print(f"Database connection refused: {e}")
        print("Please check if the database server is running and the connection details are correct.")
        raise
    except Exception as e:
        print(f"An error occurred while running migrations: {e}")
        raise

def do_run_migrations(connection: AsyncConnection) -> None:
    """Run migrations synchronously within an asynchronous context."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Run the async migrations
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()