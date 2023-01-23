import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Room, Canvas
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
# from flask_socketio import SocketIO, send, emit


app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
# socketio = SocketIO(app, cors_allowed_origins='*')


@app.get('/')
def home():
    return send_file('welcome.html')


@app.post('/login')
def login():
    data = request.json
    print('data is', data)
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'error': 'No account found'}), 404
    else:
        given_password = data['password']
        if user.password == given_password:
            access_token = create_access_token(identity=user.id)
            return jsonify({'user': user.toJSON(), 'token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid Password'}), 422


@app.post('/autologin')
@jwt_required()
def auto_login():
    current_user = get_jwt_identity()
    print('user_id is', current_user)

    user = User.query.get(int(current_user))

    if not user:
        return jsonify({'error': 'No account found'}), 404
    else:
        return jsonify(user.toJSON()), 200


@app.post('/users')
def create_user():
    data = request.json
    user = User(data['username'], data['email'],
                data['password'], data['avatarURL'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.toJSON()), 201


@app.get('/rooms/<name>')
def handle_get_room(name):
    # retrieve the room details from the database
    room = Room.query.filter_by(name=name).first()
    if room:
        return jsonify(room)
    else:
        return jsonify({"error": "Room not found"}), 404


@app.post('/rooms')
def create_room():
    data = request.json
    room = Room(data['name'], data['private'], data['occupied'])
    db.session.add(room)
    db.session.commit()
    return jsonify(room.toJSON()), 201


# @socketio.on('connect')
# def connected():
#     '''This function is an event listener that gets called when the client connects to the server'''
#     print(f'Client {request.sid} has connected')
#     emit('connect', {'data': f'id: {request.sid} is connected'})


# @socketio.on('data')
# def handle_message(data):
#     '''This function runs whenever a client sends a socket message to be broadcast'''
#     print(f'Message from Client {request.sid} : ', data)
#     emit('data', {'data': 'data', 'id': request.sid}, broadcast=True)


# @socketio.on("disconnect")
# def disconnected():
#     '''This function is an event listener that gets called when the client disconnects from the server'''
#     print(f'Client {request.sid} has disconnected')
#     emit('disconnect',
#          f'Client {request.sid} has disconnected', broadcast=True)


# @socketio.on('join')
# def handle_join(room_name):
#     join_room(room_name)
#     emit('join_success', {'message': f'Successfully joined room {room_name}'}, room=room_name)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3001))
