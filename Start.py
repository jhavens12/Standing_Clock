from appJar import gui
import datetime
import pickle
from pathlib import Path
from pprint import pprint
import history

time = datetime.datetime.now()

dictionary_file = Path('./History.dict')

if dictionary_file.is_file():
    pickle_in = open(dictionary_file,"rb")
    history_dict = pickle.load(pickle_in)
else:
    f=open(dictionary_file,"w+") #create file
    f.close()
    history_dict = {}

#find the last sit end time of the day (restart)
#OR if there is none(start of day) set it to 7:30

def initial_timer():
    global sit_end
    now = datetime.datetime.now()
    day_of_month = datetime.datetime(now.year, now.month, now.day)
    if day_of_month not in history_dict:
        sit_end = datetime.datetime(now.year, now.month, now.day, 7, 30)
    else:
        sit_end = sorted(list(history_dict[day_of_month].keys()))[-1]
        print(sit_end)

def update_label():
    global current_timer
    time = datetime.datetime.now()
    app.clearLabel('L1')
    app.setLabel('L1', time_format(time))

    #if sitting - there is a sit_start variable
    try:
        sit_start
    except NameError:
        pass
    else:
        if sit_start == None:
            pass
        else:
            app.clearLabel('L2')
            app.setLabel('L2', timedelta_format(time-sit_start))
            current_timer = time-sit_start

    #if standing - there is a sit_end variable
    try:
        sit_end
    except NameError:
        pass
    else:
        if sit_end == None:
            pass
        else:
            app.clearLabel('L2')
            app.setLabel('L2', timedelta_format(time-sit_end))
            current_timer = time-sit_end

def Sit(self):

    app.removeButton('B2') #remove the sit button
    app.addImageButton('B1', Stand, "./button_stand.gif", 4,1,2) #add stand button
    #app.setButton('B1', "STAND") #add stand button

    app.clearLabel('Title')
    app.setLabel('Title', 'You Are: Sitting')
    print("Sit Button Pressed")
    global sit_start
    global sit_end
    sit_start = datetime.datetime.now()
    app.clearLabel('L2')

    sit_end = None #reset sit_end - because we started sitting


def Stand(self):
    app.removeButton('B1') #remove the stand button
    app.addImageButton('B2', Sit, "./button_sit.gif", 4,1,2) #add sit button back

    app.clearLabel('Title')
    app.setLabel('Title', 'You Are: Standing')

    global sit_end
    global sit_start

    sit_end = datetime.datetime.now() #take time when timer stops
    app.clearLabel('L2') #clear the timer
    #app.setLabel('L2', 'Since: '+time_format(sit_end)) #display when sitting ended
    print("Stand button")

    app.clearLabel('L1')
    save_timer(sit_start,sit_end) #dump the sit_start and sit_end variables
    sit_start = None #reset sit_start

def save_timer(sit_start,sit_end):
    #data is saved with sit_end time as key, seconds sat as value
    difference = sit_end - sit_start
    now = datetime.datetime.now()
    day_of_month = datetime.datetime(now.year, now.month, now.day)

    if day_of_month not in history_dict:
        history_dict[day_of_month] = {}
        history_dict[day_of_month][sit_end] = difference
    else:
        history_dict[day_of_month][sit_end] = difference

    print()
    pprint(history_dict)
    print()

    #save to the history file
    with open(dictionary_file, 'w') as outfile:
        #json.dump(history_dict, outfile)
        pickle_out = open(dictionary_file,"wb")
        pickle.dump(history_dict, pickle_out)
        pickle_out.close()

def time_format(time):
    #return str(time.hour)+":"+str(time.minute)+":"+str(time.second)
    return str(time.time().strftime("%H:%M:%S"))

def timedelta_format(time):
    return time - datetime.timedelta(microseconds=time.microseconds)

def checkStop():
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")

def History(self):
    #os.system('python3 ./Display_History.py')
    history.build(history_dict)

initial_timer()

app = gui('Standing', '300x200')

app.setStopFunction(checkStop)
app.setPollTime(1000) #update every 1 second
app.setFont(size=36)
app.addLabel('Title','You Are: Standing', 1,1,2)
app.addLabel('L1', time, 2,1,2)
app.setLabelFg('L1', 'blue')
app.addLabel('L2', '', 3,1,2)
app.addButton('B3', History, 5,2,1)
app.setButton('B3','History')

app.addImageButton('B2', Sit, "./button_sit.gif", 4,1,2)

#app.hideTitleBar()
app.setLocation(0,0)
app.setResizable(canResize=False)
app.setTransparency(80)
app.setBg('white')
app.setFg('black')
app.setButtonFont(12)

app.registerEvent(update_label) #has program run the update

app.go()
