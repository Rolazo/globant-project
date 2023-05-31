from main import app
import pytest
import io

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Recruiters Database' in response.data
    assert b'<a href="/upload" class="btn btn-primary btn-lg me-100">Upload Data</a>' in response.data
    

def test_upload_endpoint(client):
    response = client.get('/upload')
    assert response.status_code == 200
    assert b'Upload Data' in response.data
    assert b'<input type="file" class="form-control-file" id="csv_file" name="csv_file">' in response.data
    assert b'<input type="submit" class="btn btn-primary" value="Upload">' in response.data

def test_upload_endpoint(client):
    # Prepare a sample CSV file for testing
    # You can use the built-in StringIO module to create a file-like object from a string
    csv_data = "id,name,hire_datetime,department_id,job_id\n4000,John Doe,2021-01-01T00:00:00Z,1,1"
    csv_file = (io.BytesIO(csv_data.encode()), 'employees.csv')

    # Send a POST request with the CSV file
    response = client.post('/upload', data={'csv_file': csv_file})

    assert response.status_code == 200
    # assert b"Data uploaded successfully!" in response.data
    # Add more assertions to validate the database changes or other expected behavior
