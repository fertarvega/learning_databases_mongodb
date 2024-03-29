from flask_pymongo import pymongo
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@example.3fmjj.mongodb.net/{DB_NAME}?retryWrites=true&w=majority")


# Here you need to add the collection name
db = client.db_example