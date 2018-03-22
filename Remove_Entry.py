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

is_today = int(input("Is the removal today? "))
print()
day_of_month = datetime.datetime(now.year, now.month, now.day)
choice_dict = {}
if is_today == 1:
    for n,entry in enumerate(sorted(history_dict[day_of_month])):
        print(str(n)+" - "+str(entry)+" - "+str(history_dict[day_of_month][entry]))
        choice_dict[n] = entry
else:
    pprint(history_dict)
print()
user_input = input("What number(s) to remove? (enter separated by comma) ")

input_list = user_input.split(',')
numbers = [int(x.strip()) for x in input_list]

for number in numbers:
    print("Removing " + str(choice_dict[number]))
    del history_dict[day_of_month][choice_dict[number]]

print()
print("Remaining Entries: ")
pprint(history_dict)

with open(dictionary_file, 'w') as outfile:
    #json.dump(history_dict, outfile)
    pickle_out = open(dictionary_file,"wb")
    pickle.dump(history_dict, pickle_out)
    pickle_out.close()
