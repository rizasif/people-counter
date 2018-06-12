import cv2
import os
from shazam import Shazam
import datetime

SAMPLING_RATE = 1000

# VIDEO_NAME = "walking_deed_short.mp4"
VIDEO_NAME = "walking_deed.mp4"
# VIDEO_NAME = "test_sample.mp4"

def process_file(filename, sampling_rate):
	vidcap = cv2.VideoCapture(filename)
	mShazam = Shazam()

	success,image = vidcap.read()
	skip = 0
	while vidcap.isOpened():
		if skip % sampling_rate == 0:
			timestamp = vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
			# timestamp = vidcap.get(cv2.CAP_PROP_POS_MSEC)
			
			timestamp = str(datetime.timedelta(milliseconds=timestamp))
			print ("Processing Image at {}".format(timestamp))
			mShazam.ProcessImage(image, timestamp)
		
		skip += 1
		success,image = vidcap.read()
		if not success:
			break
	vidcap.release()
	mShazam.printResults()
	mShazam.saveResults()
	

if __name__ == "__main__":
	process_file("data/" + VIDEO_NAME, SAMPLING_RATE)