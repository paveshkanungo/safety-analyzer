from flask import Flask, request, jsonify
from flask_cors import CORS
from main import run_analysis
from config import LOCATION as DEFAULT_LOCATION

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    if not data or 'hotel_name' not in data:
        return jsonify({"error": "Missing hotel_name"}), 400
        
    hotel_name = data['hotel_name']
    # If location is not provided, we can pass None or rely on default if needed,
    # but passing None is better to let query handle it, UNLESS the underlying function breaks.
    # The refactored fetch_google_maps_data uses whatever is passed.
    # Let's assume if location is blank, we don't send the ll parameter or send empty string?
    # Actually SerpAPI might accept query without ll.
    # But let's check if the user provided location bias.
    location = data.get('location', DEFAULT_LOCATION)
    
    try:
        # Run analysis
        report = run_analysis(query=hotel_name, location_bias=location)
        
        if "error" in report:
            return jsonify(report), 500
            
        return jsonify(report), 200
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = 5001
    print(f"🔥 Server starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
