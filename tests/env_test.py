from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.models.db_model import Base
import os

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "postgresql+asyncpg://testuser:testpass@localhost:5432/testdb"))

target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_async_engine(config.get_main_option("sqlalchemy.url"))
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()