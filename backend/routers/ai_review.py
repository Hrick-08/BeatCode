from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import random

from database import get_db
from models import Match
from schemas import AIReviewRequest, AIReviewResponse
from routers.auth import get_current_user

router = APIRouter(
    prefix="/ai-review",
    tags=["AI Review"],
    responses={404: {"description": "Not found"}}
)

# Mock AI feedback responses
MOCK_FEEDBACK = [
    "Great solution! Consider using a hash map to reduce lookup time from O(n) to O(1).",
    "Good approach, but you could optimize the space complexity by using two pointers.",
    "Nice work! Try to add more edge case handling for robustness.",
    "Solid implementation. Consider using built-in functions for cleaner code.",
    "Well done! The algorithm is correct, but you could improve readability with better variable names.",
    "Excellent solution! Very efficient and clean code structure.",
    "Good logic, but consider handling null/empty inputs more gracefully.",
    "Nice approach! You could reduce the number of iterations with a different algorithm."
]

@router.post("/", response_model=AIReviewResponse)
async def create_ai_review(request: AIReviewRequest, db: Session = Depends(get_db)):
    # Mock AI review - replace with actual Together.ai integration later
    score = round(random.uniform(6.0, 9.5), 1)
    feedback = random.choice(MOCK_FEEDBACK)
    
    return AIReviewResponse(score=score, feedback=feedback)

@router.get("/{match_id}")
async def get_ai_review(match_id: int, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if current_user.id not in [match.player1_id, match.player2_id]:
        raise HTTPException(status_code=403, detail="Not authorized for this match")
    
    return {
        "match_id": match_id,
        "ai_score_p1": match.ai_score_p1 or random.uniform(6.0, 9.5),
        "ai_score_p2": match.ai_score_p2 or random.uniform(6.0, 9.5),
        "feedback_p1": "Good solution with efficient algorithm choice.",
        "feedback_p2": "Nice approach, could be optimized further."
    }
