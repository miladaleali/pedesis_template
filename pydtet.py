from pydantic import (
    BaseSettings,
    PostgresDsn,
    RedisDsn,
    Field,
)
from pathlib import Path
import caissa.t2 as t2

class Settings(BaseSettings):
    api_key: str = Field(..., env="api_key")
    secret_key: str = Field(..., env='secret_key')
    redis: RedisDsn = Field(..., env='redis')
    postgres: PostgresDsn = Field(..., env='postgres')
    base_dir: Path = Field(default_factory=t2.get_dir)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        fields = {
            'redis': {
                'env': 'redis'
            }
        }

settings = Settings()

print(settings.dict())
