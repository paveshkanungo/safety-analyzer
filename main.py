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


def main():
    """Main execution function"""
    print("🔍 Starting comprehensive hotel safety analysis...")
    print("="*60)
    
    # Step 1: Fetch Google Maps data
    print("\n📍 Fetching Google Maps data...")
    try:
        place_data, google_reviews = fetch_google_maps_data()
        print(f"   ✓ Found {len(google_reviews)} Google reviews")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return
    
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
    infrastructure = fetch_infrastructure_data()
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
    
    # Step 9: Save report
    save_report(final_report)
    
    # Step 10: Print summary
    print_summary(
        place_data, safety_score, verdict, ai_analysis,
        all_reviews, google_reviews, twitter_reviews, reddit_reviews
    )
    
    # Optional: Print detailed breakdown
    print_detailed_analysis(score_breakdown, infrastructure)
    
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