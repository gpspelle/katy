from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("launch")
def launch():
    print(" [-] Received majelan")
    socketio.emit("launch_firework")

@socketio.on("connect")
def test_connect():
    print(" [.] Client connected")

@socketio.on("disconnect")
def test_disconnect():
    print(" [x] Client disconnected")

if __name__ == "__main__":
    socketio.run(app)
