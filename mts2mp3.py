"""
convert all mts files in folder to mp3, 
for uploading to castbox.
"""
import os
l = os.listdir()
for i in l:
	print(i)
	if(i[-4:].lower() == '.mts'):
		os.system('ffmpeg -i ' + i + ' -acodec libmp3lame -b:a 129K -vn ' + i + '.mp3')
 