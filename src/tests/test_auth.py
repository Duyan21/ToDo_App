import pytest
import json
from src.database.models import User


class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_register_page(self, client):
        """Test GET /register renders page"""
        response = client.get('/register')
        assert response.status_code == 200
    
    def test_signin_page(self, client):
        """Test GET /signin renders page"""
        response = client.get('/signin')
        assert response.status_code == 200
    
    def test_signin_page_root(self, client):
        """Test GET / renders signin page"""
        response = client.get('/')
        assert response.status_code == 200


class TestRegisterAPI:
    """Test POST /api/register"""
    
    def test_register_success(self, client):
        """Test successful registration"""
        data = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'Password123'
        }
        response = client.post('/api/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'message' in result
        
        # Verify user created
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.name == 'New User'
    
    def test_register_missing_fields(self, client):
        """Test registration fails with missing fields"""
        data = {'name': 'Test'}  # Missing email and password
        response = client.post('/api/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration fails with duplicate email"""
        data = {
            'name': 'Another User',
            'email': 'test@example.com',
            'password': 'Password123'
        }
        response = client.post('/api/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
    
    @pytest.mark.parametrize("invalid_data,error_msg", [
        ({'name': 123, 'email': 'test@example.com', 'password': 'Password123'}, 'phải là str'),
        ({'name': 'Test', 'email': 'invalid-email', 'password': 123}, 'phải là str'),
    ])
    def test_register_invalid_types(self, client, invalid_data, error_msg):
        """Test registration fails with invalid field types"""
        response = client.post('/api/register',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result


class TestSigninAPI:
    """Test POST /api/signin"""
    
    def test_signin_success(self, client, test_user):
        """Test successful signin"""
        data = {
            'email': 'test@example.com',
            'password': 'Test123456'
        }
        response = client.post('/api/signin',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = json.loads(response.data)
        assert 'message' in result
    
    @pytest.mark.parametrize("missing_data,expected_field", [
        ({'email': 'test@example.com'}, 'password'),
        ({'password': 'Password123'}, 'email'),
    ])
    def test_signin_missing_fields(self, client, missing_data, expected_field):
        """Test signin fails with missing fields"""
        response = client.post('/api/signin',
                             data=json.dumps(missing_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
    
    def test_signin_wrong_email(self, client):
        """Test signin fails with non-existent email"""
        data = {
            'email': 'nonexistent@example.com',
            'password': 'Password123'
        }
        response = client.post('/api/signin',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
    
    def test_signin_wrong_password(self, client, test_user):
        """Test signin fails with wrong password"""
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = client.post('/api/signin',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result
    
    @pytest.mark.parametrize("invalid_data", [
        {'email': 123, 'password': 'Password123'},
        {'email': 'test@example.com', 'password': 123},
    ])
    def test_signin_invalid_types(self, client, invalid_data):
        """Test signin fails with invalid field types"""
        response = client.post('/api/signin',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = json.loads(response.data)
        assert 'error' in result


class TestLogoutAPI:
    """Test POST /api/logout"""
    
    def test_logout_not_authenticated(self, client):
        """Test logout fails when not authenticated"""
        response = client.post('/api/logout',
                             content_type='application/json')
        
        assert response.status_code == 401
