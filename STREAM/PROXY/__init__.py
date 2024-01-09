from flask import Flask, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2
import os

app = Flask(__name__)
CORS(app) 
    
# Load environment variables
load_dotenv()
    
# Database connection parameters
db_params = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST')
}
    
@app.route('/watch') 
def serve_media():
    user_id = request.args.get('user')
    video_id = request.args.get('v')
    thumb_number = request.args.get('t')

    app.logger.info('user_id: %s', user_id)
    app.logger.info('video_id: %s', video_id)
    app.logger.info('thumb_number: %s', thumb_number)

    # Fetch new data from the database
    full_file_path = fetch_data_from_database(user_id, video_id, thumb_number)
    if full_file_path is None:
        app.logger.error("Failed to fetch file path from database")
        return "An error occurred", 500

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
        

def fetch_data_from_database(user_id, video_id, thumb_number):
    try:
        with connect_to_database() as conn:
            if not conn:
                app.logger.error("Database connection failed")
                return None  # Return None instead of a Flask Response

            with conn.cursor() as cur:
                app.logger.info("Database connection established")

                user_id_modified = user_id.replace('-', '_')
                table_name = "video_" + user_id_modified

                # Fetch video file path and name
                cur.execute(f'SELECT video_directory, video_path, video_name, auto_generated_thumbnail_names, auto_generated_thumbnail_num FROM {table_name} WHERE video_id = %s', (video_id,))
                app.logger.info("Video query executed")

                result = cur.fetchone()
                app.logger.info("Query result fetched")

                if result:
                    video_directory = result[0]
                    video_path = result[1]
                    video_name = result[2]
                    auto_generated_thumbnail_names = result[3]  # Array of thumbnail names
                    auto_generated_thumbnail_num = result[4]

                # Check if video_directory is not empty or None and is an array
                thumb_number = int(thumb_number) if thumb_number is not None else None

                # Check if thumb_number is greater than or equal to auto_generated_thumbnail_num
                if thumb_number is not None and thumb_number >= auto_generated_thumbnail_num:
                    return None  # Return None if thumb_number is out of range

                if video_directory:
                    dir_path = os.path.join(*video_directory)     
                    # Check if thumb_number
                    if thumb_number is not None:
                        thumbnail_name = auto_generated_thumbnail_names[thumb_number]
                        full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), dir_path, video_path, thumbnail_name)
                    else:
                        full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), dir_path, video_path, video_name)
                else:
                    # Check if thumb_number
                    if thumb_number is not None:
                        thumbnail_name = auto_generated_thumbnail_names[thumb_number]
                        full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), video_path, thumbnail_name)
                    else:
                        full_path = os.path.join(os.getenv('PERMANENT_MEDIA_ROOT'), video_path, video_name)

    except Exception as e:
        app.logger.error("Error occurred: %s", e)
        return None  # Return None in case of an error

    return full_path

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')