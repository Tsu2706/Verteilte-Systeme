from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, JSON, Table
from database import Base
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint

class User(Base):
    """Benutzertabelle – hier könnt ihr weitere Felder ergänzen."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)


class Recipe(Base):
    # table for recipes -> ingredients and steps are safed as JSON
    __tablename__="recipes"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    title=Column(String(200),nullable=False)
    description=Column(String(200))
    ingredients=Column(JSON,nullable=False)
    steps=Column(JSON,nullable=False)
    is_public=Column(Boolean,default=True)
    created_at=Column(DateTime(timezone=True),server_default=func.now())


class Tag(Base):
    __tablename__="tags"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True,nullable=False)

# n:m Beziehung recipes <-> tags
recipe_tags=Table(
    "recipe_tags",
    Base.metadata,
    Column("recipe_id",ForeignKey("recipes.id"),primary_key=True),
    Column("tag_id",ForeignKey("tags.id"),primary_key=True)
)

class Rating(Base):
    __tablename__="ratings"

    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    recipe_id=Column(Integer,ForeignKey("recipes.id"),nullable=False)
    rating=Column(Integer,nullable=False)
    __table_args__=(
        CheckConstraint("rating >= 1 AND rating <= 5",name="rating_range"),
    )