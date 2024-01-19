from flask import Flask, render_template, Response
import cv2
import vskomain

app = Flask(__name__)

camera = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
def gen_frames():
    while True:
        success, frame = camera.read()
        height,width = frame.shape[0:2]
        if not success:
            break
        else:
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)
            eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
    
            cv2.rectangle(frame, (0,height-50),(200,height),(0,0,0),thickness=cv2.FILLED)
    
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,pt1=(x,y),pt2=(x+w,y+h), color= (255,0,0), thickness=3)
        
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/run-script')

def run_script():
    # return Response(vskomain.open_camera(),mimetype='multipart/x-mixed-replace; boundary=frame')
    res = vskomain.abc()
    return res

if __name__ == '__main__':
    app.run(debug=True)
