from __future__ import print_function
import datetime
import os.path
from events import Task, BusyBlock, TaskBlock
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getStartEndDates():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Calculate the first Sunday of the week and coming Saturday of the week
    day_of_week = datetime.datetime.today().weekday()
    if(day_of_week== 6):
        sunday_date =  datetime.datetime.now() - datetime.timedelta(days=6-day_of_week)
    else:
        sunday_date =  datetime.datetime.now() - datetime.timedelta(days=1+day_of_week)
    sunday_start = datetime.datetime.combine(sunday_date.date(), datetime.time(0,0,0))    
    
    saturday_date =  datetime.datetime.now() + datetime.timedelta(days= 28 + (5 - day_of_week) )
    saturday_end = datetime.datetime.combine(saturday_date.date(), datetime.time(23,59,59))    
    
    delta = saturday_end.date() - sunday_start.date()
    dates = []
    for i in range(delta.days + 1):
        day = sunday_start + datetime.timedelta(days=i)
        dates.append(day.strftime("%m.%d"))
    return dates

def getCalendarInfo():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Calculate the first Sunday of the week and coming Saturday of the week
    day_of_week = datetime.datetime.today().weekday()
    if(day_of_week== 6):
        sunday_date =  datetime.datetime.now() - datetime.timedelta(days=6-day_of_week)
    else:
        sunday_date =  datetime.datetime.now() - datetime.timedelta(days=1+day_of_week)
    sunday_start = datetime.datetime.combine(sunday_date.date(), datetime.time(0,0,0))    
    sunday_formated =  sunday_start.isoformat() + 'Z' # 'Z' indicates UTC time

    saturday_date =  datetime.datetime.now() + datetime.timedelta(days= 28 + (5 - day_of_week) )
    saturday_end = datetime.datetime.combine(saturday_date.date(), datetime.time(23,59,59))    
    saturday_formated =  saturday_end.isoformat() + 'Z' # 'Z' indicates UTC time

    #gets all the events from a week
    events_result = service.events().list(calendarId='primary', timeMin=sunday_formated,
                                        timeMax= saturday_formated, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def populateBusyBlocks():
    busyBlocksImported = []
    events = getCalendarInfo()
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        if(event['start'].get('dateTime')!= None and event['end'].get('dateTime') != None):
            start = datetime.datetime.fromisoformat(event['start'].get('dateTime'))
            end = datetime.datetime.fromisoformat(event['end'].get('dateTime'))
            name = event['summary']
            busyBlocksImported.append(BusyBlock(name, start, end))    
    return busyBlocksImported

def populateCalendar():
    calendarEvents = [[] for i in range(7)]
    events = getCalendarInfo()
    
    if not events:
        print('No upcoming events found.')
    for event in events:
        data = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.fromisoformat(data)

        data = event['end'].get('dateTime', event['end'].get('date'))
        end = datetime.datetime.fromisoformat(data)
        name = event['summary']
        if(calendarEvents[start.weekday()] == None):
            calendarEvents[start.weekday()] = [{"start_day": start.date().strftime("%m.%d"), "start_time": start.time().strftime("%H:%M"), "end_day": end.date().strftime("%m.%d"), "end_time": end.time().strftime("%H:%M"), "name": name}]
        else:   
            calendarEvents[start.weekday()].append({"start_day": start.date().strftime("%m.%d"), "start_time": start.time().strftime("%H:%M"), "end_day": end.date().strftime("%m.%d"), "end_time": end.time().strftime("%H:%M"), "name": name})
    return calendarEvents

def addTaskToEvent(task_blocks, events):
    for block in task_blocks:
        new_block={"start_day": block.start_time.strftime("%m.%d"), 
                    "start_time": block.start_time.time().strftime("%H:%M"), 
                    "end_day": block.end_time.date().strftime("%m.%d"), 
                    "end_time": block.end_time.time().strftime("%H:%M"), 
                    "name": block.task.name + "("+str(block.task_block_num) + ")"
        }
        events[block.start_time.weekday()].append(new_block)
    return events

if __name__ == '__main__':
    getCalendarInfo()