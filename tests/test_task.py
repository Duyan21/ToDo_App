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



class TestCreateTaskAPI:
    """Test POST /api/task"""
    
    def test_create_task_not_authenticated(self, client):
        """Test task creation fails when not authenticated"""
        data = {
            'title': 'Test Task',
            'priority': 'High'
        }
        response = client.post('/api/task',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401


class TestGetTasksAPI:
    """Test GET /api/tasks"""
    
    def test_get_tasks_not_authenticated(self, client):
        """Test getting tasks fails when not authenticated"""
        response = client.get('/api/tasks')
        
        assert response.status_code == 401


class TestUpdateTaskAPI:
    """Test PUT /api/task/<id>"""
    
    def test_update_task_not_authenticated(self, client):
        """Test update fails when not authenticated"""
        data = {'status': 'Completed'}
        response = client.put('/api/task/1',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401


class TestEditTaskAPI:
    """Test PATCH /api/task/<id>"""
    
    def test_edit_task_not_authenticated(self, client):
        """Test edit fails when not authenticated"""
        data = {'title': 'Updated'}
        response = client.patch('/api/task/1',
                               data=json.dumps(data),
                               content_type='application/json')
        
        assert response.status_code == 401


class TestDeleteTaskAPI:
    """Test DELETE /api/task/<id>"""
    
    def test_delete_task_not_authenticated(self, client):
        """Test delete fails when not authenticated"""
        response = client.delete('/api/task/1')
        
        assert response.status_code == 401
