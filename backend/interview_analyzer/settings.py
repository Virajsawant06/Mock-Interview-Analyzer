from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
SECRET_KEY = '2DdvARSAz8N5AIJi7Bklq0jYcJtANrG6Zmp5ZUUXerFoX6jN_-_rOSXGtnvLQ-Bto-M'
ALLOWED_HOSTS = ['*']
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Optional, if you have a 'static' folder in your project
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # For production


CORS_ALLOW_ALL_ORIGINS = True  # Allow React frontend to make requests

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'core',
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Create a 'templates' directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ Add this
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ Add this
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ Add this
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MONGODB_SETTINGS = {
    'host': 'mongodb://localhost:27017/MIA',
    'db': 'MIA'
}
DATABASES = {}  # Disable default database

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

ROOT_URLCONF = 'interview_analyzer.urls'  # Change to your project's name
