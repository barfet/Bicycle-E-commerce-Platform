import os
from urllib.parse import urlparse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore' # Ignore extra fields from .env
    )

    DATABASE_URL: str
    # Add TEST_DATABASE_URL. It will be loaded from .env
    TEST_DATABASE_URL: str | None = None 

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256" # Add JWT algorithm

    @computed_field
    @property
    def POSTGRES_DB(self) -> str:
        """Derives the database name from DATABASE_URL."""
        parsed_url = urlparse(self.DATABASE_URL)
        # Get the path part (e.g., '/bicycle_db') and remove leading slash
        db_name = parsed_url.path.lstrip('/')
        return db_name

# Create a single instance of the settings to be imported
settings = Settings() 