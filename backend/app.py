import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from config import Config
from utils.file_handling import validate_file, save_uploaded_file

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
        
    file = request.files['file']
    validation_result = validate_file(file)
    
    if not validation_result['valid']:
        return jsonify({'error': validation_result['message']}), 400
    
    try:
        session_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = save_uploaded_file(file, session_id, filename)
        
        return jsonify({
            'session_id': session_id,
            'filename': filename,
            'message': 'File uploaded successfully',
            'path': file_path,
            'file_type': validation_result['file_type']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)