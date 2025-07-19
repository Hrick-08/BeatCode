from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import json
import asyncio
import random

from database import get_db
from models import User, Match, Problem, Submission
from schemas import MatchCreate, MatchResponse, SubmissionCreate
from routers.auth import get_current_user
from services.judge0 import submit_code_to_judge0

router = APIRouter(
    prefix="/matches",
    tags=["Matches"],
    responses={404: {"description": "Not found"}}
)

# Simple in-memory matchmaking queue
matchmaking_queue = []

@router.post("/matchmaking/join")
async def join_matchmaking(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if user is already in queue
    if current_user.id in matchmaking_queue:
        return {"message": "Already in queue", "position": matchmaking_queue.index(current_user.id) + 1}
    
    matchmaking_queue.append(current_user.id)
    
    # If we have 2 players, create a match
    if len(matchmaking_queue) >= 2:
        player1_id = matchmaking_queue.pop(0)
        player2_id = matchmaking_queue.pop(0)
        
        # Get random problem
        problem = db.query(Problem).order_by(Problem.id).first()
        if not problem:
            # Create a sample problem if none exists
            sample_problem = Problem(
                title="Two Sum",
                description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                input_format="First line: array of integers\nSecond line: target integer",
                output_format="Two integers representing the indices",
                test_cases=json.dumps([
                    {"input": "[2,7,11,15]\n9", "output": "0 1"},
                    {"input": "[3,2,4]\n6", "output": "1 2"}
                ]),
                difficulty="easy"
            )
            db.add(sample_problem)
            db.commit()
            db.refresh(sample_problem)
            problem = sample_problem
        
        # Create match
        match = Match(
            player1_id=player1_id,
            player2_id=player2_id,
            problem_id=problem.id
        )
        db.add(match)
        db.commit()
        db.refresh(match)
        
        return {"message": "Match found!", "match_id": match.id}
    
    return {"message": "Waiting for opponent...", "position": len(matchmaking_queue)}

@router.get("/matchmaking/start")
async def start_match(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Find active match for current user
    match = db.query(Match).filter(
        ((Match.player1_id == current_user.id) | (Match.player2_id == current_user.id)) &
        (Match.status == "active")
    ).first()
    
    if not match:
        raise HTTPException(status_code=404, detail="No active match found")
    
    # Get problem details
    problem = db.query(Problem).filter(Problem.id == match.problem_id).first()
    
    return {
        "match": match,
        "problem": problem,
        "opponent": db.query(User).filter(
            User.id == (match.player2_id if match.player1_id == current_user.id else match.player1_id)
        ).first()
    }

@router.post("/submit")
async def submit_solution(
    submission: SubmissionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get match
    match = db.query(Match).filter(Match.id == submission.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Check if user is part of this match
    if current_user.id not in [match.player1_id, match.player2_id]:
        raise HTTPException(status_code=403, detail="Not authorized for this match")
    
    # Submit code to Judge0 (mock implementation)
    result = await submit_code_to_judge0(submission.code, submission.language)
    
    # Create submission record
    db_submission = Submission(
        user_id=current_user.id,
        match_id=submission.match_id,
        code=submission.code,
        language=submission.language,
        result=result["status"]
    )
    db.add(db_submission)
    
    # Update match with player's code
    if match.player1_id == current_user.id:
        match.code_player1 = submission.code
    else:
        match.code_player2 = submission.code
    
    # If code passed, end match and declare winner
    if result["status"] == "accepted":
        match.winner_id = current_user.id
        match.end_time = datetime.utcnow()
        match.status = "completed"
        
        # Update user stats
        winner = db.query(User).filter(User.id == current_user.id).first()
        loser_id = match.player2_id if match.player1_id == current_user.id else match.player1_id
        loser = db.query(User).filter(User.id == loser_id).first()
        
        winner.win_count += 1
        winner.rating += 25
        loser.loss_count += 1
        loser.rating = max(800, loser.rating - 25)
    
    db.commit()
    
    return {
        "submission_id": db_submission.id,
        "result": result,
        "match_completed": result["status"] == "accepted"
    }

@router.post("/result/{id}")
async def submit_match_result(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Check if user is part of this match
    if current_user.id not in [match.player1_id, match.player2_id]:
        raise HTTPException(status_code=403, detail="Not authorized for this match")
    
    # Update match with winner
    match.winner_id = current_user.id
    match.end_time = datetime.utcnow()
    match.status = "completed"
    
    # Update user stats
    winner = db.query(User).filter(User.id == current_user.id).first()
    loser_id = match.player2_id if match.player1_id == current_user.id else match.player1_id
    loser = db.query(User).filter(User.id == loser_id).first()
    
    winner.win_count += 1
    winner.rating += 25
    loser.loss_count += 1
    loser.rating = max(800, loser.rating - 25)
    
    db.commit()
    
    return {
        "message": "Match result submitted successfully",
        "winner": current_user.username,
        "match_id": id
    }

@router.get("/leaderboard")
async def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.rating.desc()).limit(10).all()
    return users
