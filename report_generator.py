"""
Report generation and output functions
"""
import json
from datetime import datetime
from config import OUTPUT_FILE, MAX_REVIEWS_TO_ANALYZE


def generate_report(place_data, all_reviews, infrastructure, safety_score, 
                   negative_hits, ai_analysis, verdict, google_reviews, 
                   twitter_reviews, reddit_reviews, score_breakdown):
    """Generate comprehensive safety report"""
    
    report = {
        "hotel_info": place_data,
        "safety_score": safety_score,
        "verdict": verdict,
        "score_breakdown": score_breakdown,
        "infrastructure": infrastructure,
        "review_sources": {
            "google_maps": len(google_reviews),
            "twitter": len(twitter_reviews),
            "reddit": len(reddit_reviews),
            "total": len(all_reviews)
        },
        "negative_review_count": negative_hits,
        "ai_analysis": ai_analysis,
        "all_reviews": all_reviews[:MAX_REVIEWS_TO_ANALYZE],
        "generated_at": datetime.now().isoformat(),
        "analysis_metadata": {
            "version": "2.0",
            "ai_model": "Gemini 1.5 Flash",
            "data_sources": ["Google Maps", "Twitter/X", "Reddit", "OpenStreetMap"]
        }
    }
    
    return report


def save_report(report, filename=OUTPUT_FILE):
    """Save report to JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(f"\n📄 Full report saved to: {filename}")
        return True
    except Exception as e:
        print(f"Error saving report: {e}")
        return False


def print_summary(place_data, safety_score, verdict, ai_analysis, 
                 all_reviews, google_reviews, twitter_reviews, reddit_reviews):
    """Print formatted summary to console"""
    
    print("\n" + "="*60)
    print("✅ SAFETY ANALYSIS COMPLETED")
    print("="*60)
    print(f"🏨 Hotel: {place_data['name']}")
    print(f"📍 Location: {place_data['address']}")
    print(f"⭐ Rating: {place_data['rating']}/5 ({place_data['total_reviews']} reviews)")
    print(f"🔐 Safety Score: {safety_score}/100")
    print(f"📌 Verdict: {verdict}")
    
    # AI Analysis Summary
    if ai_analysis and "error" not in ai_analysis:
        print(f"\n🤖 AI Assessment: {ai_analysis.get('assessment', 'N/A')}")
        print(f"📊 AI Confidence: {ai_analysis.get('confidence_score', 0)}/100")
        
        concerns = ai_analysis.get('concerns', [])
        if concerns and len(concerns) > 0:
            print(f"⚠️  Key Concerns: {', '.join(concerns[:3])}")
        
        positives = ai_analysis.get('positives', [])
        if positives and len(positives) > 0:
            print(f"✅ Positive Aspects: {', '.join(positives[:3])}")
    
    # Review Source Breakdown
    print(f"\n📊 Reviews Analyzed: {len(all_reviews)}")
    print(f"   - Google Maps: {len(google_reviews)}")
    print(f"   - Twitter/X: {len(twitter_reviews)}")
    print(f"   - Reddit: {len(reddit_reviews)}")
    
    print("="*60)


def print_detailed_analysis(score_breakdown, infrastructure):
    """Print detailed score breakdown"""
    print("\n" + "="*60)
    print("📊 DETAILED SCORE BREAKDOWN")
    print("="*60)
    print(f"Base Score: {score_breakdown['base_score']}")
    print(f"Rating Bonus: {score_breakdown['rating_bonus']:+d}")
    print(f"Infrastructure Bonus: {score_breakdown['infrastructure_bonus']:+d}")
    print(f"Negative Reviews Penalty: -{score_breakdown['negative_penalty']}")
    print(f"Final Score: {score_breakdown['final_score']}")
    
    print("\n🏗️ Infrastructure Details:")
    print(f"   - Street Lights: {infrastructure['street_lights']}")
    print(f"   - Police Stations: {infrastructure['police_stations']}")
    print(f"   - Hospitals: {infrastructure['hospitals']}")
    print(f"   - Fire Stations: {infrastructure['fire_stations']}")
    print(f"   - Roads Nearby: {infrastructure['roads_nearby']}")
    print("="*60)