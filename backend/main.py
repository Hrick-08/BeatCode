from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import asyncio
import json
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import os
from typing import Dict, List

from database import get_db, engine
from models import Base, User, Problem, Match, Submission
from schemas import UserCreate, UserLogin, UserResponse, MatchCreate, SubmissionCreate
from routers import auth, match, problem, ai_review
from ws.connection_manager import ConnectionManager

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="BeatCode API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(match.router, prefix="/api")
app.include_router(problem.router, prefix="/api")
app.include_router(ai_review.router, prefix="/api")

# WebSocket connection manager
manager = ConnectionManager()

@app.websocket("/ws/match/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await manager.broadcast_to_room(room_id, message)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)

@app.get("/")
async def root():
    return {"message": "BeatCode API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
