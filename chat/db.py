# chat/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
# You can either use the default database in your URI or specify one:
db = client['ai_chatbot']  # or client['chatbot_db']
# We'll store chat history in a collection named "chat_history"
collection = db.chat_history
