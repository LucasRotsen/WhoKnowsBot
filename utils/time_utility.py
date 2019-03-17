import time
from datetime import datetime
from time import strptime


def get_current_timestamp():
    # Get current time from the system
    now = datetime.now()

    # Convert DateTime to Timestamp
    now_date_time = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(
        now.minute) + ":" + str(now.second)
    now_timestamp = time.mktime(datetime.strptime(now_date_time, "%Y-%m-%d %H:%M:%S").timetuple())

    # Return the current time as timestamp format
    return now_timestamp


def convert_to_timestamp(twitter_date_format):
    created = twitter_date_format.split(" ")
    date_time = created[5] + "-" + str(strptime(created[1], '%b').tm_mon) + "-" + created[2] + " " + created[3]

    # Convert DateTime to Timestamp and return it
    return time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
