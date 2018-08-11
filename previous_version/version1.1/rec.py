
from converter import Converter
from multiprocessing import Pool
import speech_recognition as sr  
import sys
import argparse
import subprocess
import os

"""
	@Aurthor: Bharath Sundar
	@version: 1.1
"""

class Generator:
	"""docstring for Generator"""
	def __init__(self,debug=False):
		self.count = 0
		self.t = 0
		self.debug = debug
	
	def _write_sub(self,file_name,subtitles):
		with open(file_name+".srt",'w') as file:
			file.write(subtitles)

		return True		

	def _get_chunks(self,file):
		cmd = "ffmpeg -i audio.wav -f segment -segment_time 5 -c copy parts/out%05d.wav"

		subprocess.call(cmd,shell=True)

		return True

	def _get_time(self,sec):
		m, s = divmod(sec, 60)
		h, m = divmod(m, 60)

		return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)


	def transribe(self,name):
		num = int(name[9:14])
		text = ''

		with open('api-key.json','r') as f:
				key = f.read()
		with sr.AudioFile(name) as source:
				audio = r.record(source)
		if self.arg.offline:
			try:
				text += r.recognize_sphinx(audio)

			except Exception as e:
				if self.debug:
					print(e)
				else:
					print("")
					print("try --help to know more about usage")

		else:
			#print(key)
			try:
				text += r.recognize_google_cloud(audio,credentials_json=key)

			except Exception as e:
				if self.debug:
					print(e)
				else:
					print("Check internet connection............."),
					print("try --offline to generate offline subtittles ")
		os.remove(name)
		return str(num)+','+text+"\n\n"




	def create_sub(self,name,arg):
		self.arg = arg
		self._get_chunks('audio.wav')
		files = os.listdir("parts/")
		files = ["parts/"+file for file in files]
		p = Pool(10)

		subs = p.map(self.transribe,files)
		subs = [e.split(',') for e in subs]
		subs = [[int(e[0]),e[1]] for e in subs]
		subs = sorted(subs)
		t = 0
		subtitles = ''
		#print(subs)
		for count,text in subs:
			subtitles += str(count) +"\n" +self._get_time(t)+" --> "
			t += 5
			subtitles += self._get_time(t) +"\n"
			subtitles += text

		self._write_sub(name,subtitles)
		return True

def main():
	debug = True
	parser = argparse.ArgumentParser()
	parser.add_argument('-o','--offline',help="used to generate subtitles offline",required=False)
	arg = parser.parse_args()

	g = Generator()
	g.create_sub('h',arg)


if __name__ == '__main__':
	r = sr.Recognizer()
	main()

