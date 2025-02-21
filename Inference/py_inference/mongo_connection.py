import os
import pymongo


def save_dict(collection_name: str, to_save: dict) -> None:
    username  = os.getenv("mongo_username")
    password  = os.getenv("mongo_password")
    host_name = os.getenv("mongo_host_name")
    host_port = os.getenv("mongo_host_port")
    database  = os.getenv("mongo_database")
    
    url = f"mongodb://{username}:{password}@{host_name}:{host_port}"

    client = pymongo.MongoClient(url)
    database = client[database]
    collection = database[collection_name]
        
    collection.insert_one(to_save)
