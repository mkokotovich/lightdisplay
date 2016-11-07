# Stream Video with OpenCV from an Android running IP Webcam (https://play.google.com/store/apps/details?id=com.pas.webcam)
# Code Adopted from http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

import cv2
import urllib2
import numpy as np
import datetime


class ReadVideoStream(object):
    video_url = ""
    framerate_in_fpm = 0
    delta_between_frames = None
    time_for_next_frame = None
    stream = None
    stream_buffer = ''
    # cv2 flags are not exposed to python?
    MISSING_CV_LOAD_IMAGE_COLOR = 1

    def __init__(self, video_url, framerate_in_fpm=60):
        self.video_url = video_url
        self.delta_between_frames = datetime.timedelta(milliseconds=(1000*int(framerate_in_fpm/60)))

    def connect_to_stream(self):
        print 'Opening stream to {}'.format(self.video_url)
        self.stream = urllib2.urlopen(self.video_url)
        print 'Connection established'
        self.time_for_next_frame = datetime.datetime.now()

    def read_and_block_until_next_image(self):
        image = None
        while image == None:
            image = self.read_next_buffer()
        return image

    def read_next_buffer(self):
        image = None
        if self.stream == None:
            print "Stream has not been connected"
            exit(1)
        self.stream_buffer += self.stream.read(1024)
        # If it isn't time for the next frame, just drop the data and return
        if datetime.datetime.now() < self.time_for_next_frame:
            self.stream_buffer=''
            return None
        a = self.stream_buffer.find('\xff\xd8')
        b = self.stream_buffer.find('\xff\xd9')
        print "a: {}  b: {}".format(a, b)
        if a == -1:
            print "could not find beginning of image (a={}), dropping bytes".format(a)
            self.stream_buffer=''
        elif b == -1:
            print "Found beginning of image ({}) but no end, read more".format(a)
        elif b < a:
            print "Need to align stream to beginning of image (a={})".format(a)
            self.stream_buffer = self.stream_buffer[a:]
        else:
            print "Found image: a({}) and b({})".format(a,b)
            self.time_for_next_frame = datetime.datetime.now() + self.delta_between_frames
            jpg = self.stream_buffer[a:b+2]
            self.stream_buffer= self.stream_buffer[b+2:]
            #image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), self.MISSING_CV_LOAD_IMAGE_COLOR)
            # Could this work?
            image = jpg
        return image


class DisplayVideo(object):
    caption = ""

    def __init__(self, caption="Video"):
        self.caption = caption

    def handle_image(self, image):
        cv2.imshow(self.caption, image)
        if cv2.waitKey(1) == 27:
            exit(0)

class WriteVideo(object):
    file_format = ""
    image_num = 0

    def __init__(self, file_format="output_image"):
        self.file_format == file_format
        self.image_num = 0

    def handle_image(self, image):
        filename = "{}_{}.jpg".format(self.file_format, self.image_num)
        with open(filename, "wb") as outfile:
            outfile.write(str(image))



class DisplayVideoStream(object):
    video_reader = None
    displayer = None

    def __init__(self, video_url, framerate_in_fpm):
        self.video_reader = ReadVideoStream(video_url, framerate_in_fpm)
        self.displayer = WriteVideo()

    def read_stream_and_display(self):
        self.video_reader.connect_to_stream()
        while True:
            image = self.video_reader.read_and_block_until_next_image()
            self.displayer.handle_image(image)



if __name__ == "__main__":
    import sys
    host = "192.168.86.106:8080"
    if len(sys.argv)>1:
        host = sys.argv[1]

    hoststr = 'http://' + host + '/video'

# Framerate in frames per minute
    framerate = 60

    display = DisplayVideoStream(hoststr, framerate)
    display.read_stream_and_display()
