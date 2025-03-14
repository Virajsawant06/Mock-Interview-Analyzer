import pandas as pd
from datetime import datetime

class InterviewReportGenerator:
    def __init__(self, emotion_data, qa_responses):
        self.emotion_data = emotion_data
        self.qa_responses = qa_responses
        
    def generate_report(self):
        emotion_analysis = self._analyze_emotions()
        qa_analysis = self._analyze_qa_responses()
        
        report = {
            'timestamp': datetime.now(),
            'emotion_analysis': emotion_analysis,
            'qa_analysis': qa_analysis,
            'overall_score': self._calculate_overall_score(emotion_analysis, qa_analysis)
        }
        
        return report
    
    def _analyze_emotions(self):
        if self.emotion_data.empty:
            return {'error': 'No emotion data available'}
            
        emotion_counts = self.emotion_data['emotion'].value_counts()
        total_duration = len(self.emotion_data)
        
        analysis = {
            'emotion_distribution': {
                emotion: count/total_duration * 100 
                for emotion, count in emotion_counts.items()
            },
            'confidence_indicators': self._analyze_confidence_indicators()
        }
        
        return analysis
    
    def _analyze_qa_responses(self):
        if not self.qa_responses:
            return {'error': 'No QA responses available'}
            
        correct_answers = sum(1 for resp in self.qa_responses.values() 
                            if resp.get('is_correct', False))
        total_questions = len(self.qa_responses)
        
        analysis = {
            'score': (correct_answers / total_questions * 100) if total_questions > 0 else 0,
            'correct_answers': correct_answers,
            'total_questions': total_questions,
            'detailed_responses': self.qa_responses
        }
        
        return analysis
    
    def _analyze_confidence_indicators(self):
        positive_emotions = ['happy', 'neutral']
        negative_emotions = ['sad', 'angry', 'fear']
        
        positive_count = self.emotion_data['emotion'].isin(positive_emotions).sum()
        negative_count = self.emotion_data['emotion'].isin(negative_emotions).sum()
        total_count = len(self.emotion_data)
        
        return {
            'confidence_score': (positive_count / total_count * 100) if total_count > 0 else 0,
            'stress_level': (negative_count / total_count * 100) if total_count > 0 else 0
        }
    
    def _calculate_overall_score(self, emotion_analysis, qa_analysis):
        if 'error' in emotion_analysis or 'error' in qa_analysis:
            return 0
            
        emotion_score = emotion_analysis['confidence_indicators']['confidence_score']
        qa_score = qa_analysis['score']
        
        # Weight: 30% emotion, 70% QA performance
        return (0.3 * emotion_score + 0.7 * qa_score)