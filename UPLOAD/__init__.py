from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import tempfile
import os 

from PROCESS.DatabaseManager import DatabaseManager
from PROCESS.VideoStatus import VideoStatus
from PROCESS.VideoProcessor import VideoProcessor
from PROCESS.ImageProcessor import ImageProcessor

app = Flask(__name__) # Create Flask app
CORS(app)  # Enable CORS for all routes 
load_dotenv() # Load environment variables

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'flv', 'wmv'}
app.config['UPLOAD_FOLDER'] = os.getenv('PERMANENT_MEDIA_ROOT')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/upload', methods=['POST'])
def upload_file():
    app.logger.info('UPLOAD_FOLDER: %s', app.config['UPLOAD_FOLDER'])
    
    supabase_user_id = request.form.get('supabase_user_id')
    if not supabase_user_id:
        return jsonify({'error': 'Supabase user ID is required'}), 400

    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        app.logger.error('No selected file or file type not allowed')
        return jsonify({'error': 'No selected file or file type not allowed'}), 400

    try:
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, filename)
        file.save(temp_path)

        # Initialize DatabaseManager which also manages the DB connection
        db_manager = DatabaseManager(app.logger)
        if not db_manager.db_pool:
            raise Exception("Failed to connect to the database")

        # Initialize other classes
        video_status = VideoStatus(db_manager, app.logger)
        image_processor = ImageProcessor(db_manager, video_status, app.logger)
        video_processor = VideoProcessor(db_manager, video_status, image_processor, app.logger)

        # Process video and create thumbnails
        video_processor.ffmpeg_progress(temp_path, app.config['UPLOAD_FOLDER'], supabase_user_id)

        # Close the database connection
        db_manager.db_pool.closeall()

        return jsonify({'message': 'File successfully uploaded'}), 200

    except Exception as e:
        app.logger.error(f"Error in file upload: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')