#PiCamera Testbed
#crontab -e example:
#export DISPLAY=:0 && <<COMMAND>>

from time import sleep
import picamera
import os.path
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import sys
import dropbox

verbose = False

logging.basicConfig()
dbx = dropbox.Dropbox(dropbox_API_key)

for arg in sys.argv:
	if arg == '-v':
		verbose = True
		print("VERBOSE is ON")

def directorycheck():
	now = datetime.datetime.now()
	if not os.path.exists('./images/'):
		os.makedirs('./images/')
	if not os.path.exists('./images/' + now.strftime("%Y-%m")):
		os.makedirs('./images/' + now.strftime("%Y-%m"))

def dropbox_update(output, output_dir):
	try:
		with open(output, 'rb') as f:
			dbx.files_upload(f.read(), '/Programming/images/%s' %output_dir)
	except Exception:
		pass

def capture():
	with picamera.PiCamera() as camera:
		global output, output_dir
		now = datetime.datetime.now()
		directorycheck()
		output_file_name = 'image' + now.strftime("%Y-%m-%d_%H%MHRS") + '.jpg'
		output = './images/' + now.strftime("%Y-%m") + '/' + output_file_name
		output_dir = now.strftime("%Y-%m") + '/' + output_file_name
		camera.iso = 1600
		camera.led = False
		camera.annotate_text = now.strftime("%Y-%m-%d %H%MHRS")
		camera.capture('./images/output.jpg')
		camera.resolution = (1280, 720)
		camera.capture(output, resize=(640, 360))
		if verbose:
			print("Image Captured: ", output)
		dropbox_update(output, output_dir)

if (1):
	scheduler = BlockingScheduler()
	scheduler.add_job(capture, 'cron', hour=8)
	scheduler.add_job(capture, 'cron', hour=12)
	scheduler.add_job(capture, 'cron', hour=18)
	capture()
	scheduler.start()
