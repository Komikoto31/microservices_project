from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.settings import settings
from app.schemas.base_schema import Base
from app.schemas.delivery import Delivery
import logging
import time

logger = logging.getLogger(__name__)


def wait_for_db(max_retries=30, retry_interval=2):
    """Ожидает пока БД станет доступной"""
    for i in range(max_retries):
        try:
            # Пробуем создать временное подключение
            temp_engine = create_engine(settings.postgres_url, connect_args={'connect_timeout': 5})
            with temp_engine.connect() as conn:
                logger.info("Database is ready!")
                return True
        except OperationalError as e:
            if i < max_retries - 1:
                logger.info(f"Database not ready, retrying in {retry_interval}s... ({i + 1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                logger.error(f"Could not connect to database after {max_retries} retries: {e}")
                raise


# Создаем движок БД
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Создает таблицы в БД"""
    try:
        # Ждем пока БД станет доступной
        wait_for_db()

        # Удаляем все таблицы и создаем заново
        Base.metadata.drop_all(bind=engine)
        logger.info("Tables dropped successfully")

        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully")

        # Проверяем, что таблица создалась с нужными колонками
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = inspector.get_columns('deliveries')
        logger.info(f"Table 'deliveries' columns: {[col['name'] for col in columns]}")

    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise