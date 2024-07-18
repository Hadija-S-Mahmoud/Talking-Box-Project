from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s672*6a8g#2_t0ox98cpjw=$bnhp3_t^$^y(04!e9k(fx$zgm&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set to False in production

# List of allowed hosts for the application
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # Admin interface
    'django.contrib.auth',  # Authentication framework
    'django.contrib.contenttypes',  # Content type framework
    'django.contrib.sessions',  # Session framework
    'django.contrib.messages',  # Messaging framework
    'django.contrib.staticfiles',  # Static files management
    'main',  # The main app of the project
    'channels',  # Django Channels for WebSocket and background tasks
]

# Middleware definition
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common middleware functions
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # User authentication middleware
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework middleware
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Default backend for username
    'main.backends.EmailBackend',  # Custom backend for email login
)

# URL configuration
ROOT_URLCONF = 'talking_box_project.urls'

# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Use Django's template engine
        'DIRS': [os.path.join(BASE_DIR, 'main/templates')],  # Directory for template files
        'APP_DIRS': True,  # Look for templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Debug context processor
                'django.template.context_processors.request',  # Request context processor
                'django.contrib.auth.context_processors.auth',  # Auth context processor
                'django.contrib.messages.context_processors.messages',  # Messages context processor
            ],
        },
    },
]

# WSGI and ASGI application configurations
WSGI_APPLICATION = 'talking_box_project.wsgi.application'
ASGI_APPLICATION = 'talking_box_project.asgi.application'  # ASGI application for WebSocket and background tasks

# Database configuration
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite database
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file location
    }
}

# Password validation settings
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # User attribute similarity validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Minimum password length validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Common password validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Numeric password validator
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UniqueEmailValidator',  # Ensures email is unique
    },
]

# Internationalization settings
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'  # Language code for the application
TIME_ZONE = 'Africa/Nairobi'  # Time zone for the application
USE_I18N = True  # Enable Django’s translation system
USE_TZ = True  # Enable timezone support

# Static files (CSS, JavaScript, Images) settings
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'  # URL for serving static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'main/static')]  # Additional directories for static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collected static files

# Media files settings
MEDIA_URL = '/media/'  # URL for serving media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory for media files

# Channel Layers configuration
# WebSocket support
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',  # Use Redis as the channel layer backend
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # Redis server configuration
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGOUT_REDIRECT_URL = 'index'  # Redirect to the home page after logout

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'talkingboxteam@gmail.com'
EMAIL_HOST_PASSWORD = 'zfat cgzc huxv sxsv'
DEFAULT_FROM_EMAIL = 'talkingboxteam@gmail.com'
