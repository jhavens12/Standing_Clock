from appJar import gui
import datetime
import pickle
from pathlib import Path
from pprint import pprint

dictionary_file = Path('./History.json')

if dictionary_file.is_file():
    pickle_in = open(dictionary_file,"rb")
    history_dict = pickle.load(pickle_in)

pprint(history_dict)
