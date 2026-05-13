mariodatetime import datetime, timedelta
from apple_calendar_integration import ICloudCalendarAPI
import sys, os
sys.path.append(os.path.expanduser("~/myshells/pyplugs"))
from debug import debug

api = ICloudCalendarAPI(username, password)

start_date = int(datetime.now().timestamp())
debug(start_date)
end_date = start_date + timedelta(hours=2).seconds
etag, ctag, guid = api.create_event('Your title', start_date, end_date)
