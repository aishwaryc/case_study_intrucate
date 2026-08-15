import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
database_name = os.getenv("MONGO_DB_NAME")

client = MongoClient(mongo_uri)

db = client[database_name]

prompts_collection = db["prompts"]
history_collection = db["history"]