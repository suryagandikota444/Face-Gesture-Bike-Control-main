# from flask import Flask, request,jsonify
# from flask_socketio import SocketIO,emit
# from flask_cors import CORS
# from time import sleep
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

i = 0
@app.route('/indicator')
def indicator():
   with open("indicator.txt") as f:
    firstline = f.readline().rstrip()
   return firstline

@app.route('/headlight')
def headlight():
   with open("headlight.txt") as f:
    firstline = f.readline().rstrip()
   return firstline

if __name__ == '__main__':
   app.run(host="0.0.0.0",debug=True)

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# CORS(app,resources={r"/*":{"origins":"*"}})
# socketio = SocketIO(app,cors_allowed_origins="*")
# print("running")
# @app.route("/http")
# def http_call():
#     """return JSON with string data as the value"""
#     data = {'data':'This text was fetched using an HTTP call to server on render'}
#     return jsonify(data)

# @socketio.on("connect")
# def connected():
#     """event listener when client connects to the server"""
#     print(request.sid)
#     print("client has connected")
#     while 1:
#         emit("connect",{"data":f"id: {request.sid} is connected"})
#         sleep(1)

# @socketio.on('data')
# def handle_message(data):
#     """event listener when client types a message"""
#     print("data from the front end: ",str(data))
#     emit("data",{'data':data,'id':request.sid},broadcast=True)

# @socketio.on("disconnect")
# def disconnected():
#     """event listener when client disconnects to the server"""
#     print("user disconnected")
#     emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


# if __name__ == '__main__':
#     socketio.run(app, debug=True)