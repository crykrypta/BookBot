from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None):
    # Fill env class
    env = Env()
    env.load_env()

    # Making config class from env variables
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_id=env.int('ADMIN_ID')
        )
    )
