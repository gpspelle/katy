import socketio
import time

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000/katy')

for i in range(10):
    sio.emit("launch")
    time.sleep(1)

