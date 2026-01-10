from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import traceback

# Import stamp detector
from stamp_detector import StampDetector

#Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), 'results')
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  #50MB max file size - can be changed

#Flask app creation
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

CORS(app)

#Create uploads and results directories if they don't exist
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(RESULTS_FOLDER).mkdir(parents=True, exist_ok=True)

# Initialize stamp detector (will load the trained model)
try:
    stamp_detector = StampDetector()
    print(f"Stamp detector initialized successfully!")
    print(f"Model info: {stamp_detector.get_model_info()}")
except Exception as e:
    print(f"Warning: Could not initialize stamp detector: {e}")
    print("Please train a model first using train_model.py")
    stamp_detector = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    #Handle PDF file upload and analyze for stamps Expected: multipart/form-data with 'file' field
    try:
        if stamp_detector is None:
            return jsonify({
                'error': 'Stamp detector not initialized. Please train a model first.'
            }), 503
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Only PDF and image files (jpg, jpeg, png) are allowed'
            }), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        #Get confidence threshold from request (default 0.25)
        conf_threshold = float(request.form.get('confidence', 0.25))
        
        ###########################Stamp detection logic###########################
        print(f"Processing file: {filename}")
        
        #Process the file for stamp detection
        results = stamp_detector.process_upload(
            file_path=filepath,
            conf_threshold=conf_threshold,
            output_dir=Path(app.config['RESULTS_FOLDER'])
        )
        
        #Prepare response
        response_data = {
            'message': 'File processed successfully',
            'filename': filename,
            'has_stamps': results['has_stamps'],
            'total_stamps': results['total_stamps'],
            'total_pages': results.get('total_pages', 1)
        }
        
        #Add detection details based on file type
        if filename.lower().endswith('.pdf'):
            #For PDF files, include per-page results
            pages_summary = []
            annotated_filenames = []
            
            for i, page_result in enumerate(results['pages']):
                pages_summary.append({
                    'page_number': page_result['page_number'],
                    'stamps_count': page_result['count'],
                    'detections': page_result['detections']
                })
                
                # Extract just the filename from the full path
                if results.get('annotated_paths') and i < len(results['annotated_paths']):
                    full_path = results['annotated_paths'][i]
                    filename_only = os.path.basename(full_path)
                    annotated_filenames.append(filename_only)
            
            response_data['pages'] = pages_summary
            response_data['annotated_paths'] = annotated_filenames
        else:
            # For image files
            response_data['detections'] = results['detections']
            if results.get('annotated_path'):
                response_data['annotated_path'] = os.path.basename(results['annotated_path'])
        
        return jsonify(response_data), 200
    
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    model_status = 'ready' if stamp_detector is not None else 'not_initialized'
    return jsonify({
        'status': 'ok',
        'model_status': model_status
    }), 200


@app.route('/api/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    if stamp_detector is None:
        return jsonify({
            'error': 'Model not initialized. Please train a model first.'
        }), 503
    
    return jsonify(stamp_detector.get_model_info()), 200


@app.route('/api/results/<path:filename>', methods=['GET'])
def get_result_image(filename):
    """Serve annotated result images"""
    try:
        result_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
        if os.path.exists(result_path):
            return send_file(result_path, mimetype='image/jpeg')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    #Run with debug mode enabled for development
    app.run(debug=True, host='localhost', port=5000)
