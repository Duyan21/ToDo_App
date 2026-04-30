from typing import Dict, Any
from werkzeug.security import generate_password_hash
from .base import ValidationError


class UserCreateDTO:
    """DTO for user registration/creation"""
    
    def __init__(self, data: Dict[str, Any] = None):
        self.name = None
        self.email = None
        self.password = None
        if data:
            self.name = data.get('name')
            self.email = data.get('email')
            self.password = data.get('password')
    
    def validate(self):
        """Custom validation for user creation"""
        # Type validation
        if not isinstance(self.name, str):
            raise ValidationError("Name must be a string")
        if not isinstance(self.email, str):
            raise ValidationError("Email must be a string")
        if not isinstance(self.password, str):
            raise ValidationError("Password must be a string")
        
        # Value validation
        if not self.name or len(self.name) < 2:
            raise ValidationError("Name must be at least 2 characters long")
        
        if not self.email or '@' not in self.email:
            raise ValidationError("Invalid email format")
        
        if not self.password or len(self.password) < 6:
            raise ValidationError("Password must be at least 6 characters long")
    
    def get_password_hash(self) -> str:
        """Generate password hash for storage"""
        return generate_password_hash(self.password)


class UserResponseDTO:
    """DTO for user response (excludes sensitive data)"""
    
    def __init__(self):
        self.id = None
        self.name = None
        self.email = None
        self.created_at = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_model(cls, user_model):
        """Create DTO from database model"""
        dto = cls()
        dto.id = user_model.id
        dto.name = user_model.name
        dto.email = user_model.email
        dto.created_at = user_model.created_at.isoformat() if user_model.created_at else None
        return dto
