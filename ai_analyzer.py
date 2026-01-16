"""
AI analysis using Google Gemini
"""
import json
import requests
from config import GEMINI_API_KEY, GEMINI_API_URL, MAX_REVIEWS_TO_ANALYZE


def analyze_with_genai(all_reviews, place_data, infrastructure):
    """Use Google Gemini AI to analyze reviews and provide safety insights"""
    
    # Prepare review text for AI analysis
    review_texts = "\n\n".join([
        f"[{r['source']}] Rating: {r.get('rating', 'N/A')} - {r['text'][:200]}"
        for r in all_reviews[:MAX_REVIEWS_TO_ANALYZE]
    ])
    
    prompt = f"""Analyze the safety of this hotel for families based on the following data:

Hotel: {place_data['name']}
Location: {place_data['address']}
Overall Rating: {place_data['rating']}/5
Total Reviews: {place_data['total_reviews']}

Infrastructure nearby:
- Street lights: {infrastructure['street_lights']}
- Police stations: {infrastructure['police_stations']}
- Hospitals: {infrastructure['hospitals']}
- Fire stations: {infrastructure['fire_stations']}

Recent Reviews:
{review_texts}

Please provide:
1. Safety Assessment (Safe/Moderate/Unsafe)
2. Key Safety Concerns (if any) - list as array
3. Positive Safety Aspects - list as array
4. Recommendations for families - list as array
5. Overall confidence score (0-100)

Format your response as JSON with keys: assessment, concerns, positives, recommendations, confidence_score"""

    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1500,
        }
    }
    
    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            gemini_response = response.json()
            
            # Extract text from Gemini response
            try:
                content = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
                
                # Try to parse JSON from response
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                ai_analysis = json.loads(content.strip())
                
                # Validate required fields
                required_fields = ["assessment", "concerns", "positives", "recommendations", "confidence_score"]
                for field in required_fields:
                    if field not in ai_analysis:
                        ai_analysis[field] = [] if field != "assessment" and field != "confidence_score" else "N/A"
                
                return ai_analysis
                
            except Exception as parse_error:
                print(f"Warning: Could not parse AI response - {parse_error}")
                return {
                    "assessment": "Unable to parse",
                    "concerns": [],
                    "positives": [],
                    "recommendations": [],
                    "confidence_score": 0,
                    "raw_response": content if 'content' in locals() else "Error extracting content"
                }
        else:
            print(f"Error: API returned status {response.status_code}")
            return {
                "error": f"API returned status {response.status_code}", 
                "details": response.text,
                "assessment": "Error",
                "concerns": [],
                "positives": [],
                "recommendations": [],
                "confidence_score": 0
            }
    
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return {
            "error": str(e),
            "assessment": "Error",
            "concerns": [],
            "positives": [],
            "recommendations": [],
            "confidence_score": 0
        }