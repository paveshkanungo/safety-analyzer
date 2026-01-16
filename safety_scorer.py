"""
Safety score calculation logic
"""
from config import *


def calculate_safety_score(place_data, all_reviews, infrastructure):
    """Calculate numerical safety score based on various factors"""
    
    score = BASE_SCORE
    
    # Rating impact
    rating = place_data.get("rating", 0)
    if rating >= 4:
        score += RATING_WEIGHTS["excellent"]
    elif rating >= 3:
        score += RATING_WEIGHTS["good"]
    else:
        score += RATING_WEIGHTS["poor"]
    
    # Check for negative keywords in reviews
    negative_hits = count_negative_reviews(all_reviews)
    penalty = min(negative_hits * NEGATIVE_REVIEW_PENALTY_PER_HIT, MAX_NEGATIVE_REVIEW_PENALTY)
    score -= penalty
    
    # Infrastructure impact
    score += min(
        infrastructure["street_lights"] * INFRASTRUCTURE_WEIGHTS["street_light"], 
        MAX_STREET_LIGHT_SCORE
    )
    score += min(
        infrastructure["police_stations"] * INFRASTRUCTURE_WEIGHTS["police_station"], 
        MAX_POLICE_SCORE
    )
    score += min(
        infrastructure["hospitals"] * INFRASTRUCTURE_WEIGHTS["hospital"], 
        MAX_HOSPITAL_SCORE
    )
    score += min(
        infrastructure["fire_stations"] * INFRASTRUCTURE_WEIGHTS["fire_station"], 
        MAX_FIRE_STATION_SCORE
    )
    
    # Road connectivity (crowd proxy)
    roads = infrastructure["roads_nearby"]
    if roads > 20:
        score += 10
    elif roads < 5:
        score -= 10
    
    # Ensure score is within 0-100 range
    score = max(0, min(100, score))
    
    return score, negative_hits


def count_negative_reviews(all_reviews):
    """Count reviews containing negative safety keywords"""
    negative_count = 0
    
    for review in all_reviews:
        text = review.get("text", "").lower()
        if any(keyword in text for keyword in NEGATIVE_KEYWORDS):
            negative_count += 1
    
    return negative_count


def get_safety_verdict(score):
    """Convert numerical score to safety verdict"""
    if score >= 75:
        return "SAFE for family stay"
    elif score >= 50:
        return "MODERATELY SAFE"
    else:
        return "NOT RECOMMENDED"


def get_detailed_breakdown(score, place_data, infrastructure, negative_hits):
    """Get detailed breakdown of score components"""
    breakdown = {
        "base_score": BASE_SCORE,
        "rating_bonus": 0,
        "infrastructure_bonus": 0,
        "negative_penalty": 0,
        "final_score": score
    }
    
    # Rating bonus
    rating = place_data.get("rating", 0)
    if rating >= 4:
        breakdown["rating_bonus"] = RATING_WEIGHTS["excellent"]
    elif rating >= 3:
        breakdown["rating_bonus"] = RATING_WEIGHTS["good"]
    else:
        breakdown["rating_bonus"] = RATING_WEIGHTS["poor"]
    
    # Infrastructure bonus
    infra_score = 0
    infra_score += min(infrastructure["street_lights"] * INFRASTRUCTURE_WEIGHTS["street_light"], MAX_STREET_LIGHT_SCORE)
    infra_score += min(infrastructure["police_stations"] * INFRASTRUCTURE_WEIGHTS["police_station"], MAX_POLICE_SCORE)
    infra_score += min(infrastructure["hospitals"] * INFRASTRUCTURE_WEIGHTS["hospital"], MAX_HOSPITAL_SCORE)
    infra_score += min(infrastructure["fire_stations"] * INFRASTRUCTURE_WEIGHTS["fire_station"], MAX_FIRE_STATION_SCORE)
    breakdown["infrastructure_bonus"] = infra_score
    
    # Negative penalty
    breakdown["negative_penalty"] = min(negative_hits * NEGATIVE_REVIEW_PENALTY_PER_HIT, MAX_NEGATIVE_REVIEW_PENALTY)
    
    return breakdown