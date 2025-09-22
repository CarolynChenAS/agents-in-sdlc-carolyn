"""
Publisher model for the Tailspin Toys Crowd Funding platform.
This module defines the Publisher entity representing game publishers seeking crowdfunding.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Publisher(BaseModel):
    """
    Publisher model representing a game publisher on the crowdfunding platform.
    
    Attributes:
        id: Primary key identifier
        name: Publisher name (required, unique, min 2 characters)
        description: Publisher description (optional, min 10 characters if provided)
        games: Relationship to associated Game objects
    """
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # One-to-many relationship: one publisher has many games
    games = relationship("Game", back_populates="publisher")

    @validates('name')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validate the publisher name meets minimum length requirements.
        
        Args:
            key: The field name being validated
            name: The name value to validate
            
        Returns:
            str: The validated name
            
        Raises:
            ValueError: If name is invalid
        """
        return self.validate_string_length('Publisher name', name, min_length=2)

    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """
        Validate the publisher description meets minimum length requirements.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            str: The validated description
            
        Raises:
            ValueError: If description is invalid
        """
        return self.validate_string_length('Description', description, min_length=10, allow_none=True)

    def __repr__(self) -> str:
        """
        Return a string representation of the Publisher object.
        
        Returns:
            str: String representation showing publisher name
        """
        return f'<Publisher {self.name}>'

    def to_dict(self) -> dict:
        """
        Convert the Publisher object to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the publisher with game count
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'game_count': len(self.games) if self.games else 0
        }