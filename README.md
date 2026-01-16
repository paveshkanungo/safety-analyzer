# Hotel Safety Analyzer 🏨🔐

A comprehensive hotel safety analysis tool that uses AI, social media reviews, and infrastructure data to assess hotel safety for families.

## 📁 Project Structure

```
hotel-safety-analyzer/
│
├── config.py                 # Configuration and constants
├── data_fetchers.py          # Data collection from various sources
├── ai_analyzer.py            # Google Gemini AI integration
├── safety_scorer.py          # Safety score calculation logic
├── report_generator.py       # Report generation and output
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Features

- **Multi-source Review Collection**
  - Google Maps reviews
  - Twitter/X mentions
  - Reddit discussions

- **Infrastructure Analysis**
  - Street lighting
  - Police stations proximity
  - Hospital accessibility
  - Fire station coverage

- **AI-Powered Analysis**
  - Google Gemini AI integration
  - Intelligent pattern recognition
  - Safety concern identification

- **Comprehensive Scoring**
  - 0-100 safety score
  - Detailed breakdown
  - Clear verdict (Safe/Moderate/Unsafe)

## 📋 Requirements

- Python 3.8+
- SerpAPI account (for reviews)
- Google Gemini API key (for AI analysis)

## 🔧 Installation

1. **Clone or download the project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```env
SERPAPI_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

Or export them directly:
```bash
export SERPAPI_KEY="your_serpapi_key_here"
export GEMINI_API_KEY="your_gemini_api_key_here"
```

## 🔑 Getting API Keys

### SerpAPI Key
1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for free account
3. Copy your API key from dashboard

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy your API key

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Change the hotel to analyze
QUERY = "Your Hotel Name"
LOCATION = "@latitude,longitude,15z"
LAT, LON = latitude, longitude

# Adjust safety keywords
NEGATIVE_KEYWORDS = [
    "cockroach", "unsafe", "theft", 
    # Add more keywords...
]

# Modify scoring weights
BASE_SCORE = 50
RATING_WEIGHTS = {
    "excellent": 15,
    "good": 5,
    "poor": -10
}
```

## 🎯 Usage

Run the analysis:
```bash
python main.py
```

The script will:
1. Fetch hotel data from Google Maps
2. Collect social media reviews
3. Analyze nearby infrastructure
4. Calculate safety score
5. Run AI analysis with Gemini
6. Generate comprehensive report

## 📊 Output

The tool generates two outputs:

### 1. Console Summary
```
✅ SAFETY ANALYSIS COMPLETED
============================================================
🏨 Hotel: Radisson Kharadi
📍 Location: Pune, Maharashtra
⭐ Rating: 4.2/5 (1,234 reviews)
🔐 Safety Score: 78/100
📌 Verdict: SAFE for family stay

🤖 AI Assessment: Safe
📊 AI Confidence: 85/100
✅ Positive Aspects: Well-lit area, Security staff, Clean rooms
```

### 2. JSON Report
Saved as `comprehensive_safety_report.json` containing:
- Full hotel information
- All reviews (up to 20)
- Infrastructure details
- Score breakdown
- AI analysis with recommendations
- Timestamp

## 🏗️ Module Descriptions

### `config.py`
- API keys and credentials
- Search parameters
- Scoring weights
- Safety keywords
- Configuration constants

### `data_fetchers.py`
- `fetch_google_maps_data()` - Google Maps reviews
- `fetch_twitter_reviews()` - Twitter/X mentions
- `fetch_reddit_reviews()` - Reddit discussions
- `fetch_infrastructure_data()` - OpenStreetMap data

### `ai_analyzer.py`
- `analyze_with_genai()` - Gemini AI analysis
- JSON parsing and validation
- Error handling

### `safety_scorer.py`
- `calculate_safety_score()` - Score calculation
- `count_negative_reviews()` - Negative keyword detection
- `get_safety_verdict()` - Verdict determination
- `get_detailed_breakdown()` - Score component breakdown

### `report_generator.py`
- `generate_report()` - Report compilation
- `save_report()` - JSON file export
- `print_summary()` - Console output
- `print_detailed_analysis()` - Detailed breakdown

### `main.py`
- Orchestrates entire analysis
- Step-by-step execution
- Error handling
- Progress logging

## 🎨 Customization

### Add New Data Sources
Edit `data_fetchers.py`:
```python
def fetch_tripadvisor_reviews(hotel_name):
    # Your implementation
    pass
```

### Modify AI Prompt
Edit `ai_analyzer.py`:
```python
prompt = f"""Your custom prompt here..."""
```

### Change Scoring Algorithm
Edit `safety_scorer.py`:
```python
def calculate_safety_score(place_data, all_reviews, infrastructure):
    # Your custom scoring logic
    pass
```

## 🐛 Troubleshooting

**Issue: API Key errors**
- Verify keys are set in environment
- Check key validity on provider dashboards

**Issue: No reviews found**
- Verify hotel name is correct
- Check SerpAPI quota
- Try different search query

**Issue: AI analysis fails**
- Check Gemini API key
- Verify internet connection
- Review rate limits

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

Feel free to:
- Add new data sources
- Improve scoring algorithm
- Enhance AI prompts
- Add features

## 📧 Support

For issues or questions:
1. Check the documentation
2. Review error messages
3. Verify API keys and quotas

---

**Made with ❤️ for safer family travels**