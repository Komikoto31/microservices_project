from app.database import engine
from sqlalchemy import inspect

def test_tables_exist():
    """Проверка, что таблица deliveries существует"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "deliveries" in tables

def test_table_columns():
    """Проверка колонок таблицы deliveries"""
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns("deliveries")]
    expected = ["id", "address", "date", "status", "comment", "customer_id"]
    for col in expected:
        assert col in columns
