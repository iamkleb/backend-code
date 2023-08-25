from flask import Blueprint, request, jsonify
from .extensions import db
from .models import User, Attendance
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
    course_name = data.get('course_name')
    
    user = User.query.filter_by(fingerprintID=fingerprint_id).first()
    if user:
        new_attendance = Attendance(index_number=user.index_number, time=datetime.datetime.now(), attended=True, course_name=course_name)
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance marked successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

@main.route('/lecturers/attendance', methods=['GET'])
def get_students_attendance_for_lecturer():
    attendance_data = db.session.query(Attendance.time, User.name, User.index_number, Attendance.course_name).\
        join(User, User.index_number == Attendance.index_number).\
        filter(User.role == 'student').all()
    
    result = []
    for time, name, index_number, course_name in attendance_data:
        result.append({
            'time': time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string format
            'student_name': name,
            'student_index_number': index_number,
            'course_name': course_name
        })
    
    return jsonify({'attendance': result})

@main.route('/students/attendance', methods=['POST'])
def get_student_attendance():
    data = request.get_json()
    student_index_number = data.get('index_number')
    
    student = User.query.filter_by(index_number=student_index_number, role='student').first()
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    
    attendance_data = Attendance.query.filter_by(index_number=student.index_number).all()
    
    result = []
    for attendance in attendance_data:
        result.append({
            'time': attendance.time.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string format
            'course_name': attendance.course_name
        })
    
    return jsonify({'attendance': result})
