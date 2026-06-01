from pathlib import Path
from typing import Optional

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', extra='ignore'
    )


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='db_')

    host: str
    name: str
    password: SecretStr
    port: int
    user: str
    url: Optional[str] = Field(default=None)

    test_host: str = 'localhost'
    test_name: str = 'test_db'
    test_password: SecretStr = SecretStr('postgres')
    test_port: int = 5432
    test_user: str = 'postgres'
    test_url: Optional[str] = Field(default=None)

    @staticmethod
    def create_url(info: ValidationInfo, prefix: str = '') -> str:
        """Build connection string from validation info using a prefix."""
        data = info.data
        user = data.get(f'{prefix}user')
        pwd = data.get(f'{prefix}password')
        host = data.get(f'{prefix}host')
        port = data.get(f'{prefix}port')
        name = data.get(f'{prefix}name')

        secret = pwd.get_secret_value() if pwd else ''
        return f'postgresql+asyncpg://{user}:{secret}@{host}:{port}/{name}'

    @field_validator('url', mode='before')
    @classmethod
    def assemble_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        """Assemble main database URL if not provided."""
        return v if v else cls.create_url(info, prefix='')

    @field_validator('test_url', mode='before')
    @classmethod
    def assemble_test_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        """Assemble test database URL if not provided."""
        return v if v else cls.create_url(info, prefix='test_')


class AppConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='app_')
    name: str
    mode: str


class Settings(BaseSettings):
    app: AppConfig = Field(default_factory=AppConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)

    @classmethod
    def load(cls) -> 'Settings':
        return cls()


settings: Settings = Settings.load()
