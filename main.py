from datetime import datetime, timezone
from auth import get_service
from dateutil.parser import parse
from dateutil.tz import gettz
import time
import sched

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

def launch_alert (event):
  print(event)

if __name__ == "__main__":
  while True:
    db = update_db()
    for event in db:
      event = parse_event(event)
      scheduler.enterabs(event['start'], 1, launch_alert, (event,))
    scheduler.run()
    print('end')
    time.sleep(10000)


# print(time.time())
# now = time.time()
# event_time = parse('2020-09-10T23:40:00-04:00').timestamp()
# scheduler.enterabs(event_time+2, 1, test, ('hi 3',))
# scheduler.enterabs(event_time+1, 1, test, ('hi 1',))
# scheduler.enterabs(event_time+10, 1, test, ('hi 2',))
# scheduler.run()
# print(time.time())
# print('finish')