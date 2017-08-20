#PiCamera Testbed
#crontab -e example:
#export DISPLAY=:0 && <<COMMAND>>

from time import sleep
import picamera
import os.path
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()
import sys

verbose = False

for arg in sys.argv:
	if arg == '-v':
		verbose = True
		print("VERBOSE is ON")

def directorycheck():
	now = datetime.datetime.now()
	if not os.path.exists('/home/pi/picam/images/'):
		os.makedirs('/home/pi/picam/images/')
	if not os.path.exists('/home/pi/picam/images/' + now.strftime("%Y-%m")):
		os.makedirs('/home/pi/picam/images/' + now.strftime("%Y-%m"))

def dropbox_update(output, output_dir):
	try:
		subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "upload", "%s" %output, "/Programming/images/%s" %output_dir])
	except Exception:
		pass

def capture():
	with picamera.PiCamera() as camera:
		global output, output_dir
		now = datetime.datetime.now()
		directorycheck()
		output = '/home/pi/picam/images/' + now.strftime("%Y-%m") + '/' + 'image' + now.strftime("%Y-%m-%d--%H-%M-%S") + '.jpg'
		output_dir = now.strftime("%Y-%m") + '/'
		camera.iso = 1600
		camera.led = False
		camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
		camera.capture('/home/pi/picam/images/output.jpg')
		camera.resolution = (480, 320)
		camera.capture(output)
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
