#PiCamera Testbed

from time import sleep
import picamera
import os.path
import os
import imageio
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()

def capture():
	with picamera.PiCamera() as camera:
		now = datetime.datetime.now()
		output_dir = '/home/pi/picamera/images/' + now.strftime("%Y-%m") + '/'
		output_file = 'image' + now.strftime("%H-%M-%S") + '.png'
		camera.iso = 1600
		camera.resolution = (1280, 720)
		camera.vflip = True
		camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
		camera.capture(os.path.join(output_dir, output_file))

if (1):
	scheduler = BlockingScheduler()
	scheduler.add_job(capture, 'interval', seconds=30)
	scheduler.start()
