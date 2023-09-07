# One issue is that this only will get one of the attachements ... only targets first, I think ...
import io
import os
import json
import shutil

import gkeepapi
import requests
import PIL.Image as Image
from datetime import datetime

# Reess added these 
import time
from datetime import timezone
#import urllib
import datetime
import wget


from config import USERNAME, PASSWORD, JSON_DIRECTORY, DOWNLOAD_URL, DOWNLOAD_FOLDER


if __name__ == '__main__':

	# creating the Keep client
	keep = gkeepapi.Keep()

	# logging into the app account
	success = keep.login(USERNAME, PASSWORD)

	# fetching all the available notes
	# notes = keep.all()
	# notes = keep.find(archived=False, trashed=False) # Only get new ones
	notes = keep.find(archived=False, trashed=False, pinned=False) #

	# creating a list with the json items; notes
	for note in notes:
		filetime = note.timestamps.created
		# must make time back into string for it to work
		filetimestring = str(filetime)
		filename1 = filetimestring + '_1.png'
		filename1_url = DOWNLOAD_URL + filename1
		filename1_path = DOWNLOAD_FOLDER + filename1
		
		# print(filename1_path)
		response = requests.get(filename1_url)
		
		if response.status_code == 200:
			status = 'Image already downloaded'
			print(status)
		else:
			status = 'New image ...'
			print(status)
			try:
				blob = note.images[0]
				keepimagelink = keep.getMediaLink(blob)
				wget.download(keepimagelink,filename1_path)
			except:
				keepimagelink = ''
			finally: 
				print('----')
				
				
		
	
	
	

	
		

		


		



		





	