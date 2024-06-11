from flask import Flask, render_template, Response
from camera import Camera
from flask import request
from flask import send_from_directory,send_file
from makeup_artist import Makeup_artist

app = Flask(__name__)
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera,theme,glass,effect,bg):
    while True:
        frame = camera.get_frame(theme,glass,effect,bg)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    vid = request.args.get('id');
    path = "static/output/"+vid+".avi";
    return send_file(path, as_attachment=True)


@app.route('/video_feed')
def video_feed():
    theme = request.args.get('theme')
    glass = request.args.get('glass')
    effect = request.args.get('effect')
    vid = request.args.get('id')
    bg = request.args.get('bg')
    return Response(gen(Camera(Makeup_artist(), vid),theme,glass,effect,bg),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
