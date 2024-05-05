import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='http://localhost:3000')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('my event', {'data': 'foobar'})

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.on('game_status')
def another_event(sid, data):
    print(data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 6969)), app)