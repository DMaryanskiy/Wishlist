import functools
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    db_url: str

    access_token_expire_minutes: int
    refresh_token_expire_days: int

    secret_key: str
    algorithm: str

    model_config = pydantic_settings.SettingsConfigDict(env_file='.env')


@functools.lru_cache
def get_settings():
    return Settings()
