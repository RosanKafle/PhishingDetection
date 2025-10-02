from flask import Flask, jsonify, request
import pandas as pd
from threat_scoring import calculate_threat_score, classify_threat_level

app = Flask(__name__)

def validate_single_url(url):
    """Validate a single URL and return threat assessment"""
    print(f"Debug: Validating URL: {url}")
    try:
        score = calculate_threat_score(url)
        level = classify_threat_level(score)
        result = {
            'url': url,
            'threat_score': score,
            'threat_level': level,
            'valid': True,
            'malicious': score >= 60,
            'details': f'Threat assessment completed. Score: {score}/100, Level: {level}'
        }
        print(f"Debug: Validation result: {result}")
        return result
    except Exception as e:
        print(f"Error in validate_single_url: {e}")
        return {
            'url': url,
            'valid': False,
            'error': str(e)
        }

@app.route('/api/threats/recent', methods=['GET'])
def get_recent_threats():
    """Get recent threats from the scored dataset"""
    print("Debug: Received request for recent threats")
    try:
        df = pd.read_csv('combined_threats_scored.csv')
        print(f"Debug: Loaded {len(df)} threats from CSV")
        return jsonify(df.head(50).to_dict('records'))
    except Exception as e:
        print(f"Error loading recent threats: {e}")
        return jsonify({'error': f'Failed to load latest threats: {str(e)}'}), 500

@app.route('/api/threats/validate', methods=['POST'])
def validate_url():
    """Validate a URL for threats"""
    print("Debug: Received request for URL validation")
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        print("Error: Missing 'url' parameter in validate_url")
        return jsonify({'error': 'Missing "url" parameter'}), 400
    result = validate_single_url(url)
    return jsonify(result)

@app.route('/api/threats/score', methods=['POST'])
def score_url():
    """Score a URL for threat level"""
    print("Debug: Received request for URL scoring")
    data = request.get_json()
    url = data.get('url') if data else None
    if not url:
        print("Error: Missing 'url' parameter in score_url")
        return jsonify({'error': 'Missing "url" parameter'}), 400
    try:
        score = calculate_threat_score(url)
        level = classify_threat_level(score)
        result = {
            'url': url,
            'score': score,
            'level': level
        }
        print(f"Debug: Scoring result: {result}")
        return jsonify(result)
    except Exception as e:
        print(f"Error scoring URL: {e}")
        return jsonify({'error': f'Error scoring URL: {str(e)}'}), 500

@app.route('/api/threats/stats', methods=['GET'])
def get_threat_stats():
    """Get threat statistics"""
    print("Debug: Received request for threat stats")
    try:
        df = pd.read_csv('combined_threats_scored.csv')
        stats = {
            'total_urls': len(df),
            'sources': df['source'].value_counts().to_dict(),
            'threat_levels': df['threat_level'].value_counts().to_dict(),
            'average_score': df['threat_score'].mean()
        }
        print(f"Debug: Threat stats computed: {stats}")
        return jsonify(stats)
    except Exception as e:
        print(f"Error generating threat stats: {e}")
        return jsonify({'error': f'Failed to generate stats: {str(e)}'}), 500

if __name__ == '__main__':
    print("Debug: Starting Flask server on http://0.0.0.0:5001")
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        print(f"Flask server failed to start: {e}")
