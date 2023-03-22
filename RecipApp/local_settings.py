import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'recipeapp',
            'USER':'recipappadm',
            'PASSWORD': 'adm12345',
            'HOST': 'recipeapp.ccusntviihbq.eu-north-1.rds.amazonaws.com',
            'PORT': '5432'}
}