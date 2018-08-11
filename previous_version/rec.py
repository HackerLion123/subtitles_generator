
from converter import Converter
import speech_recognition as sr  
import sys
from multiprocessing import Pool
import argparse
import subprocess
import os

debug = True
r = sr.Recognizer()

parser = argparse.ArgumentParser()

parser.add_argument('-o','--offline',help="used to generate subtitles offline",required=False)

arg = parser.parse_args()

def write_sub(file_name,subtitles):
	with open(file_name,'w') as file:
		file.write(subtitles)

	return True



def get_chunks(file):
	cmd = "ffmpeg -i out.wav -f segment -segment_time 5 -c copy parts/out%05d.wav"

	subprocess.call(cmd,shell=True)

	return True


def get_time(sec):
	m, s = divmod(sec, 60)
	h, m = divmod(m, 60)

	return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)


def transribe(name):
	text = ''
	with sr.AudioFile(name) as source:
			audio = r.record(source)
	if arg.offline:
		try:
			text = r.recognize_sphinx(audio)

		except Exception as e:
			if debug:
				print(e)
			else:
				print("")
				print("try --help to know more about usage")

	else:
		with open('api-key.json','r') as f:
			key = f.read()

		#print(key)
		try:
			text = r.recognize_google_cloud(audio,credentials_json=key)

		except Exception as e:
			if debug:
				print(e)
			else:
				print("Check internet connection.............")
				print("try --offline to generate offline subtittles ")

	return text



def create_sub(arg):

	count = 1
	pool = 10
	t = 0	

	files = os.listdir("parts/")
	files = ["parts/"+file for file in files]


	for name in files:
		time = ''

		text = transribe(name)
		time += get_time(t)
		t += 5
		time += ' --> ' + get_time(t)
		print(time)
		print(text) 
		os.remove(name)
		count += 1


get_chunks('audio.wav')
create_sub(arg)


