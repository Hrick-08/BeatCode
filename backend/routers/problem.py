from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import json
import random

from database import get_db
from models import Problem
from schemas import ProblemResponse, ProblemDetail

router = APIRouter(
    prefix="/problems",
    tags=["Problems"],
    responses={404: {"description": "Not found"}}
)

@router.get("/random", response_model=ProblemResponse)
async def get_random_problem(db: Session = Depends(get_db)):
    problems = db.query(Problem).all()
    if not problems:
        # Create sample problems if none exist
        sample_problems = [
            Problem(
                title="Two Sum",
                description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                input_format="First line: array of integers\nSecond line: target integer",
                output_format="Two integers representing the indices",
                test_cases=json.dumps([
                    {"input": "[2,7,11,15]\n9", "output": "0 1"},
                    {"input": "[3,2,4]\n6", "output": "1 2"}
                ]),
                difficulty="easy"
            ),
            Problem(
                title="Reverse String",
                description="Write a function that reverses a string. The input string is given as an array of characters s.",
                input_format="Array of characters",
                output_format="Reversed array of characters",
                test_cases=json.dumps([
                    {"input": "['h','e','l','l','o']", "output": "['o','l','l','e','h']"},
                    {"input": "['H','a','n','n','a','h']", "output": "['h','a','n','n','a','H']"}
                ]),
                difficulty="easy"
            )
        ]
        
        for problem in sample_problems:
            db.add(problem)
        db.commit()
        problems = sample_problems
    
    return random.choice(problems)

@router.get("/{problem_id}", response_model=ProblemDetail)
async def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem
