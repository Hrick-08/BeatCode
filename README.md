# BeatCode - Competitive Programming Platform

A real-time 1v1 competitive programming platform built with FastAPI and Next.js.

## Features

- 🔐 JWT-based authentication
- 👥 Real-time matchmaking system
- 💻 Live code editor with syntax highlighting
- ⚡ WebSocket-powered real-time communication
- 🏆 Rating system and leaderboards
- 🤖 AI code review (mock implementation)
- 📊 User profiles and match history

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily upgradable to PostgreSQL)
- **WebSockets** - Real-time communication
- **JWT** - Authentication
- **Pydantic** - Data validation

### Frontend
- **Next.js** - React framework
- **TailwindCSS** - Utility-first CSS framework
- **shadcn/ui** - UI component library
- **WebSocket Client** - Real-time updates

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
\`\`\`bash
cd backend
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart websockets
\`\`\`

4. Create environment file:
\`\`\`bash
cp .env.example .env
\`\`\`

5. Run database migrations and seed data:
\`\`\`bash
python scripts/seed_database.py
\`\`\`

6. Start the backend server:
\`\`\`bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
\`\`\`

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
\`\`\`bash
cd frontend
\`\`\`

2. Install dependencies:
\`\`\`bash
npm install
\`\`\`

3. Start the development server:
\`\`\`bash
npm run dev
\`\`\`

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT token
- `GET /api/user/profile` - Get current user profile
- `GET /api/user/matches` - Get user's match history

### Matchmaking & Games
- `POST /api/matchmaking/join` - Join matchmaking queue
- `GET /api/matchmaking/start` - Get current match details
- `POST /api/match/submit` - Submit code solution
- `POST /api/match/result` - Get match results
- `GET /api/leaderboard` - Get top players

### Problems
- `GET /api/problem/random` - Get a random problem
- `GET /api/problem/{id}` - Get specific problem details

### AI Review
- `POST /api/ai-review` - Get AI code review (mock)
- `GET /api/ai-review/{match_id}` - Get match AI reviews

### WebSocket
- `WS /ws/match/{room_id}` - Real-time match communication

## Database Schema

### Users
- id, username, email, hashed_password
- win_count, loss_count, rating
- created_at

### Problems
- id, title, description
- input_format, output_format, test_cases
- difficulty, created_at

### Matches
- id, player1_id, player2_id, problem_id
- winner_id, start_time, end_time
- code_player1, code_player2
- ai_score_p1, ai_score_p2, status

### Submissions
- id, user_id, match_id
- code, language, result, timestamp

## Features in Detail

### Real-time Matchmaking
- Simple queue-based system
- Automatic pairing when 2 players join
- WebSocket notifications for match updates

### Code Execution
- Mock Judge0 integration (replace with real API)
- Support for multiple languages
- Test case validation

### Rating System
- ELO-style rating updates
- Win/loss tracking
- Leaderboard rankings

### AI Code Review
- Mock implementation with random scores
- Structured feedback format
- Ready for Together.ai integration

## Environment Variables

Create a `.env` file in the backend directory:

\`\`\`env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./beatcode.db
JUDGE0_URL=https://judge0-ce.p.rapidapi.com
JUDGE0_API_KEY=your-judge0-api-key
TOGETHER_API_KEY=your-together-api-key
\`\`\`

## Deployment

### Backend (Vercel/Railway/Heroku)
1. Update database to PostgreSQL for production
2. Set environment variables
3. Deploy FastAPI application

### Frontend (Vercel/Netlify)
1. Update API URLs for production
2. Deploy Next.js application

## Future Enhancements

- [ ] Real Judge0 API integration
- [ ] Together.ai code review integration
- [ ] Tournament system
- [ ] Practice mode
- [ ] Code sharing and discussions
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Team competitions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
