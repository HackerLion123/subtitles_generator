

from docopt import docopt
from converter import Converter
from multiprocessing import Pool
from helper import extract_audio,merge_sub,progress
import speech_recognition as sr  
import sys
import argparse
import subprocess 
import os
import tqdm

"""
	@Aurthor: Bharath Sundar
	@version: 1.1
"""

class Generator:
	"""docstring for Generator"""
	def __init__(self,debug=False):
		self.debug = debug
	
	def _write_sub(self,file_name,subtitles):
		with open(file_name+".srt",'w') as file:
			file.write(subtitles)

		return True		

	def _get_chunks(self,file):
		if not os.path.exists('./parts/'):
			os.makedirs('./parts/')
		cmd = "ffmpeg -loglevel quiet -i "+file+" -f segment -segment_time 5 -c copy parts/out%05d.wav -hide_banner"

		subprocess.call(cmd,shell=True)

		try:
			os.rmdir('/parts')
		except Exception as e:
			print(e)

		return True

	def _get_time(self,sec):
		m, s = divmod(sec, 60)
		h, m = divmod(m, 60)

		return "{:0>2d}:{:0>2d}:{:0>2d}".format(h, m, s)


	def transribe(self,name):

		num = int(name[9:14])
		text = ''

		with open('/root/PycharmProjects/Subs_geneartor/api-key.json','r') as f:
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
		self._get_chunks('out.wav')
		files = os.listdir("parts/")
		files = ["parts/"+file for file in files]
		self.total = len(files)
		p = Pool(10)
		subs = []
		for x in tqdm.tqdm(p.imap_unordered(self.transribe,files), total=len(files)):
			#os.system('clear')
			subs.append(x)
		subs = [e.split(',') for e in subs]
		subs = [[int(e[0]),e[1]] for e in subs]
		subs = sorted(subs)
		t = 0
		subtitles = ''
		#print(subs)
		for count,text in subs:
			progress(count,self.total,status='')
			subtitles += str(count) +"\n" +self._get_time(t)+" --> "
			t += 5
			subtitles += self._get_time(t) +"\n"
			subtitles += text

		self._write_sub(name,subtitles)
		os.remove('out.wav')
		return True

def parse_arguments():
	parser = argparse.ArgumentParser(description="Application to generate subtitles for any videos")
	parser.add_argument('filename',type=str)
	parser.add_argument('-o','--offline',help="used to generate subtitles offline",action='store_true',required=False)
	parser.add_argument('--version',action='store_true')
	parser.add_argument('--no-merge',action='store_true')
	parser.add_argument('-t')
	arg = parser.parse_args()
	return arg


def main():

	arg = parse_arguments()
	file_name = arg.filename
	file_name = file_name.split('/')
	if len(file_name) > 1:
		path = '/'.join(file_name[0:-1])
		print(path+'/')
		os.chdir(path)
		print(os.getcwd())
	extract_audio(file_name[-1])
	g = Generator(debug = True)
	g.create_sub(arg.filename,arg)


if __name__ == '__main__':
	r = sr.Recognizer()
	main()

