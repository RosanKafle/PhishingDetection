from flask import Flask, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/api/run_script', methods=['POST'])
def run_script():
    data = request.json
    script = data.get('script')
    args = data.get('args', [])
    # Always look for scripts in the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(project_root, script) if script else None
    if not script or not os.path.exists(script_path):
        return jsonify({'error': 'Script not found'}), 400
    try:
        result = subprocess.run([sys.executable, script_path] + args, capture_output=True, text=True, timeout=60)
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)
