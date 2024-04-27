import cv2
import threading
import subprocess
from flask import Flask, render_template, Response

app = Flask(__name__)
app.static_folder = 'static'

phone_rtsp_url = 'rtsp://192.168.117.106:8554/live'  # 手机摄像头RTSP地址
paddle_out_rtsp_url = 'rtsp://localhost:8554/output'  # Paddle检测后输出的RTSP地址


def gen_frames(address):
    # 从摄影机逐帧生成
    camera = cv2.VideoCapture(address)
    while True:
        # 逐帧捕获
        success, frame = camera.read()  # 读取相机帧
        if not success:
            pass
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # 逐帧显示结果


def EmotionDetection():
    print('start')
    shell = ['python', 'D:/DesktopLink/Python/DBSE-monitor-master/EmotionDetection/notebook.py']
    subprocess.run(shell, stdout=subprocess.PIPE, shell=True)


def start():
    t = threading.Thread(target=EmotionDetection)
    t.daemon = True
    t.start()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/qianduan')
def qianduan():
    return render_template("qianduan.html")


@app.route('/houduan')
def houduan():
    return render_template("houduan.html")


@app.route('/shipinliu')
def shipinliu():
    return render_template("shipinliu.html")


@app.route('/native')
def native():
    return render_template("native.html")


@app.route('/flask')
def flask():
    return render_template("flask.html")


@app.route('/bijiben')
def bijiben():
    return render_template("bijiben.html")


@app.route('/shouji')
def shouji():
    return render_template("shouji.html")


@app.route('/suanfa')
def suanfa():
    # start()
    return render_template("suanfa.html")


@app.route('/video_feed_0')
def video_feed_0():
    return Response(gen_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_2')
def video_feed_2():
    return Response(gen_frames(phone_rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_3')
def video_feed_3():
    return Response(gen_frames(paddle_out_rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
