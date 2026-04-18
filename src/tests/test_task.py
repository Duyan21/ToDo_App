import pytest
import json
import datetime
from src.database.models import Task


class TestTaskPage:
    """Test task page rendering"""
    
    def test_task_page_not_authenticated(self, client):
        """Test /tasks page redirects when not authenticated"""
        response = client.get('/tasks', follow_redirects=False)
        assert response.status_code == 302  # Redirect


class TestTaskAPIAuthRequired:
    """Test all task API endpoints require authentication"""
    
    @pytest.mark.parametrize("method,path,data", [
        ('post', '/api/task', {'title': 'Test Task', 'priority': 'High'}),
        ('get', '/api/tasks', None),
        ('put', '/api/task/1', {'status': 'Completed'}),
        ('patch', '/api/task/1', {'title': 'Updated'}),
        ('delete', '/api/task/1', None),
    ])
    def test_endpoints_require_auth(self, client, method, path, data):
        """Test all task endpoints fail with 401 when not authenticated"""
        request_method = getattr(client, method)
        kwargs = {'content_type': 'application/json'} if method != 'get' else {}
        
        if data:
            kwargs['data'] = json.dumps(data)
        
        response = request_method(path, **kwargs)
        assert response.status_code == 401
