from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    win_count = Column(Integer, default=0)
    loss_count = Column(Integer, default=0)
    rating = Column(Integer, default=1200)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player1_matches = relationship("Match", foreign_keys="Match.player1_id", back_populates="player1")
    player2_matches = relationship("Match", foreign_keys="Match.player2_id", back_populates="player2")
    submissions = relationship("Submission", back_populates="user")

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    input_format = Column(Text, nullable=False)
    output_format = Column(Text, nullable=False)
    test_cases = Column(Text, nullable=False)  # JSON string
    difficulty = Column(String(20), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", back_populates="problem")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    code_player1 = Column(Text, nullable=True)
    code_player2 = Column(Text, nullable=True)
    ai_score_p1 = Column(Float, nullable=True)
    ai_score_p2 = Column(Float, nullable=True)
    status = Column(String(20), default="active")  # active, completed, cancelled
    
    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id], back_populates="player1_matches")
    player2 = relationship("User", foreign_keys=[player2_id], back_populates="player2_matches")
    problem = relationship("Problem", back_populates="matches")
    submissions = relationship("Submission", back_populates="match")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    code = Column(Text, nullable=False)
    language = Column(String(20), nullable=False)
    result = Column(String(20), nullable=True)  # accepted, wrong_answer, time_limit, etc.
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    match = relationship("Match", back_populates="submissions")
