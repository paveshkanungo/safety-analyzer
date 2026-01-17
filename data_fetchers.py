"""
Data fetching functions for Hotel Safety Analyzer
"""
import requests
from serpapi import GoogleSearch
from config import *


def fetch_google_maps_data(query=QUERY, location=LOCATION):
    """Fetch place data and reviews from Google Maps using two-step approach"""
    
    # Step 1: Search for the place (without ll parameter which causes issues)
    search_params = {
        "engine": "google_maps",
        "type": "search",
        "q": query,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
    
    results = GoogleSearch(search_params).get_dict()
    
    # Debug: Print what we got from SerpAPI
    if "error" in results:
        print(f"   ⚠️ SerpAPI Search Error: {results.get('error')}")
    
    # Get the first local result (the hotel we're looking for)
    local_results = results.get("local_results", [])
    place = {}
    data_id = None
    
    if local_results:
        place = local_results[0]
        data_id = place.get("data_id")
        print(f"   ✓ Found place: {place.get('title')} (data_id: {data_id[:20] if data_id else 'N/A'}...)")
    else:
        # Try place_results as fallback
        place = results.get("place_results", {})
        data_id = place.get("data_id")
    
    place_data = {
        "name": place.get("title"),
        "rating": place.get("rating", 0),
        "total_reviews": place.get("reviews", 0),
        "address": place.get("address"),
        "coordinates": place.get("gps_coordinates"),
        "types": place.get("type", [])
    }
    
    reviews = []
    
    # Step 2: Fetch reviews using data_id if available
    if data_id:
        try:
            reviews_params = {
                "engine": "google_maps_reviews",
                "data_id": data_id,
                "hl": "en",
                "api_key": SERPAPI_KEY
            }
            
            reviews_results = GoogleSearch(reviews_params).get_dict()
            
            if "error" in reviews_results:
                print(f"   ⚠️ SerpAPI Reviews Error: {reviews_results.get('error')}")
            else:
                reviews_data = reviews_results.get("reviews", [])
                for r in reviews_data[:MAX_REVIEWS_TO_ANALYZE]:
                    reviews.append({
                        "source": "Google Maps",
                        "rating": r.get("rating"),
                        "text": r.get("snippet", r.get("text", "")),
                        "date": r.get("date", ""),
                        "author": r.get("user", {}).get("name", "Anonymous")
                    })
        except Exception as e:
            print(f"   ⚠️ Could not fetch reviews: {e}")
    
    return place_data, reviews


def fetch_twitter_reviews(hotel_name):
    """Fetch Twitter/X mentions using Google search (since Twitter engine is unsupported)"""
    params = {
        "engine": "google",
        "q": f"{hotel_name} hotel (site:twitter.com OR site:x.com)",
        "api_key": SERPAPI_KEY,
        "num": MAX_TWEETS
    }
    
    try:
        results = GoogleSearch(params).get_dict()
        
        # Debug: Check for errors
        if "error" in results:
            print(f"   ⚠️ SerpAPI Twitter Search Error: {results.get('error')}")
            return []
        
        search_results = results.get("organic_results", [])
        
        social_reviews = []
        for result in search_results[:MAX_TWEETS]:
            social_reviews.append({
                "source": "Twitter/X",
                "text": result.get("snippet", ""),
                "author": result.get("title", "").split(" on X:")[0] if " on X:" in result.get("title", "") else "Anonymous",
                "date": "",
                "link": result.get("link", "")
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


def fetch_infrastructure_data(lat=LAT, lon=LON):
    """Fetch nearby infrastructure from OpenStreetMap"""
    # Simplified query to reduce server load (removed street_lamp - too many results)
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="police"](around:1000,{lat},{lon});
      node["amenity"="hospital"](around:1000,{lat},{lon});
      node["emergency"="fire_station"](around:1000,{lat},{lon});
      way["highway"~"primary|secondary|tertiary"](around:500,{lat},{lon});
    );
    out count;
    out;
    """
    
    # Overpass API endpoints to try (primary + fallback)
    overpass_endpoints = [
        OVERPASS_URL,
        "https://overpass.kumi.systems/api/interpreter"  # Fallback endpoint
    ]
    
    default_infrastructure = {
        "street_lights": 0,
        "police_stations": 0,
        "hospitals": 0,
        "fire_stations": 0,
        "roads_nearby": 0
    }
    
    for endpoint in overpass_endpoints:
        try:
            # Use 'data' parameter with proper content-type for Overpass API
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            osm_response = requests.post(endpoint, data={"data": query}, headers=headers, timeout=45)
            
            # Debug: Check response status
            if osm_response.status_code == 504 or osm_response.status_code == 429:
                print(f"   ⚠️ Overpass API ({endpoint}) returned {osm_response.status_code}, trying fallback...")
                continue  # Try next endpoint
            
            if osm_response.status_code != 200:
                print(f"   ⚠️ Overpass API returned status {osm_response.status_code}")
                continue
            
            osm_data = osm_response.json()
            elements = osm_data.get("elements", [])
            
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
            print(f"Warning: Could not fetch from {endpoint} - {e}")
            continue
    
    # All endpoints failed
    print("   ⚠️ All Overpass API endpoints failed, using defaults")
    return default_infrastructure