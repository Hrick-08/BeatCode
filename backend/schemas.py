from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    win_count: int
    loss_count: int
    rating: int
    created_at: datetime
    
    class Config:
        orm_mode = True


# Problem schemas
class ProblemResponse(BaseModel):
    id: int
    title: str
    description: str
    input_format: str
    output_format: str
    difficulty: str
    
    class Config:
        from_attributes = True

class ProblemDetail(ProblemResponse):
    test_cases: str

# Match schemas
class MatchCreate(BaseModel):
    player1_id: int
    player2_id: int
    problem_id: int

class MatchResponse(BaseModel):
    id: int
    player1_id: int
    player2_id: int
    problem_id: int
    winner_id: Optional[int]
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    
    class Config:
        from_attributes = True

# Submission schemas
class SubmissionCreate(BaseModel):
    match_id: int
    code: str
    language: str

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    match_id: int
    code: str
    language: str
    result: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True

# AI Review schemas
class AIReviewRequest(BaseModel):
    code: str
    problem_id: int
    language: str

class AIReviewResponse(BaseModel):
    score: float
    feedback: str
