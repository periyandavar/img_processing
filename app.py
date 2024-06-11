from sys import stdout
from makeup_artist import Makeup_artist
import logging
from flask import Flask, render_template, Response,request
from flask_socketio import SocketIO
from camera import Camera
from utils import base64_to_pil_image, pil_image_to_base64
from flask import send_from_directory,send_file
import cv
import random
import string
idl=''
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(stdout))
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)
letters = string.ascii_lowercase
idl=''.join(random.choice(letters) for i in range(10))
camera={}
# def randomString(stringLength=10):
#     """Generate a random string of fixed length """
    
#     return 
camera[idl] = Camera(Makeup_artist(),idl)


@socketio.on('input image', namespace='/test')
def test_message(input):
    input = input.split(",")[1]
    camera[idl].enqueue_input(input)
    #camera.enqueue_input(base64_to_pil_image(input))


@socketio.on('connect', namespace='/test')
def test_connect():
    app.logger.info("client connected")

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    cv.clear();
    vid = request.args.get('id');
    path = "static/output/"+vid+".avi";
    return send_file(path, as_attachment=True)


@app.route('/')
def index():
    """Video streaming home page."""
    #return "welcome"
    return render_template('index.html',value=idl)


def gen(theme,glass,effect,bg,vid):
    """Video streaming generator function."""
    camera[idl].setid(vid)


    app.logger.info("starting to generate frames!")
    while True:
        frame = camera[idl].get_frame(theme,glass,effect,bg) #pil_image_to_base64(camera.get_frame())
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route('/video_feed/<val>')
def video_feed(val):
    theme = request.args.get('theme')
    glass = request.args.get('glass')
    effect = request.args.get('effect')
    vid = request.args.get('id')
    bg = request.args.get('bg')
    print(camera[idl].sid+" ")
    print(val+"\n")
    """Video streaming route. Put this in the src attribute of an img tag."""
    if(val==camera[idl].sid):
        return Response(gen(theme,glass,effect,bg,vid), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "welcome\n"+camera[idl].sid+"\n"+val


if __name__ == '__main__':
    socketio.run(app,port=5000, debug=True)
