from django.db import models
from pymongo import MongoClient
from django.conf import settings

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_SETTINGS['host'])
        self.db = self.client[settings.MONGODB_SETTINGS['db']]
    
    def get_collection(self, collection_name):
        return self.db[collection_name]

class InterviewQuestion:
    collection_name = 'questions'
    
    @classmethod
    def get_questions(cls):
        manager = MongoDBManager()
        collection = manager.get_collection(cls.collection_name)
        return list(collection.find())
    
    @classmethod
    def add_question(cls, question_data):
        manager = MongoDBManager()
        collection = manager.get_collection(cls.collection_name)
        return collection.insert_one(question_data)