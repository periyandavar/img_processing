import cv
import cv2
import threading
import binascii
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64


class Camera(object):
    def __init__(self, makeup_artist,id):
        self.to_process = []
        self.to_output = []
        self.makeup_artist = makeup_artist
        self.sid=id

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process_one(self):
        if not self.to_process:
            return

        # input is an ascii string. 
        input_str = self.to_process.pop(0)

        # convert it to a pil image
        input_img = base64_to_pil_image(input_str)

        ################## where the hard work is done ############
        # output_img is an PIL image
        

        # output_str is a base64 string in ascii
        

        # convert eh base64 string in ascii to base64 string in _bytes_
        self.to_output.append(input_img)

    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        self.to_process.append(input)
    def setid(self,vid):
        cv.setid(vid)

    def __del__(self):
        cv.clear();
    def get_frame(self,theme,glass,effect,bg):
        while not self.to_output:
            sleep(0.05)
        img=self.to_output.pop(0)
        output_img = cv.fun(img,theme,glass,effect,bg)
        output_str = pil_image_to_base64(output_img)
        return binascii.a2b_base64(output_str)
