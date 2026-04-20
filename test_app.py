import pytest
from app import app, students

@pytest.fixture(autouse=True)
def reset_data():
    students.clear()
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test 1: Health check endpoint returns 200
def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


# Test 2: Get all students returns a list
def test_get_students(client):
    response = client.get('/api/students')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


# Test 3: Get a student that does not exist returns 404
def test_get_student_not_found(client):
    response = client.get('/api/students/9999')
    assert response.status_code == 404


# Test 4: POST a new student with valid data returns 201
def test_add_student(client):
    new_student = {'name': 'Memoona', 'grade': 'A'}
    response = client.post('/api/students', json=new_student)
    assert response.status_code == 201

    data = response.get_json()
    assert data['name'] == 'Memoona'
    assert 'id' in data


# Test 5: POST without required fields returns 400
def test_add_student_missing_field(client):
    response = client.post('/api/students', json={'name': 'Sara'})
    assert response.status_code == 400


# Test 6: Get existing student
def test_get_student_success(client):
    new_student = {'name': 'Ali', 'grade': 'B'}
    post_res = client.post('/api/students', json=new_student)
    student = post_res.get_json()

    response = client.get(f"/api/students/{student['id']}")
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Ali'