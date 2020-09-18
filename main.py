from datetime import datetime, timezone
from auth import get_service
from dateutil.parser import parse
from dateutil.tz import gettz
from multiprocessing import Process
import time
import sched
import webbrowser

UPDATE_TIME = 120 # minutes
MINUTES_BEFORE = 2
EMAIL = ['example@gmail.com']
TIMEZONE = 'America/La_Paz'

scheduler = sched.scheduler(time.time, time.sleep)

def update_db():
  db = []
  service = get_service()
  calendars = service.calendarList().list().execute()
  local_time_start = datetime.now(timezone.utc).astimezone().replace(hour=0, minute=0, second=0)
  local_time_start = local_time_start.isoformat()

  local_time_end = datetime.now(timezone.utc).astimezone().replace(hour=23, minute=59, second=59)
  local_time_end = local_time_end.isoformat()

  for calendar in calendars['items']:
    if calendar['id'] in EMAIL:
      events = service.events().list(calendarId=calendar['id'], timeMin=local_time_start, timeMax=local_time_end, timeZone=TIMEZONE).execute()
      for event in events['items']:
        db.append(event)
  return db
        
def parse_event(event):
  event_object = {}
  if 'hangoutLink' in event.keys():
    event_object['hangoutLink'] = event['hangoutLink']
    if 'summary' in event.keys():
      event_object['summary'] = event['summary']
    if 'start' in event.keys():
      event_object['start'] = parse(event['start']['dateTime']).timestamp()
  return event_object

def alert (event):
  print('Openning browser...', datetime.now())
  webbrowser.open(event['hangoutLink'], new=2)
  print('Meeting: {}'.format(event['summary']))

def launch_scheduler(events):
  for event in events:
    event = parse_event(event)
    if(event['start'] > time.time()):
      scheduler.enterabs((event['start'] - (MINUTES_BEFORE * 60)), 1, alert, (event,))
      print('{}, active event :D'.format(event['summary']))
    else:
      print('{}, past event :|'.format(event['summary']))
  print('launching schedulers...')
  scheduler.run()

def kill_jobs(jobs):
  for job in jobs:
    job.terminate()
    job.join()

if __name__ == "__main__":
  while True:
    jobs = []
    db = update_db()
    print('updating data...')
    kill_jobs(jobs)
    if len(db) > 0:
      print('{} events found!'.format(len(db)))
      process = Process(target=launch_scheduler, args=(db,))
      jobs.append(process)
      process.start()
    time.sleep(UPDATE_TIME * 60)
