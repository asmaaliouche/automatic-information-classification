"""
Script to create the PostgreSQL database tables.

Usage:
    poetry run python -m db.create_db

This script:
    1. Connects to the PostgreSQL database.
    2. Creates all tables defined in the ORM models (employees, predictions).
    3. Prints the created table names for confirmation.
"""

from db.database import Base, engine
from db.models import Employee, Prediction  # noqa: F401 — needed to register models


def create_tables():
    """Create all database tables from the ORM models."""
    print("🔧 Creating database tables...")
    Base.metadata.create_all(bind=engine)

    # Confirm which tables were created
    table_names = Base.metadata.tables.keys()
    for name in table_names:
        print(f"  ✅ Table '{name}' ready.")

    print(f"\n✅ All {len(table_names)} tables created successfully.")


if __name__ == "__main__":
    create_tables()
