import os
from sqlalchemy import Engine, create_engine


def get_engine():
    username  = os.getenv("postgres_username")
    password  = os.getenv("postgres_password")
    host_name = os.getenv("postgres_host_name")
    host_port = os.getenv("postgres_host_port")
    database  = os.getenv("postgres_database")

    url = f"postgresql+psycopg2://{username}:{password}@{host_name}:{host_port}/{database}"

    return create_engine(url)


class Engine_Connected:
    
    engine: None | Engine

    def __init__(self):
        self.engine = get_engine()
