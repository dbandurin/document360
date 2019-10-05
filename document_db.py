import pymongo
from pymongo import MongoClient

class DocumentDB():
    def __init__(self, db_name, collection_name):
        #Connect to MongoDB - Note: Change connection string as needed
        #client = MongoClient(port=27017)
        client = MongoClient('mongodb://localhost:27017/')
        #client = MongoClient('mongodb://data-science-0.strike.0638.mongodbdns.com:27017')

        self.collection = client[db_name][collection_name]
        self.collection.create_index([("$**", 'text')]) 

    def write_to_db(self, bucket_name, fname, text):
        self.collection.insert_one({"bucket_name":bucket_name, "file_name":fname, 
                                    "content":text, "language":"english"})


    #Search
    def search_for_docs(self, search_text, n=10):
        coursor = self.collection.find({"$text": {"$search": search_text}},
                                       {"score": {"$meta": "textScore"}}).limit(n)
        coursor.sort([('score', {'$meta': 'textScore'})])

        collectionResults = []
        for res in coursor:
            collectionResults.append({'file_name':res['file_name'],
                                      'content':res['content'],
                                      'score':res['score']})

        return collectionResults

