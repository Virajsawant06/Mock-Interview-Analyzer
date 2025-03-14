from pymongo import MongoClient
import random
import difflib
from django.conf import settings

class QnASystem:
    def __init__(self):
        self.client = MongoClient(settings.MONGODB_SETTINGS['host'])
        self.db = self.client[settings.MONGODB_SETTINGS['db']]
        self.collection = self.db['questions']
        self.current_session = None
        
    def get_random_questions(self, count=5):
        questions = list(self.collection.find())
        return random.sample(questions, min(count, len(questions)))
    
    def verify_answer(self, question_id, answer):
        question = self.collection.find_one({'_id': question_id})
        if not question:
            return {'error': 'Question not found'}
            
        expected_keywords = question.get('expected_keywords', [])
        answer_lower = answer.lower()
        
        matched_keywords = [
            keyword for keyword in expected_keywords
            if keyword.lower() in answer_lower
        ]
        
        confidence = len(matched_keywords) / len(expected_keywords) * 100 if expected_keywords else 0
        
        return {
            'is_correct': bool(matched_keywords),
            'confidence': confidence,
            'matched_keywords': matched_keywords,
            'expected_keywords': expected_keywords
        }
    
    def save_session_results(self, session_data):
        return self.db.sessions.insert_one(session_data)