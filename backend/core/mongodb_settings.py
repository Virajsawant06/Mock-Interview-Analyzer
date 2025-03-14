from pymongo import MongoClient
from django.conf import settings

class MongoDBClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MongoClient(settings.MONGODB_SETTINGS['host'])
        return cls._instance

    @classmethod
    def get_database(cls):
        client = cls.get_instance()
        return client[settings.MONGODB_SETTINGS['db']]

    @classmethod
    def close(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None
