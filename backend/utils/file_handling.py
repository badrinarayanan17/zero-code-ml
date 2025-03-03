import os
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from config import Config

def validate_file(file):
    """Validate file type and size"""
    result = {'valid': False, 'message': '', 'file_type': None}
    
    try:
        # Check file size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        if file_length > Config.MAX_FILE_SIZE:
            result['message'] = f'File size exceeds {Config.MAX_FILE_SIZE//(1024*1024)}MB limit'
            return result
            
        # Get file extension
        filename = secure_filename(file.filename)
        file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
        
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            result['message'] = f'Unsupported file type: {file_extension}'
            return result
            
        # Additional content validation for CSV
        if file_extension == 'csv':
            file.seek(0)
            try:
                pd.read_csv(file, nrows=1)
                file.seek(0)
            except Exception as e:
                result['message'] = f'Invalid CSV file: {str(e)}'
                return result
                
        result['file_type'] = file_extension
        result['valid'] = True
        return result
        
    except Exception as e:
        result['message'] = f'Validation error: {str(e)}'
        return result

def save_uploaded_file(file, session_id, filename):
    """Save uploaded file with session-based naming"""
    # Secure the filename
    secured_name = secure_filename(filename)
    file_extension = secured_name.split('.')[-1].lower()
    
    # Create new filename with session ID
    new_filename = f"{session_id}_{secured_name}"
    save_path = os.path.join(Config.UPLOAD_FOLDER, new_filename)
    
    # Save the file
    file.save(save_path)
    
    # Convert to CSV if needed
    if file_extension in ('xlsx', 'xls'):
        df = pd.read_excel(save_path)
        csv_path = os.path.splitext(save_path)[0] + '.csv'
        df.to_csv(csv_path, index=False)
        os.remove(save_path)
        return csv_path
        
    return save_path