from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ecommerce"]
orders_collection = db["orders"]
products_collection = db["products"]

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
