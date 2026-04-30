from datetime import datetime
from typing import Dict, Any, List


class NotificationResponseDTO:
    """DTO for notification response"""
    
    def __init__(self):
        self.id = None
        self.message = None
        self.type = None
        self.is_read = None
        self.created_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_model(cls, notification_model, now: datetime = None):
        """Create DTO from database model with dynamic message generation"""
        if now is None:
            now = datetime.now()
        
        # Determine if task is overdue
        is_overdue = (
            notification_model.task and 
            notification_model.task.deadline and 
            notification_model.task.deadline < now
        )
        
        dto = cls()
        dto.id = notification_model.id
        dto.is_read = notification_model.is_read
        dto.created_at = notification_model.created_at.isoformat() if notification_model.created_at else None
        
        # Generate dynamic message and type
        if is_overdue:
            dto.message = f"Task '{notification_model.task.title}' đã quá hạn"
            dto.type = "OVERDUE"
        else:
            dto.message = notification_model.message
            dto.type = notification_model.type
        
        return dto
    
    @classmethod
    def from_models_list(cls, notification_models: List, now: datetime = None) -> List:
        """Create list of DTOs from database models"""
        return [cls.from_model(notification, now) for notification in notification_models]
