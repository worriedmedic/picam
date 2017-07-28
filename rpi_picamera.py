#PiCamera Testbed

from time import sleep
import picamera
from PIL import Image
import os.path
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()

verbose = False

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

def capture():
	with picamera.PiCamera() as camera:
		now = datetime.datetime.now()
		directorycheck()
		output = './images/' + now.strftime("%Y-%m") + '/' + 'image' + now.strftime("%Y-%m-%d--%H-%M-%S") + '.jpg'
		camera.iso = 1600
		camera.vflip = True
		camera.hflip = True
		camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
		camera.capture('./images/output.jpg')
		camera.resolution = (853, 480)
		camera.capture(output)
		if verbose:
			print("Image Captured: ", output)
		im = Image.open(output)
		im.show()

if (1):
	scheduler = BlockingScheduler()
	scheduler.add_job(capture, 'interval', minutes=5)
	capture()
	scheduler.start()
