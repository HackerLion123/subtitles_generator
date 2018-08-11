
from converter import Converter
import subprocess
import os
import shutil
import sys

def extract_audio(loc):
    # cmd = "ffmpeg -i " + os.path.join(loc) + " -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # print(cmd)
    # subprocess.call(cmd,shell=True)

    c = Converter()

    conv = c.convert(os.path.join(loc),'aud.mp3',{'format':'mp3','audio':{'codec': 'mp3','bitrate':'22050','channels':1}})

    for timecode in conv:
    	pass
    cmd = "ffmpeg -loglevel quiet -i aud.mp3 -acodec pcm_s16le -ac 1 -ar 22050 out.wav -hide_banner"
    subprocess.call(cmd,shell=True)

    return "out.wav"


def progress(count, total, status=''):
    bar_len = 50
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))

    sys.stdout.flush()

def move_file(src,dest):
    pass


def merge_sub(video,sub):
	cmd = "ffmpeg -loglevel quiet -i " + os.path.join(video) + " -i " + sub + " -c copy -c:s mov_text out.mp4 -hide_banner"
	subprocess.call(cmd,shell=True)

	return True


