from appJar import gui

from datetime import datetime

time = datetime.now()

def update_label():
    global current_timer
    time = datetime.now()
    app.clearLabel('L1')
    app.setLabel('L1',time)
    app.clearLabel('L2')

    try:
        stand_start
    except NameError:
        print ("No stand time")
    else:
        app.setLabel('L2', time-stand_start)
        current_timer = time-stand_start


def Stand(self):
    try:
        current_timer
    except NameError:
        print("No current timer to save")
    else:
        save_timer(current_timer)

    print("Stand Pressed")
    app.setButton('B1','SIT') #changes label to sit as you are now standing
    global stand_start
    stand_start = datetime.now()
    app.clearLabel('L2')
    app.setLabel('L2', stand_start)

def save_timer(current_timer):
    print()
    print("Timer Save Begin")
    print(current_timer)
    print()

app = gui('Standing' '480x320')
#app.setGeometry('fullscreen')


app.setPollTime(1000) #update every 1 second
app.setFont(36)
app.addLabel('L1', time, 1,1,2)
app.addLabel('L2', "Nothing", 2,1,2)
app.addButton('B1', Stand, 3,1,2)

app.setButtonFont(12)
app.setLabelFg('L1', 'blue')

app.registerEvent(update_label) #has program run the update



app.go()
