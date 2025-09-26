"""
Game model for the Tailspin Toys Crowd Funding platform.
This module defines the Game entity with its relationships to publishers and categories.
"""
from . import db
from .base import BaseModel
from sqlalchemy.orm import validates, relationship

class Game(BaseModel):
    """
    Game model representing a crowdfunding game project.
    
    Attributes:
        id: Primary key identifier
        title: Game title (required, min 2 characters)
        description: Game description (required, min 10 characters)
        star_rating: User rating (optional, float value)
        category_id: Foreign key to category
        publisher_id: Foreign key to publisher
        category: Relationship to Category model
        publisher: Relationship to Publisher model
    """
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    star_rating = db.Column(db.Float, nullable=True)
    
    # Foreign keys for one-to-many relationships
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.id'), nullable=False)
    
    # One-to-many relationships (many games belong to one category/publisher)
    category = relationship("Category", back_populates="games")
    publisher = relationship("Publisher", back_populates="games")
    
    @validates('title')
    def validate_name(self, key: str, name: str) -> str:
        """
        Validate the game title meets minimum length requirements.
        
        Args:
            key: The field name being validated
            name: The title value to validate
            
        Returns:
            str: The validated title
            
        Raises:
            ValueError: If title is invalid
        """
        return self.validate_string_length('Game title', name, min_length=2)
    
    @validates('description')
    def validate_description(self, key: str, description: str) -> str:
        """
        Validate the game description meets minimum length requirements.
        
        Args:
            key: The field name being validated
            description: The description value to validate
            
        Returns:
            str: The validated description
            
        Raises:
            ValueError: If description is invalid
        """
        if description is not None:
            return self.validate_string_length('Description', description, min_length=10, allow_none=True)
        return description
    
    def __repr__(self) -> str:
        """
        Return a string representation of the Game object.
        
        Returns:
            str: String representation showing title and ID
        """
        return f'<Game {self.title}, ID: {self.id}>'

    def to_dict(self) -> dict:
        """
        Convert the Game object to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the game with publisher and category info
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'publisher': {'id': self.publisher.id, 'name': self.publisher.name} if self.publisher else None,
            'category': {'id': self.category.id, 'name': self.category.name} if self.category else None,
            'starRating': self.star_rating  # Changed from star_rating to starRating
        }