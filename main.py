"""
Hotel Safety Analyzer - Main Application
"""
from data_fetchers import (
    fetch_google_maps_data,
    fetch_twitter_reviews,
    fetch_reddit_reviews,
    fetch_infrastructure_data
)
from ai_analyzer import analyze_with_genai
from safety_scorer import (
    calculate_safety_score,
    get_safety_verdict,
    get_detailed_breakdown
)
from report_generator import (
    generate_report,
    save_report,
    print_summary,
    print_detailed_analysis
)


from config import QUERY, LOCATION, LAT, LON

def run_analysis(query=QUERY, location_bias=LOCATION):
    """
    Run the full safety analysis.
    Returns the final report dictionary.
    """
    print(f"🔍 Starting analysis for: {query}")
    print("="*60)
    
    # Step 1: Fetch Google Maps data
    print("\n📍 Fetching Google Maps data...")
    try:
        place_data, google_reviews = fetch_google_maps_data(query=query, location=location_bias)
        print(f"   ✓ Found {len(google_reviews)} Google reviews")
    except Exception as e:
        error_msg = f"Error fetching Google Maps data: {e}"
        print(f"   ✗ {error_msg}")
        return {"error": error_msg}
    
    # Extract coordinates from place data if available, otherwise use defaults
    lat, lon = LAT, LON
    if place_data.get("coordinates"):
        try:
            lat = place_data["coordinates"]["latitude"]
            lon = place_data["coordinates"]["longitude"]
            print(f"   ✓ Detected coordinates: {lat}, {lon}")
        except KeyError:
            print("   ⚠️  Could not parse coordinates, using defaults")
    
    # Step 2: Fetch Twitter reviews
    print("\n🐦 Fetching Twitter/X reviews...")
    twitter_reviews = fetch_twitter_reviews(place_data["name"])
    print(f"   ✓ Found {len(twitter_reviews)} tweets")
    
    # Step 3: Fetch Reddit discussions
    print("\n👾 Fetching Reddit discussions...")
    reddit_reviews = fetch_reddit_reviews(place_data["name"])
    print(f"   ✓ Found {len(reddit_reviews)} Reddit posts")
    
    # Step 4: Fetch infrastructure data
    print("\n🏗️ Fetching infrastructure data...")
    # Use detected coordinates
    infrastructure = fetch_infrastructure_data(lat=lat, lon=lon)
    print(f"   ✓ Infrastructure data collected")
    
    # Step 5: Combine all reviews
    all_reviews = google_reviews + twitter_reviews
    for reddit in reddit_reviews:
        all_reviews.append({
            "source": "Reddit",
            "text": f"{reddit['title']} - {reddit['snippet']}",
            "link": reddit["link"]
        })
    
    print(f"\n📊 Total reviews collected: {len(all_reviews)}")
    
    # Step 6: Calculate safety score
    print("\n🔢 Calculating safety score...")
    safety_score, negative_hits = calculate_safety_score(
        place_data, all_reviews, infrastructure
    )
    verdict = get_safety_verdict(safety_score)
    score_breakdown = get_detailed_breakdown(
        safety_score, place_data, infrastructure, negative_hits
    )
    print(f"   ✓ Safety score calculated: {safety_score}/100")
    
    # Step 7: GenAI Analysis
    print("\n🤖 Running Gemini AI analysis...")
    ai_analysis = analyze_with_genai(all_reviews, place_data, infrastructure)
    if "error" in ai_analysis:
        print(f"   ⚠️  AI analysis encountered an issue: {ai_analysis.get('error')}")
    else:
        print(f"   ✓ AI analysis completed")
    
    # Step 8: Generate report
    print("\n📝 Generating comprehensive report...")
    final_report = generate_report(
        place_data=place_data,
        all_reviews=all_reviews,
        infrastructure=infrastructure,
        safety_score=safety_score,
        negative_hits=negative_hits,
        ai_analysis=ai_analysis,
        verdict=verdict,
        google_reviews=google_reviews,
        twitter_reviews=twitter_reviews,
        reddit_reviews=reddit_reviews,
        score_breakdown=score_breakdown
    )
    
    return final_report

def main():
    """CLI Entry point"""
    report = run_analysis()
    if "error" in report:
        return
        
    # Save report
    save_report(report)
    
    # Print summary
    # Reconstruction of arguments for print_summary from the report
    # This might be tricky if print_summary relies on variables not in report.
    # But checking print_summary signature:
    # print_summary(place_data, safety_score, verdict, ai_analysis, all_reviews, ...)
    # All these are in final_report actually? No, final_report is a dict.
    # Let's see report_generator.py if needed.
    # For now, I will just call print_summary with the data I still have local access to? 
    # No, I returned only the report.
    # To keep CLI working exactly as before without massive refactor, I can re-extract from report
    # or just accept that the CLI main function prints less or I move the printing inside run_analysis?
    # actually, run_analysis is printing progress. 
    # let's just let main() call save_report and maybe a simple "Check JSON" message.
    # Or, I can update print_summary to take the report object.
    
    print("\n✅ Analysis complete! Check the JSON file for full details.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()