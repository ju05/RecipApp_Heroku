import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys 
from RecipApp.Google import convert_to_RFC_datetime

sys.path.append('/app/RecipApp')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(request):
    '''creates the event when the user click the button 
    using request to take the recipe ID and add to the event'''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
 
    recipe_id = request.session.get('recipe_id')
    if os.path.exists('RecipApp\\token.json'):
        creds = Credentials.from_authorized_user_file('RecipApp\\token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'RecipApp\\google-credentials.json', SCOPES)
            creds = flow.run_local_server(port=56002)
        # Save the credentials for the next run
        with open('RecipApp\\token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        recipe = request.POST.get('recipe')
        hour_adjustment = -2    
        
        event = {
        'summary': 'Prepare Lunch',
        'location': 'Home',
        'description': f'http://127.0.0.1:8000/detail/{recipe_id}',
        'start': {
            'dateTime': convert_to_RFC_datetime(2023, 4, 18, 12 + hour_adjustment, 30),
            'timeZone': 'Asia/Jerusalem',
        },
        'end': {
            'dateTime': convert_to_RFC_datetime(2023, 4, 18, 13 + hour_adjustment, 30),
            'timeZone': 'Asia/Jerusalem',
        },      
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        print(event.get('htmlLink'))


    except HttpError as error:
        print('An error occurred: %s' % error)

