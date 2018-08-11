
from converter import Converter
import subprocess
import speech_recognition as sr
import os

def extract_audio(loc):
    # cmd = "ffmpeg -i " + os.path.join(loc) + " -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # print(cmd)
    # subprocess.call(cmd,shell=True)

    c = Converter()

    conv = c.convert(os.path.join(loc),'aud.mp3',{'format':'mp3','audio':{'codec': 'mp3','bitrate':'22050','channels':1}})

    for timecode in conv:
    	pass
    cmd = "ffmpeg -i aud.mp3 -acodec pcm_s16le -ac 1 -ar 22050 out.wav"
    subprocess.call(cmd,shell=True)

    return True


def merge_sub(video,sub):
	cmd = "ffmpeg -i " + os.path.join(video) + " -i " + sub + " -c copy -c:s mov_text out.mp4"
	subprocess.call(cmd,shell=True)

	return True

def main():
    loc = input()

    extract_audio(loc)


if __name__ == '__main__':
    main()
