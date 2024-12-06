from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    name = Column(String(100))
    age = Column(Integer)
    weight = Column(Float)
    height = Column(Float)
    
    workouts = relationship("Workout", back_populates="user")
    nutrition_logs = relationship("NutritionLog", back_populates="user")

class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String(50))
    duration = Column(Integer)  # in minutes
    intensity = Column(String(20))
    calories_burned = Column(Integer)
    date = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="workouts")

class NutritionLog(Base):
    __tablename__ = 'nutrition_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    food_name = Column(String(100))
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    date = Column(DateTime, default=datetime.now)
    
    user = relationship("User", back_populates="nutrition_logs")
