from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View

from core.models import InterviewQuestion
from .utils.emotion_analyzer import FacialExpressionAnalyzer
from .utils.interview_report import InterviewReportGenerator
from .utils.qna_system import QnASystem
import json
from bson import ObjectId
import datetime
import pandas as pd
import cv2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.utils.emotion_analyzer import FacialExpressionAnalyzer

analyzer = FacialExpressionAnalyzer()

import cv2
import numpy as np
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from deepface import DeepFace
from pymongo import MongoClient
from django.conf import settings

# Connect to MongoDB
client = MongoClient(settings.MONGODB_SETTINGS["host"])
db = client[settings.MONGODB_SETTINGS["db"]]
emotions_collection = db["emotions"]
questions_collection = db["questions"]

@csrf_exempt
def detect_emotion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Ensure "image" exists in request data
            if "image" not in data:
                return JsonResponse({"error": "No image provided"}, status=400)

            image_data = data["image"]

            # Convert Base64 image to OpenCV format
            image_bytes = base64.b64decode(image_data.split(',')[1])
            image_np = np.frombuffer(image_bytes, dtype=np.uint8)
            frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            # Ensure frame is not None
            if frame is None:
                return JsonResponse({"error": "Invalid frame received"}, status=400)

            # Run DeepFace emotion detection
            prediction = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = prediction[0]['dominant_emotion']

            # Save detected emotion with timestamp to MongoDB
            emotions_collection.insert_one({
                "timestamp": datetime.datetime.utcnow(),
                "emotion": dominant_emotion
            })

            return JsonResponse({"emotion": dominant_emotion})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



class InterviewView(View):
    def get(self, request):
        qna_system = QnASystem()
        questions = qna_system.get_random_questions()
        return render(request, 'core/interview.html', {'questions': questions})
    
    def post(self, request):
        data = json.loads(request.body)
        
        # Handle answer submission and emotion data
        qna_system = QnASystem()
        emotion_analyzer = FacialExpressionAnalyzer()
        
        answer_verification = qna_system.verify_answer(
            data['question_id'],
            data['answer']
        )
        
        # Generate and save report
        emotion_data = emotion_analyzer.get_emotion_report()
        report_generator = InterviewReportGenerator(
            emotion_data,
            {data['question_id']: answer_verification}
        )
        
        report = report_generator.generate_report()
        
        return JsonResponse({
            'verification': answer_verification,
            'report': report
        })
        
class IndexView(View):
    def get(self, request):
        return render(request, 'core/index.html')

class StartInterviewView(View):
    def post(self, request):
        qna_system = QnASystem()
        questions = qna_system.get_random_questions()
        session_id = str(ObjectId())
        
        # Store session information in MongoDB
        session_data = {
            '_id': session_id,
            'questions': questions,
            'start_time': datetime.now(),
            'status': 'active'
        }
        qna_system.db.sessions.insert_one(session_data)
        
        return JsonResponse({
            'session_id': session_id,
            'questions': questions
        })

class EndInterviewView(View):
    def post(self, request):
        session_id = request.POST.get('session_id')
        qna_system = QnASystem()
        
        # Update session status
        qna_system.db.sessions.update_one(
            {'_id': session_id},
            {'$set': {
                'end_time': datetime.now(),
                'status': 'completed'
            }}
        )
        
        return JsonResponse({'status': 'success'})

class StartEmotionDetectionView(View):
    def post(self, request):
        emotion_analyzer = FacialExpressionAnalyzer()
        emotion_analyzer.start_emotion_detection()
        return JsonResponse({'status': 'started'})

class StopEmotionDetectionView(View):
    def post(self, request):
        emotion_analyzer = FacialExpressionAnalyzer()
        emotion_analyzer.stop_emotion_detection()
        return JsonResponse({'status': 'stopped'})

class VerifyAnswerView(View):
    def post(self, request):
        data = json.loads(request.body)
        qna_system = QnASystem()
        
        verification = qna_system.verify_answer(
            data['question_id'],
            data['answer']
        )
        
        return JsonResponse(verification)

class ResultsView(View):
    def get(self, request, session_id):
        qna_system = QnASystem()
        session = qna_system.db.sessions.find_one({'_id': session_id})
        
        if not session:
            return HttpResponse('Session not found', status=404)
            
        return render(request, 'core/results.html', {
            'session': session
        })

class ReportView(View):
    def get(self, request, session_id):
        qna_system = QnASystem()
        session = qna_system.db.sessions.find_one({'_id': session_id})
        
        if not session:
            return HttpResponse('Session not found', status=404)
            
        report_generator = InterviewReportGenerator(
            session.get('emotion_data', pd.DataFrame()),
            session.get('qa_responses', {})
        )
        
        report = report_generator.generate_report()
        
        return render(request, 'core/report.html', {
            'report': report
        })

class DownloadReportView(View):
    def get(self, request, session_id):
        qna_system = QnASystem()
        session = qna_system.db.sessions.find_one({'_id': session_id})
        
        if not session:
            return HttpResponse('Session not found', status=404)
            
        report_generator = InterviewReportGenerator(
            session.get('emotion_data', pd.DataFrame()),
            session.get('qa_responses', {})
        )
        
        report = report_generator.generate_report()
        
        # Generate PDF or other format here
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="interview_report_{session_id}.pdf"'
        
        # Add PDF generation logic here
        
        return response

class QuestionListView(View):
    def get(self, request):
        questions = list(questions_collection.find({}, {"_id": 0}))  # Exclude `_id` field
        return JsonResponse(questions, safe=False)
    
class AddQuestionView(View):
    def get(self, request):
        return render(request, 'core/add_question.html')
        
    def post(self, request):
        data = json.loads(request.body)
        qna_system = QnASystem()
        question_id = qna_system.collection.insert_one(data).inserted_id
        return JsonResponse({'id': str(question_id)})

class EditQuestionView(View):
    def get(self, request, question_id):
        qna_system = QnASystem()
        question = qna_system.collection.find_one({'_id': ObjectId(question_id)})
        return render(request, 'core/edit_question.html', {
            'question': question
        })
        
    def post(self, request, question_id):
        data = json.loads(request.body)
        qna_system = QnASystem()
        qna_system.collection.update_one(
            {'_id': ObjectId(question_id)},
            {'$set': data}
        )
        return JsonResponse({'status': 'success'})

class DeleteQuestionView(View):
    def post(self, request, question_id):
        qna_system = QnASystem()
        qna_system.collection.delete_one({'_id': ObjectId(question_id)})
        return JsonResponse({'status': 'success'})