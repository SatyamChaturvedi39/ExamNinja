from flask import Flask
from flask_pymongo import PyMongo
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

app.config["MONGO_URI"] = 'mongodb+srv://farrahman111:root@samurai.6l3x38m.mongodb.net/Examninja'
mongo = PyMongo(app)

@app.route('/')
def index():
    return "App with SocketIO and MongoDB is running"

if __name__ == '__main__':
    socketio.run(app, debug=True)
