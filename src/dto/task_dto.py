from datetime import datetime
from typing import Dict, Any, List, Optional
from .base import ValidationError


class TaskCreateDTO:
    """DTO for task creation"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.title = None
        self.description = None
        self.deadline = None
        self.priority = "Medium"
        self.reminder_minutes = 0
        
        if data:
            self.title = data.get('title')
            self.description = data.get('description')
            self.priority = data.get('priority', 'Medium')
            self.reminder_minutes = int(data.get('reminder_minutes', 0))
            
            deadline_str = data.get('deadline')
            if deadline_str:
                try:
                    self.deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M")
                except ValueError:
                    raise ValidationError("Invalid deadline format")
    
    def validate(self):
        """Custom validation for task creation"""
        if not self.title or len(self.title.strip()) == 0:
            raise ValidationError("Title is required")
        
        if self.priority not in ['Low', 'Medium', 'High']:
            raise ValidationError("Priority must be Low, Medium, or High")
        
        if self.reminder_minutes < 0:
            raise ValidationError("Reminder minutes cannot be negative")


class TaskUpdateDTO:
    """DTO for task updates"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.title = None
        self.description = None
        self.deadline = None
        self.priority = None
        self.status = None
        self.reminder_minutes = None
        
        if data:
            self.title = data.get('title')
            self.description = data.get('description')
            self.priority = data.get('priority')
            self.status = data.get('status')
            
            if 'reminder_minutes' in data:
                self.reminder_minutes = int(data['reminder_minutes'])
            
            deadline_str = data.get('deadline')
            if deadline_str:
                try:
                    self.deadline = datetime.strptime(deadline_str, "%Y-%m-%dT%H:%M")
                except ValueError:
                    raise ValidationError("Invalid deadline format")
    
    def validate(self):
        """Custom validation for task updates"""
        if self.priority and self.priority not in ['Low', 'Medium', 'High']:
            raise ValidationError("Priority must be Low, Medium, or High")
        
        if self.status and self.status not in ['Pending', 'Completed']:
            raise ValidationError("Status must be Pending or Completed")
        
        if self.reminder_minutes is not None and self.reminder_minutes < 0:
            raise ValidationError("Reminder minutes cannot be negative")


class TaskResponseDTO:
    """DTO for task response"""
    
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.deadline = None
        self.priority = None
        self.status = None
        self.reminder_minutes = None
        self.created_at = None
        self.completed_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'priority': self.priority,
            'status': self.status,
            'reminder_minutes': self.reminder_minutes,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_model(cls, task_model):
        """Create DTO from database model"""
        dto = cls()
        dto.id = task_model.id
        dto.title = task_model.title
        dto.description = task_model.description
        dto.deadline = task_model.deadline.isoformat() if task_model.deadline else None
        dto.priority = task_model.priority
        dto.status = task_model.status
        dto.reminder_minutes = task_model.reminder_minutes
        dto.created_at = task_model.created_at.isoformat() if task_model.created_at else None
        dto.completed_at = task_model.completed_at.isoformat() if task_model.completed_at else None
        return dto
    
    @classmethod
    def from_models_list(cls, task_models: List) -> List:
        """Create list of DTOs from database models"""
        return [cls.from_model(task) for task in task_models]
