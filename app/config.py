from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    server_url: str
    dbx_token: str
    gh_token: str
    secret: str
    keys: str
    debug: bool = False
    root_path: str = ''

    class Config:
        env_file = ".env"
