import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
    
from app.database import DATABASE_URL, Base
from app import models 

config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Extract metadata from the SQLAlchemy Base after models module is loaded
target_metadata = Base.metadata

print(f"ALEMBIC DEBUG: Tables found in metadata: {list(target_metadata.tables.keys())}")

# --------------------------------------------------------------------------
# 4. FILTERING LOGIC (The "Additive" Approach)
# --------------------------------------------------------------------------
def include_object(object, name, type_, reflected, compare_to):
    """
    Prevents Alembic from dropping tables that exist in the DB
    but are not defined in our SQLAlchemy schemas.
    """
    if type_ == "table":
        # If the table is in our schemas, manage it (Create/Alter)
        if name in target_metadata.tables:
            return True
        # If it's in the DB but NOT our schemas, ignore it (No Drop)
        if reflected:
            return False
    return True

# --------------------------------------------------------------------------
# 5. MIGRATION RUNNERS
# --------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # We use engine_from_config but override the URL to ensure it uses the .env value
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()