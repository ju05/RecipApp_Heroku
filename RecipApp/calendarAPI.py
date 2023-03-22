from pprint import pprint
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

servie = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)