import os
from datetime import timedelta

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Judge0 Configuration
JUDGE0_URL = os.getenv("JUDGE0_URL", "https://judge0-ce.p.rapidapi.com")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY", "mock-api-key")

# Together.ai Configuration (placeholder)
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "mock-together-key")
