"""
Configuration file for Hotel Safety Analyzer
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Search Configuration
QUERY = "Radisson Kharadi"
LOCATION = "@18.5654075,73.9445731,15z"
LAT, LON = 18.5654075, 73.9445731

# Safety Keywords
NEGATIVE_KEYWORDS = [
    "cockroach", "food poisoning", "unsafe", "dirty", 
    "theft", "harassment", "bad experience", "danger",
    "scared", "uncomfortable", "avoid", "terrible",
    "robbery", "crime", "violence", "unhygienic"
]

# Scoring Parameters
BASE_SCORE = 50
RATING_WEIGHTS = {
    "excellent": 15,  # >= 4 stars
    "good": 5,        # >= 3 stars
    "poor": -10       # < 3 stars
}

INFRASTRUCTURE_WEIGHTS = {
    "street_light": 1,
    "police_station": 10,
    "hospital": 5,
    "fire_station": 5
}

# Limits
MAX_STREET_LIGHT_SCORE = 15
MAX_POLICE_SCORE = 20
MAX_HOSPITAL_SCORE = 10
MAX_FIRE_STATION_SCORE = 5
MAX_NEGATIVE_REVIEW_PENALTY = 20
NEGATIVE_REVIEW_PENALTY_PER_HIT = 3

# Review Limits
MAX_REVIEWS_TO_ANALYZE = 20
MAX_TWEETS = 10
MAX_REDDIT_POSTS = 5

# API URLs
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Output
OUTPUT_FILE = "comprehensive_safety_report.json"