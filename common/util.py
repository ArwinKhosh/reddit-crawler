'''Utility functions to be reused across project'''

import os
import time
import datetime
import calendar

# TODO: Describe what each function does.
#! Probably some of this custom functionality is achivable with the imported packes

def increment_time(epoch_time, add_day = 0, add_hour = 0, add_min = 0, add_sec = 0):

    epoch_time_add = epoch_time + \
                     add_day*24*60*60 + \
                     add_hour*60*60 + \
                     add_min*60 + \
                     add_sec
    return epoch_time_add


def epoch_to_gmt(epoch_time, add_day = 0, add_sec = 0,*,format = 'date'):

    epoch_time = epoch_time + add_day*24*60*60 + add_sec

    if format == 'datetime':
        date_format = '%Y-%m-%d_%H-%M-%S'
    else:
        date_format = '%Y-%m-%d'

    gmt_date = time.strftime(date_format, time.gmtime(epoch_time))

    return gmt_date

def gmt_to_epoch(gmt_date, hour = 0, min = 0, sec = 0, add_day = 0, add_sec = 0 ):
    # Convert time in GMT to epoch time.

    gmt_datetime = gmt_date + " " + str(hour) + ":" + str(min)  + ":" + str(sec) 

    epoch_time = calendar.timegm(time.strptime(gmt_datetime, '%Y-%m-%d %H:%M:%S'))

    add_day_sec = add_day*24*60*60 + add_sec

    return epoch_time + add_day_sec

def exist_date(begin_date):
    # Checks if datafile already exists

    file_list = os.listdir("data\comments_by_date")
    
    # Strip JSON
    files = [item.split('.')[0] for item in file_list]

    # Calculate days between input date and today.
    sdate = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    edate = datetime.datetime.now()  

    delta = edate - sdate       # as timedelta

    delta_days = []
    for i in range(delta.days + 1):
        day = sdate + datetime.timedelta(days=i)
        delta_days.append(day.strftime("%Y-%m-%d"))

    # Compare intersection between files that already exist and the dates we want
    days_exist = list(set(delta_days).intersection(set(files)))

    return days_exist