from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from logging.config import fileConfig
from app.core.models.db_model import Base
import os
import asyncio

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Definir URL do banco
config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "postgresql+asyncpg://testuser:testpass@localhost:5432/testdb")
)

# Metadados das tabelas
target_metadata = Base.metadata


def run_migrations_offline():
    """Executa migrações no modo offline."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Executa migrações no modo online com AsyncEngine."""
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))

    async with connectable.connect() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn, target_metadata=target_metadata
            )
        )

        async with connection.begin():
            await connection.run_sync(context.run_migrations)

    await connectable.dispose()


# Roteador principal
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
