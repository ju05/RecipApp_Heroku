import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recipeapp_heroku',
        'USER':'postgres',
        'PASSWORD': '1948',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}