import subprocess
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/activate_privategpt', methods=['POST'])
def activate_privategpt():
    # Specify the full path to the batch file
    batch_file_path = r'C:\GPT\Bot\privateGPT-main\run_privategpt.bat'

    # Check if the batch file exists
    if not os.path.exists(batch_file_path):
        return jsonify({'error': 'Batch file not found'}), 500

    try:
        # Execute the batch file using a system command
        subprocess.Popen([batch_file_path])

        # You can also add additional logic or processing here if needed

        return 'PrivateGPT activated'
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)