from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

students = []
next_id = 1


@app.route('/api/health', methods=["GET"])
def health():
    return jsonify({'status': 'ok', 'message': 'flask is running'}), 200


@app.route('/api/students', methods=["GET"])
def get_students():
    return jsonify(students), 200


@app.route('/api/students/<int:student_id>', methods=["GET"])
def get_student(student_id):
    s = next((s for s in students if s['id'] == student_id), None)
    if not s:
        return jsonify({'error': 'not found'}), 404
    return jsonify(s), 200


@app.route('/api/students', methods=["POST"])
def add_student():
    global next_id
    data = request.get_json()

    if not data or 'name' not in data or 'grade' not in data:
        return jsonify({'error': 'name and grade required'}), 400

    student = {
        'id': next_id,
        'name': data['name'],
        'grade': data['grade']
    }

    students.append(student)
    next_id += 1

    return jsonify(student), 201


if __name__ == '__main__':
    app.run(debug=True)
