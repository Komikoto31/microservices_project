from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    amqp_url: str = "amqp://guest:guest123@51.250.26.59:5672/"
    postgres_url: str = "postgresql://user:password@delivery_db:5432/delivery_db"
    jwt_secret_key: str = "your-super-secret-jwt-key-here"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
