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




from creds import username, password


# Date stuff
date_time_str = '2018-06-29 08:15:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
print('---------Trail date below ...')
print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)
print('---------')


#i = 1
#while i < 6:
 # print(newtimestamp)
#  if i == 3:
#    break
#  i += 1

downloadfolder = '/www/wwwroot/www.yourdomain.com/files/exported_images/'
downloadurl = 'https://www.yourdomain.com/files/exported_images/' #Have to use a url below but would be better with a path

if __name__ == '__main__':

	# creating the Keep client
	keep = gkeepapi.Keep()

	# logging into the app account
	success = keep.login(username, password)

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
		filename1_url = downloadurl + filename1
		filename1_path = downloadfolder + filename1
		
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
				
				
		
	
	
	

	
		

		


		



		





	