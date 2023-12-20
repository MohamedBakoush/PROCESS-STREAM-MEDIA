from flask import Flask, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)
CORS(app) 
    
# Load environment variables
load_dotenv()
    
# Simple in-memory cache
cache = {
    'last_video_id': None,
    'last_thumb_number': None,
    'full_file_path': None
} 
    
# Database connection parameters
db_params = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST')
}
    
# Example
# /watch?id=fd94f2c1 - return video 
# /watch?id=fd94f2c1&t=1 - return thumbnail 
@app.route('/watch') 
def serve_media():
    video_id = request.args.get('v')
    thumb_number = request.args.get('t')

    app.logger.info('video_id: %s', video_id)
    app.logger.info('thumb_number: %s', thumb_number)

    # Check if the current request matches the cached data
    if video_id == cache['last_video_id'] and thumb_number == cache['last_thumb_number']:
        app.logger.info("Using cached data")
        full_file_path = cache['full_file_path']
    else:
        app.logger.info("Fetching new data and updating cache")
        # Fetch new data from the database and update cache
        full_file_path = fetch_data_from_database(video_id, thumb_number)
        if full_file_path is None:
            app.logger.error("Failed to fetch file path from database")
            return "An error occurred", 500
        
        cache['last_video_id'] = video_id
        cache['last_thumb_number'] = thumb_number
        cache['full_file_path'] = full_file_path

    if full_file_path and os.path.isfile(full_file_path):
        return send_file(full_file_path, conditional=True)
    else:
        app.logger.info('File does not exist at path: %s', full_file_path)
        return "Media file not found", 404
            
def connect_to_database(attempts=5, delay=5):
    for _ in range(attempts):
        try:
            return psycopg2.connect(**db_params)
        except psycopg2.OperationalError as e:
            app.logger.warning("Could not connect to database, retrying...")
            time.sleep(delay)
    app.logger.error("Failed to connect to database after several attempts.")
    return None
        
def fetch_data_from_database(video_id, thumb_number):
    try:
        conn = connect_to_database()
        if not conn:
            app.logger.error("Database connection failed")
            return None  # Return None instead of a Flask Response
        
        cur = conn.cursor()
        app.logger.info("Database connection established")

        if thumb_number is not None:
            # Fetch thumbnail file path and name
            cur.execute('SELECT file_dir, file_path, file_name FROM thumbnails WHERE video_id = %s AND thumb_num = %s',
                        (video_id, thumb_number))
            app.logger.info("Thumbnail query executed")
        else:
            # Fetch video file path and name
            cur.execute('SELECT file_dir, file_path, file_name FROM videos WHERE video_id = %s', (video_id,))
            app.logger.info("Video query executed")

        result = cur.fetchone()
        app.logger.info("Query result fetched") 

        if result:
            file_dirs = result[0]
            file_path = result[1]
            file_name = result[2]

            # Check if file_dirs is not empty or None and is an array
            if file_dirs:
                # Join all elements of the file_dirs array into a single path
                dir_path = os.path.join(*file_dirs)
                full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), dir_path, file_path, file_name)
            else:
                full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), file_path, file_name)
    
        app.logger.info('full_path: %s', full_path)
    
    except Exception as e:
        app.logger.error("Error occurred: %s", e)
        return None  # Return None in case of an error

    finally:
        cur.close()
        conn.close()
        app.logger.info("Database connection closed")

    return full_path 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')