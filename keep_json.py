import json
import gkeepapi
#import urllib
import wget
import time
from datetime import datetime
from datetime import timezone
import datetime

from creds import username, password


# Date stuff
date_time_str = '2018-06-29 08:15:27.243860'
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')
print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
print('Date-time:', date_time_obj)



#i = 1
#while i < 6:
 # print(newtimestamp)
#  if i == 3:
#    break
#  i += 1



if __name__ == '__main__':

	# creating the Keep client
	keep = gkeepapi.Keep()

	# logging into the app account
	success = keep.login(username, password)

	# fetching all the available notes
	# notes = keep.all()
	notes = keep.find(archived=False, trashed=False, pinned=False) # Only get new ones

	#mostrecentnote = notes[0]
	#mostrecentnotetime = mostrecentnote.timestamps.created
	#print(mostrecentnotetime)


	json_data = []
	# creating a list with the json items; notes
	for note in notes:
		# Unix time
		# timestamp = filetime.replace(tzinfo=timezone.utc).timestamp()
		
		# print date
		#theidis = note.id
		#print(timestamp)
		
		#try:	
			#blob = note.images[0]
			#imagelink1 = keep.getMediaLink(blob)
			#filepath = '/www/wwwroot/www.yourdomain.com/files/gkeep/files2/'
			
			#Normal time
			#filename2 = filepath + filetimestring + '_2.png'
			#filename3 = filepath + filetimestring + '_3.png'
			
			#uncomment this to activate it ...
			#newtime = wget.download(imagelink1,filename1)
			#print(imagelink1)
			#print("deck"")
		#except:
			#print("No image!")
			#filename1 = None
		

		filetime = note.timestamps.created
		filetimestring = str(filetime)
		#filename1 = filepath + filetime + '_1.png'
		filename1 = filetimestring + '_1'
		print(filename1)
		note.archived = True
		#notes.add('Start_', True, gkeepapi.node.NewListItemPlacementValue.Top)

		
		# if len(note.labels) > 0:
		json_data.append({
			'created_at': str(note.timestamps.created),
			'title': note.title,
			'body': note.text,
			'tags': [keep.getLabel(label).name for label, val in list(note.labels._labels.items())] if len(note.labels) > 0 else [],
			# Remove array version
			#'images': [keep.getMediaLink(image) for image in note.images]
			'image1': filename1
	   })
           
     	
	# writing the keep notes to file named keep_notes.json
	with open('exported_json/keep_notes.json', 'w') as outfile:
		json.dump(json_data, outfile)
	
	keep.sync()	

		





	