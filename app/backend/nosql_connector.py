from pymongo import MongoClient
import json
from config_params import COSMOS_CONNECTION_STRING, DB_NAME, COLLECTION_NAME

class NoSQLConnector:
    def __init__(self):
        self.MONGO_URL = COSMOS_CONNECTION_STRING
        self.database_name = DB_NAME
        self.collection_name = COLLECTION_NAME
        self.client = None
    
    def connect_to_db(self):
        client = MongoClient(self.MONGO_URL)
        self.client = client
        db = client[self.database_name] 
        if self.database_name not in client.list_database_names():
            # Create a database with 400 RU throughput that can be shared across
            # the DB's collections
            db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
            print("Created db '{}' with shared throughput.\n".format(self.database_name))
        else:
            print("Using database: '{}'.\n".format(self.database_name))
        
        collection = db[self.collection_name]
        indexes = [
            {"key": {"_id": 1}, "name": "_id_1"},
            {"key": {"course_name": 1}, "name": "_id_2"},
            {"key": {"sec_number": 1}, "name": "_id_3"},
            {"key": {"sec_semester": 1}, "name": "_id_4"},
            {"key": {"sec_year": 1}, "name": "_id_5"},
            {"key": {"lecture_number": 1}, "name": "_id_6"}
        ]
        if self.collection_name not in db.list_collection_names():
            # Creates a unsharded collection that uses the DBs shared throughput
            db.command(
                {"customAction": "CreateCollection", "collection": self.collection_name}
            )
            print("Created collection '{}'.\n".format(self.collection_name))
        else:
            print("Using collection: '{}'.\n".format(self.collection_name))
 
        db.command(
            {
                "customAction": "UpdateCollection",
                "collection": self.collection_name,
                "indexes": indexes,
            }
        )
        print("Indexes are: {}\n".format(sorted(collection.index_information())))
        
        return collection

    def close_connection(self):
        self.client.close()

  