from flask import Blueprint, request, jsonify
from extensions import db  # Assuming you have the SQLAlchemy db object defined somewhere
from models import User, Data, Plug, Attendance
from sqlalchemy import func
import datetime

main = Blueprint('main', __name__)

@main.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({'role': user.role})
    else:
        return jsonify({'error': 'Authentication failed'}), 401

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    index_number = data.get('index_number')
    fingerprint_id = data.get('fingerprint_id')
    
    new_user = User(name=name, email=email, password=password, role=role, index_number=index_number, fingerprintID=fingerprint_id)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'})

@main.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    fingerprint_id = data.get('fingerprint_id')
    
    user = User.query.filter_by(fingerprintID=fingerprint_id).first()
    if user:
        new_attendance = Attendance(index_number=user.index_number, time=datetime.datetime.now(), attended=True)
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance marked successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404
