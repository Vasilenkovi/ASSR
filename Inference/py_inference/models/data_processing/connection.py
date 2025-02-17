import os
from sqlalchemy import create_engine


def get_engine():
    dialect   = os.getenv("dialect")
    driver    = os.getenv("driver")
    username  = os.getenv("username")
    password  = os.getenv("password")
    host_name = os.getenv("host_name")
    host_port = os.getenv("host_port")
    database  = os.getenv("database")

    url = f"{dialect}+{driver}://{username}:{password}@{host_name}:{host_port}/{database}"

    return create_engine(url)