#PiCamera Testbed

from time import sleep
import picamera
import os.path
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()

def capture():
	with picamera.PiCamera() as camera:
		now = datetime.datetime.now()
		output_dir = '/home/pi/picamera/images/' + now.strftime("%Y-%m") + '/'
		output_file = 'image' + now.strftime("%H-%M-%S") + '.jpg'
		camera.iso = 1600
		camera.vflip = True
		camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
		camera.capture(output_dir + output_file, resize=(853, 480))
		camera.capture('/home/pi/picamera/images/output.jpg')

if (1):
	scheduler = BlockingScheduler()
	scheduler.add_job(capture, 'interval', seconds=30)
	scheduler.start()
