from pydantic import BaseSettings

class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    database_name: str = 'HTW_manager'
    database_port: str = '5432'
    database_host: str = 'localhost'
    database_user: str = 'postgres'
    database_password: str = '82647436'

    database_connect: str = f'postgresql+psycopg2://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'

    jwt_secret: str = 'Hyx3r68oiDvi9-Qma8CwJbV2C6YUqsVQeG2VMXSfVD0'
    jwt_algorithm: str = 'HS256'
    jwt_access_expiration: int = 60  # 1 час
    jwt_refresh_expiration: int = 60 * 24 * 30  # 1 месяц



settings = Settings()