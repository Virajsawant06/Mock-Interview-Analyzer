from django.core.management.base import BaseCommand
from core.mongodb_settings import MongoDBClient

class Command(BaseCommand):
    help = 'Initialize MongoDB collections'

    def handle(self, *args, **kwargs):
        client = MongoDBClient.get_instance()
        db = client.get_database()
        
        # Create collections
        try:
            db.create_collection("questions")
            db.create_collection("sessions")
            self.stdout.write(self.style.SUCCESS('MongoDB initialized successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error initializing MongoDB: {e}'))
