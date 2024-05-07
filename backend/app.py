import eventlet
import socketio
from checkers import *

sio = socketio.Server(cors_allowed_origins='http://localhost:3000')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

p1 = Player("B")
p2 = Player("R")
board = Board(p1, p2)

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('my event', {'data': 'foobar'})

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.on('request_move')
def another_event(sid, data):
    state = data["data"]
    turn = data["turn"]
    state, move, captured = board.request_move(state, turn)
    sio.emit("game_status", {'state': state, 'move': move, 'captured': captured})

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 6969)), app)