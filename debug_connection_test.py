# Working! As of 2023-09-06
import gkeepapi
from config import USERNAME, PASSWORD

# This makes sure this is only run here and can not be run as an include in another file
if __name__ == '__main__':

    # creating the Keep client
    keep = gkeepapi.Keep()

    # logging into the app account
    success = keep.login(USERNAME, PASSWORD)

    # fetching all the available notes
    # notes = keep.all()
    # notes = keep.find(archived=False, trashed=False) # Only get new ones
    notes = keep.find(archived=False, trashed=False, pinned=False) #

    # Loop throught and just display timestamps for latest notes ... 
    for note in notes:
        filetime = note.timestamps.created
        print(filetime)
