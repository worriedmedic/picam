#PiCamera Testbed

from time import sleep
import picamera
import os.path
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig()
import sys
import pygame
from pygame.locals import *
import subprocess

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
	if not os.path.exists('./images/' + now.strftime("%Y-%m") + '/' + now.strftime("%d")):
		os.makedirs('./images/' + now.strftime("%Y-%m") + '/' + now.strftime("%d"))

def image_display(n):
	img=pygame.image.load(n) 
	screen.blit(img,(0,0))
	pygame.display.flip()

def dropbox_update(output, output_dir):
	try:
		subprocess.call(["/usr/local/bin/dropbox_uploader.sh", "-q", "upload", "%s" %output, "/Programming/images/%s" %output_dir])
	except Exception:
		pass

def capture():
	with picamera.PiCamera() as camera:
		global output
		now = datetime.datetime.now()
		directorycheck()
		output = './images/' + now.strftime("%Y-%m") + '/' + now.strftime("%d") + '/' + 'image' + now.strftime("%Y-%m-%d--%H-%M-%S") + '.jpg'
		output_dir = now.strftime("%Y-%m") + '/' + now.strftime("%d") + '/'
		camera.iso = 1600
		camera.vflip = True
		camera.hflip = True
		camera.annotate_text = now.strftime("%Y-%m-%d %H:%M:%S")
		camera.capture('./images/output.jpg')
		camera.resolution = (480, 320)
		camera.capture(output)
		if verbose:
			print("Image Captured: ", output)
		image_display(output)
		dropbox_update(output, output_dir)

if (1):
	pygame.init()
	screen = pygame.display.set_mode((480,320),pygame.FULLSCREEN)
	scheduler = BlockingScheduler()
	scheduler.add_job(capture, 'interval', minutes=5)
	capture()
	scheduler.start()
