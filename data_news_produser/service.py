import json

from pymongo import MongoClient
db_name = "terror_db"
collection_name = "event_collection"
client = MongoClient("mongodb://root:1234@localhost:27018")  # עדכן את הפורט אם צריך
db = client[db_name]
collection = db[collection_name]

def save_json_to_mongo(json_data):

    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    result = collection.insert_one(json_data)
    print(f"Document inserted with ID: {str(result.inserted_id)}")







