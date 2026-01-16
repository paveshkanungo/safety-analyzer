"""
Data fetching functions for Hotel Safety Analyzer
"""
import requests
from serpapi import GoogleSearch
from config import *


def fetch_google_maps_data():
    """Fetch place data and reviews from Google Maps"""
    params = {
        "engine": "google_maps",
        "type": "search",
        "q": QUERY,
        "ll": LOCATION,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    
    results = GoogleSearch(params).get_dict()
    place = results.get("place_results", {})
    reviews_section = results.get("user_reviews", {})
    
    place_data = {
        "name": place.get("title"),
        "rating": place.get("rating", 0),
        "total_reviews": place.get("reviews", 0),
        "address": place.get("address"),
        "coordinates": place.get("gps_coordinates"),
        "types": place.get("type", [])
    }
    
    reviews = []
    for r in reviews_section.get("most_relevant", []):
        reviews.append({
            "source": "Google Maps",
            "rating": r.get("rating"),
            "text": r.get("description", ""),
            "date": r.get("date", ""),
            "author": r.get("user", {}).get("name", "Anonymous")
        })
    
    return place_data, reviews


def fetch_twitter_reviews(hotel_name):
    """Fetch tweets mentioning the hotel"""
    params = {
        "engine": "twitter",
        "q": f"{hotel_name} hotel review OR experience OR stay",
        "api_key": SERPAPI_KEY
    }
    
    try:
        results = GoogleSearch(params).get_dict()
        tweets = results.get("organic_results", [])
        
        social_reviews = []
        for tweet in tweets[:MAX_TWEETS]:
            social_reviews.append({
                "source": "Twitter/X",
                "text": tweet.get("snippet", ""),
                "author": tweet.get("user", {}).get("name", "Anonymous"),
                "date": tweet.get("date", ""),
                "link": tweet.get("link", "")
            })
        
        return social_reviews
    except Exception as e:
        print(f"Warning: Could not fetch Twitter data - {e}")
        return []


def fetch_reddit_reviews(hotel_name):
    """Fetch Reddit discussions about the hotel"""
    params = {
        "engine": "google",
        "q": f"{hotel_name} site:reddit.com",
        "api_key": SERPAPI_KEY
    }
    
    try:
        results = GoogleSearch(params).get_dict()
        reddit_results = results.get("organic_results", [])
        
        reddit_reviews = []
        for post in reddit_results[:MAX_REDDIT_POSTS]:
            reddit_reviews.append({
                "source": "Reddit",
                "title": post.get("title", ""),
                "snippet": post.get("snippet", ""),
                "link": post.get("link", "")
            })
        
        return reddit_reviews
    except Exception as e:
        print(f"Warning: Could not fetch Reddit data - {e}")
        return []


def fetch_infrastructure_data():
    """Fetch nearby infrastructure from OpenStreetMap"""
    query = f"""
    [out:json];
    (
      node["highway"="street_lamp"](around:800,{LAT},{LON});
      node["amenity"="police"](around:1500,{LAT},{LON});
      node["amenity"="hospital"](around:1500,{LAT},{LON});
      way["highway"](around:800,{LAT},{LON});
      node["emergency"="fire_station"](around:1500,{LAT},{LON});
    );
    out;
    """
    
    try:
        osm_response = requests.post(OVERPASS_URL, data=query, timeout=30).json()
        elements = osm_response.get("elements", [])
        
        infrastructure = {
            "street_lights": 0,
            "police_stations": 0,
            "hospitals": 0,
            "fire_stations": 0,
            "roads_nearby": 0
        }
        
        for el in elements:
            tags = el.get("tags", {})
            if tags.get("highway") == "street_lamp":
                infrastructure["street_lights"] += 1
            elif tags.get("amenity") == "police":
                infrastructure["police_stations"] += 1
            elif tags.get("amenity") == "hospital":
                infrastructure["hospitals"] += 1
            elif tags.get("emergency") == "fire_station":
                infrastructure["fire_stations"] += 1
            elif tags.get("highway"):
                infrastructure["roads_nearby"] += 1
        
        return infrastructure
    
    except Exception as e:
        print(f"Warning: Could not fetch infrastructure data - {e}")
        return {
            "street_lights": 0,
            "police_stations": 0,
            "hospitals": 0,
            "fire_stations": 0,
            "roads_nearby": 0
        }