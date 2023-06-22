from dataclasses import dataclass
from environs import Env


@dataclass
class SettingsData:
    redis_host: str
    redis_password: str
    pg_host: str
    pg_port: int
    pg_user: str
    pg_password: str
    pg_name: str


@dataclass
class Settings:
    api: SettingsData


def get_settings():
    env = Env()
    env.read_env()

    return Settings(
        api=SettingsData(
            redis_host=env.str('REDIS_HOST'),
            redis_password=env.str('REDIS_PASSWORD'),
            pg_host=env.str('PG_HOST'),
            pg_port=env.str('PG_PORT'),
            pg_user=env.str('PGUSER'),
            pg_password=env.str('PG_PASSWORD'),
            pg_name=env.str('PG_NAME'),
        )
    )


settings = get_settings()
