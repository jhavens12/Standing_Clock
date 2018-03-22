import datetime
import pickle
from pathlib import Path
from pprint import pprint

now = datetime.datetime.now()

dictionary_file = Path('./History.dict')

if dictionary_file.is_file():
    pickle_in = open(dictionary_file,"rb")
    history_dict = pickle.load(pickle_in)

print("Time is now: "+str(now))
print()
print("1 - Today")
print("2 - Not Today")
print()

is_today = int(input("Is the addition today? "))

if is_today == 1:
    new_hour = int(input("What is the new hour? "))
    new_minute = int(input("What is the new minute? "))
    print()
    new_minutes = int(input("How many minutes are we adding? "))
    new_seconds = new_minutes*60
    new_entry = datetime.timedelta(0, new_seconds, 429745)
    new_timestamp = datetime.datetime(now.year, now.month, now.day, new_hour, new_minute)
    day_of_month = datetime.datetime(now.year, now.month, now.day)
else:
    new_year = int(input("What is the new year? "))
    new_month = int(input("What is the new month? "))
    new_day = int(input("What is the new day? "))
    new_hour = int(input("What is the new hour? "))
    new_minute = int(input("What is the new minute? "))
    print()
    new_minutes = int(input("How many minutes are we adding? "))
    new_seconds = new_minutes*60
    new_entry = datetime.timedelta(0, new_seconds, 429745)

    new_timestamp = datetime.datetime(new_year, new_month, new_day, new_hour, new_minute)
    day_of_month = datetime.datetime(new_year, new_month, new_day)

print(new_timestamp)
print(str(new_seconds)+" Seconds")



if day_of_month not in history_dict:
    history_dict[day_of_month] = {}
    history_dict[day_of_month][new_timestamp] = new_entry
else:
    history_dict[day_of_month][new_timestamp] = new_entry

pprint(history_dict[day_of_month])

with open(dictionary_file, 'w') as outfile:
    #json.dump(history_dict, outfile)
    pickle_out = open(dictionary_file,"wb")
    pickle.dump(history_dict, pickle_out)
    pickle_out.close()
