from pymongo import MongoClient
from config import MONGO_URI

# Connect to MongoDB
conn = MongoClient(MONGO_URI)
# db = conn.databaseOne
db = conn.studentTest
