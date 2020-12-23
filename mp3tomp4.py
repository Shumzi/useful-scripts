 # -*- coding: utf-8 -*-
import os
#get list of mp3 files
audioList = list(filter(lambda x: x.endswith(".mp3") or x.endswith(".wav") or x.endswith(".m4a"),os.listdir()))
# split into ביאור and קריאה
biurList = list(filter(lambda x: 'ביאור' in x, audioList))
kriyaList = list(filter(lambda x: 'קריאה' in x, audioList))

# make lists, make and send mp4 files to those folders.
if not os.path.exists('biyur'):
	os.mkdir('biyur')
if not os.path.exists('kriya'):
	os.mkdir('kriya')
# os.mkdir('video')
# for audio in audioList:
# 	os.system('ffmpeg -loop 1 -i <image> -i "'+ audio + '" -shortest -acodec copy "video/'+ audio[:-3] + 'mp4"')
for biyur in biurList:
	os.system('ffmpeg -loop 1 -i biyur.jpg -i "'+ biyur + '" -shortest -acodec copy "biyur/'+ biyur[:-3] + 'mp4"')
for kriya in kriyaList:
	os.system('ffmpeg -loop 1 -i kriya.jpg -i "'+ kriya + '" -shortest -acodec copy "kriya/'+ kriya[:-3] + 'mp4"')