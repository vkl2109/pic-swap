import os
from flask import Flask, send_file, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db, User, Room, Canvas
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_socketio import SocketIO, send, emit


app = Flask(__name__, static_folder='public')
CORS(app, origins=['*'])
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, cors_allowed_origins='*')


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


@app.post('/postimage')
@jwt_required()
def postimage():
    data = request.json
    room = Room.query.get(data['id'])
    current_user = User.query.get(get_jwt_identity())
    if current_user.sid == room.player_sid:
        room.playerURI = data['uri']
        # print(data['uri'])
        room.playerBool = not room.playerBool
        db.session.commit()
    elif current_user.sid == room.host_sid:
        room.hostURI = data['uri']
        print(data['uri'])
        room.hostBool = not room.hostBool
        db.session.commit()
    else:
        print('session id not found: ' + current_user.sid)
    if room.hostBool == room.playerBool:
        socketio.emit('upload_success', {
            'message': f'{room.id}'}, room=room.host_sid)
        socketio.emit('upload_success', {
            'message': f'{room.id}'}, room=room.player_sid)
        return {"message":"refresh"}, 201
    db.session.commit()
    return {"message":"don't refresh"}, 201


@app.post('/getimage')
@jwt_required()
def getimage():
    data = request.json
    room = Room.query.get(data['id'])
    current_user = User.query.get(get_jwt_identity())
    if current_user.sid == room.player_sid:
        return jsonify(room.hostURI), 201
    elif current_user.sid == room.host_sid:
        return jsonify(room.playerURI), 201
    else:
        return { 'error':'no ID found'}, 404
    

@app.post('/rooms/<name>')
@jwt_required()
def join_private_room(name):
    room = Room.query.filter_by(room_name=name).first()
    current_user = User.query.get(get_jwt_identity())
    room.player_sid = current_user.sid
    db.session.commit()
    socketio.emit('join_success', {
        'message': f'{room.id}'}, room=room.host_sid)
    socketio.emit('join_success', {
        'message': f'{room.id}'}, room=current_user.sid)
    return jsonify(room.toJSON()), 201


@app.post('/rooms')
@jwt_required()
def create_room():
    data = request.json

    if Room.query.filter_by(room_name=data['name']).first():
        return jsonify('Name taken'), 403

    current_user = User.query.get(get_jwt_identity())
    host_sid = current_user.sid
    room = Room(data['name'], data['private'], host_sid)
    db.session.add(room)
    db.session.commit()
    return jsonify(room.toJSON()), 201


@app.post('/rooms/<int:id>')
@jwt_required()
def join_public_room(id):
    room = Room.query.filter_by(id=id).first()
    current_user = User.query.get(get_jwt_identity())
    room.player_sid = current_user.sid
    db.session.commit()
    socketio.emit('join_success', {
        'message': f'{room.id}'}, room=room.host_sid)
    socketio.emit('join_success', {
        'message': f'{room.id}'}, room=current_user.sid)
    return jsonify(room.toJSON()), 201


@app.get('/rooms')
def show_rooms():
    rooms = Room.query.all() or []
    print(rooms)
    return jsonify([r.toJSON() for r in rooms])


@socketio.on('connect')
@jwt_required()
def connected():
    current_user = User.query.get(get_jwt_identity())
    current_user.sid = request.sid
    db.session.commit()
    emit('connect', {'data': f'id: {request.sid} is connected'})


@socketio.on('data')
def handle_message(data):
    '''This function runs whenever a client sends a socket message to be broadcast'''
    print(f'Message from Client {request.sid} : ', data)
    emit('data', {'data': 'data', 'id': request.sid}, broadcast=True)

    print(jsonify(request.data))

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
    app.run(host='127.0.0.1', port=os.environ.get('PORT', 3001), debug=True)
