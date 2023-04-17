import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd68dq15a42f444',
        'USER':'mcbgkwgigfihvt',
        'PASSWORD': '74f790679537dcd4c23c57fad718c7a772b3d047ab7d9c5ff640db29a802edf7',
        'HOST': 'ec2-3-234-204-26.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}