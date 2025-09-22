"""
Base model class for the Tailspin Toys Crowd Funding platform.
This module provides the abstract base model with common validation methods
used across all database models.
"""
# filepath: server/models/base.py
from . import db

class BaseModel(db.Model):
    """
    Abstract base model class that provides common functionality for all models.
    
    This class includes validation methods that can be used by all model classes
    to ensure data integrity and consistent validation across the application.
    """
    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name: str, value: str, min_length: int = 2, allow_none: bool = False) -> str:
        """
        Validate that a string field meets minimum length requirements.
        
        Args:
            field_name: Name of the field being validated (used in error messages)
            value: The string value to validate
            min_length: Minimum required length (defaults to 2)
            allow_none: Whether None values are allowed (defaults to False)
            
        Returns:
            str: The validated string value
            
        Raises:
            ValueError: If validation fails (empty, wrong type, or too short)
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value