import os
import sys
from dotenv import load_dotenv

def main():
    """Run administrative tasks."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interview_analyzer.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # Add custom commands for MongoDB initialization
    if sys.argv[1:2] == ['init_db']:
        from core.mongodb_settings import MongoDBClient
        client = MongoDBClient.get_instance()
        db = client.get_database()
        
        # Initialize database collections
        try:
            # Create collections and indexes
            from core.management.commands.init_mongodb import Command
            cmd = Command()
            cmd.handle()
            print("MongoDB initialization completed successfully!")
        except Exception as e:
            print(f"Error initializing MongoDB: {e}")
        finally:
            client.close()
        return
        
    # Add custom command for test data
    if sys.argv[1:2] == ['load_test_data']:
        from core.management.commands.load_test_data import Command
        cmd = Command()
        cmd.handle()
        return
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

# core/management/commands/load_test_data.py
from django.core.management.base import BaseCommand
from core.mongodb_settings import MongoDBClient
from datetime import datetime

class Command(BaseCommand):
    help = 'Load test data into MongoDB collections'

    def handle(self, *args, **kwargs):
        client = MongoDBClient.get_instance()
        db = client.get_database()
        
        # Sample interview questions
        test_questions = [
            {
                "question": "Explain the concept of deep learning.",
                "expected_keywords": ["neural networks", "layers", "training", "algorithms"],
                "difficulty": "medium",
                "category": "machine_learning",
                "created_at": datetime.now()
            },
            {
                "question": "What is the difference between HTTP and HTTPS?",
                "expected_keywords": ["security", "encryption", "ssl", "certificates"],
                "difficulty": "easy",
                "category": "networking",
                "created_at": datetime.now()
            },
            {
                "question": "Describe the principles of clean code.",
                "expected_keywords": ["readability", "maintainability", "simplicity", "dry"],
                "difficulty": "medium",
                "category": "programming",
                "created_at": datetime.now()
            },
            {
                "question": "What are design patterns in software engineering?",
                "expected_keywords": ["solutions", "problems", "reusable", "patterns"],
                "difficulty": "hard",
                "category": "software_design",
                "created_at": datetime.now()
            },
            {
                "question": "Explain the CAP theorem in distributed systems.",
                "expected_keywords": ["consistency", "availability", "partition tolerance"],
                "difficulty": "hard",
                "category": "distributed_systems",
                "created_at": datetime.now()
            }
        ]
        
        # Insert test questions
        try:
            db.questions.insert_many(test_questions)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(test_questions)} test questions'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading test questions: {e}'))
        
        # Sample interview sessions
        test_sessions = [
            {
                "candidate_id": "test_candidate_1",
                "start_time": datetime.now(),
                "status": "completed",
                "questions_asked": 5,
                "correct_answers": 4,
                "emotion_data": {
                    "happy": 45,
                    "neutral": 35,
                    "anxious": 20
                }
            },
            {
                "candidate_id": "test_candidate_2",
                "start_time": datetime.now(),
                "status": "completed",
                "questions_asked": 5,
                "correct_answers": 3,
                "emotion_data": {
                    "happy": 30,
                    "neutral": 40,
                    "anxious": 30
                }
            }
        ]
        
        # Insert test sessions
        try:
            db.sessions.insert_many(test_sessions)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(test_sessions)} test sessions'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading test sessions: {e}'))
