import datetime
#import pickle
#from pathlib import Path
from pprint import pprint
import matplotlib.pyplot as plt
import pylab
import numpy as np
import matplotlib.dates as mdates

def time_format(time):
    return str(time.hour)+":"+str(time.minute)+":"+str(time.second)

def timedelta_format(time):
    return time - datetime.timedelta(microseconds=time.microseconds)

def format_number(number):
    return ("{0:.2f}".format(number))

def build(history_dict):

    now = datetime.datetime.now()

    # dictionary_file = Path('./History.dict')
    #
    # if dictionary_file.is_file():
    #     pickle_in = open(dictionary_file,"rb")
    #     history_dict = pickle.load(pickle_in)

    #create dictionary of daily totals (sitting)
    historical_dict = {}
    for day in history_dict:
        historical_dict[day] = {}
        event_list = []
        for event in history_dict[day]:
            event_list.append(float(history_dict[day][event].seconds))
        historical_dict[day]['sitting_seconds'] = day_sitting_seconds = sum(event_list)
        historical_dict[day]['standing_seconds'] = day_standing_seconds = 28800 - day_sitting_seconds
        historical_dict[day]['sitting_hours'] = (historical_dict[day]['sitting_seconds']/60)/60
        historical_dict[day]['standing_hours'] = (historical_dict[day]['standing_seconds']/60)/60

    #find today and change data to show progress through day
    for day in historical_dict:
        if now.year == day.year:
            if now.month == day.month:
                if now.day == day.day:
                    todays_key = day
                    hours_in_day = 8
                    start_of_day = datetime.datetime(now.year, now.month, now.day, 7, 30)
                    end_of_day = datetime.datetime(now.year, now.month, now.day, 13, 30)
                    hours_into_day = now - start_of_day
                    historical_dict[day]['standing_seconds'] = hours_into_day.seconds - historical_dict[day]['sitting_seconds']
                    historical_dict[day]['standing_hours'] = (historical_dict[day]['standing_seconds']/60)/60

    #graph setup
    bar_y = []
    bar_y2 = []
    bar_x = []

    for day in historical_dict:
        bar_x.append(day)
        bar_y.append(historical_dict[day]['standing_hours'])
        bar_y2.append(historical_dict[day]['sitting_hours'])

    total_seconds = 28800
    todays_remaining = ((total_seconds - (historical_dict[todays_key]['standing_seconds'] + historical_dict[todays_key]['sitting_seconds']))/60)/60
    pie_list = [format_number(historical_dict[todays_key]['standing_hours']),\
                format_number(historical_dict[todays_key]['sitting_hours']),\
                format_number(todays_remaining)]
    pie_labels = ['Standing','Sitting','Remaining']
    colors = ['Green','Blue','Yellow']
    explode = (0.1, 0, 0)

    fig, (ax2,ax4) = plt.subplots(nrows=2, figsize=(8,9.5))
    days = mdates.DayLocator()
    daysFmt = mdates.DateFormatter('%D')
    width = .9
    ax2.bar(bar_x, bar_y, width, color='green')
    ax2.bar(bar_x, bar_y2, width, color='blue', bottom=bar_y )
    ax2.set_title("Daily Standing Vs Sitting")
    ax2.set_ylabel("Hours")
    ax2.xaxis.set_major_locator(days)
    ax2.xaxis.set_major_formatter(daysFmt)
    ax2.legend(labels=['Standing','Sitting'])

    ax4.pie(pie_list, explode=explode, colors=colors, labels=pie_labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax4.legend(title='Hours', labels=pie_list)
    ax4.set_title("Today's Breakdown")

    fig.subplots_adjust(hspace=0.3)
    fig.tight_layout()
    plt.show()
