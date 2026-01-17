"""
AI analysis using Google Gemini
"""
import json
import re
import requests
from config import GEMINI_API_KEY, GEMINI_API_URL, MAX_REVIEWS_TO_ANALYZE


def extract_from_text(content):
    """Fallback: Extract safety analysis from raw text when JSON parsing fails"""
    result = {
        "assessment": "Moderate",
        "concerns": [],
        "positives": [],
        "recommendations": [],
        "confidence_score": 50
    }
    
    content_lower = content.lower()
    
    # Determine assessment based on keywords
    if any(word in content_lower for word in ["safe", "secure", "recommended", "family-friendly"]):
        result["assessment"] = "Safe"
        result["confidence_score"] = 70
    elif any(word in content_lower for word in ["unsafe", "dangerous", "avoid", "not recommended"]):
        result["assessment"] = "Unsafe"
        result["confidence_score"] = 65
    else:
        result["assessment"] = "Moderate"
        result["confidence_score"] = 55
    
    # Extract concerns and positives using simple pattern matching
    if "concern" in content_lower or "negative" in content_lower:
        result["concerns"] = ["Some concerns identified in reviews"]
    if "positive" in content_lower or "good" in content_lower:
        result["positives"] = ["Some positive aspects noted"]
    if "recommend" in content_lower:
        result["recommendations"] = ["Review detailed analysis for specifics"]
    
    return result


def analyze_with_genai(all_reviews, place_data, infrastructure):
    """Use Google Gemini AI to analyze reviews and provide safety insights"""
    
    # Prepare review text for AI analysis - limit to avoid token overflow
    review_texts = "\n".join([
        f"[{r['source']}] {r.get('rating', 'N/A')}/5 - {r['text'][:150]}"
        for r in all_reviews[:15]  # Max 15 reviews total for AI
    ])
    
    # Build prompt carefully to avoid JSON issues
    hotel_name = place_data.get('name', 'Unknown Hotel')
    hotel_address = place_data.get('address', 'Unknown Location')
    hotel_rating = place_data.get('rating', 0)
    total_reviews = place_data.get('total_reviews', 0)
    hospitals = infrastructure.get('hospitals', 0)
    police = infrastructure.get('police_stations', 0)
    
    prompt = f"""Analyze this hotel's safety for families:

Hotel: {hotel_name}
Location: {hotel_address}
Google Rating: {hotel_rating}/5 ({total_reviews} reviews)
Nearby: {hospitals} hospitals, {police} police stations

Reviews:
{review_texts if review_texts else 'No reviews available'}

Based on the above, provide a JSON response with these exact keys:
- assessment: either "Safe", "Moderate", or "Unsafe"
- concerns: array of 2-3 safety concerns (or empty array if none)
- positives: array of 2-3 positive safety aspects
- recommendations: array of 2-3 tips for families
- confidence_score: number 0-100 based on data quality

Respond with ONLY the JSON object, no explanation or markdown."""

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
            "temperature": 0.1,  # Very low for consistent output
            "topK": 5,
            "topP": 0.5,
            "maxOutputTokens": 500,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "object",
                "properties": {
                    "assessment": {
                        "type": "string",
                        "enum": ["Safe", "Moderate", "Unsafe"]
                    },
                    "concerns": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "positives": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "recommendations": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "confidence_score": {
                        "type": "integer"
                    }
                },
                "required": ["assessment", "concerns", "positives", "recommendations", "confidence_score"]
            }
        }
    }
    
    try:
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url, headers=headers, json=payload, timeout=60)  # Increased timeout
        
        if response.status_code == 200:
            gemini_response = response.json()
            
            # Extract text from Gemini response
            try:
                content = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
                
                # Clean the content first
                json_content = content.strip()
                
                # Remove markdown code blocks
                if "```json" in json_content:
                    json_content = json_content.split("```json")[1].split("```")[0]
                elif "```" in json_content:
                    parts = json_content.split("```")
                    if len(parts) >= 2:
                        json_content = parts[1]
                
                json_content = json_content.strip()
                
                # Try to find JSON object using regex
                import re
                json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', json_content, re.DOTALL)
                if json_match:
                    json_content = json_match.group(0)
                
                try:
                    ai_analysis = json.loads(json_content)
                except json.JSONDecodeError as je:
                    print(f"   ⚠️ JSON decode error: {je}. Attempting to fix...")
                    
                    # Try aggressive JSON repair
                    fixed_json = json_content
                    
                    # Remove any trailing incomplete content after last complete value
                    # Find the last complete key-value pair
                    last_complete = max(
                        fixed_json.rfind('"],'),
                        fixed_json.rfind('"],'),
                        fixed_json.rfind('"}'),
                        fixed_json.rfind('],'),
                        fixed_json.rfind(': 0'),
                        fixed_json.rfind(': 1'),
                    )
                    
                    if last_complete > 0:
                        fixed_json = fixed_json[:last_complete + 1]
                    
                    # Close any open structures
                    open_brackets = fixed_json.count('[') - fixed_json.count(']')
                    open_braces = fixed_json.count('{') - fixed_json.count('}')
                    fixed_json = fixed_json + (']' * max(0, open_brackets)) + ('}' * max(0, open_braces))
                    
                    try:
                        ai_analysis = json.loads(fixed_json)
                    except:
                        # Ultimate fallback: extract info from text using patterns
                        print("   ⚠️ JSON repair failed. Using text extraction fallback...")
                        ai_analysis = extract_from_text(content)
                
                # Validate required fields
                required_fields = ["assessment", "concerns", "positives", "recommendations", "confidence_score"]
                for field in required_fields:
                    if field not in ai_analysis:
                        if field in ["concerns", "positives", "recommendations"]:
                            ai_analysis[field] = []
                        elif field == "confidence_score":
                            ai_analysis[field] = 50  # Default to 50 instead of 0
                        else:
                            ai_analysis[field] = "Moderate"  # Default assessment
                
                # Ensure confidence_score is a number
                if isinstance(ai_analysis.get("confidence_score"), str):
                    try:
                        ai_analysis["confidence_score"] = int(ai_analysis["confidence_score"])
                    except:
                        ai_analysis["confidence_score"] = 50
                
                return ai_analysis
                
            except Exception as parse_error:
                print(f"Warning: Could not parse AI response - {parse_error}")
                return {
                    "assessment": "Unable to parse",
                    "concerns": [],
                    "positives": [],
                    "recommendations": [],
                    "confidence_score": 0,
                    "raw_response": content[:500] if 'content' in locals() else "Error extracting content"
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