import psycopg2  
import os  

class DatabaseManager:
    def __init__(self, logger):
        self.logger = logger
        self.db_connection = self.get_db_connection()

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                dbname=os.getenv('POSTGRES_DB')
            )
            return conn
        except Exception as e:
            self.logger.error(f"Error connecting to the database: {e}")
            return None

    def execute_query(self, query, params, success_message=None):
        if self.db_connection:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self.db_connection.commit()
                    if success_message:
                        self.logger.info(success_message)
            except Exception as e:
                self.logger.error(f"Database error: {e}")
                self.db_connection.rollback()
        else:
            self.logger.error("Database connection is not established.")

    def update_download_status(self, video_id, video_status, thumbnail_status):
        query = "UPDATE download_status SET video_download_status = %s, thumbnail_download_status = %s WHERE video_id = %s"
        params = (video_status, thumbnail_status, video_id)
        self.execute_query(query, params, f"Updated download status for {video_id}")
          
    def insert_video_data(self, video_id, file_name_uuid):
        query = "INSERT INTO videos (video_id, file_dir, file_path, file_name, file_type) VALUES (%s, %s, %s, %s, %s)"
        params = (video_id, [], file_name_uuid, f"{file_name_uuid}.mp4", 'video/mp4')
        self.execute_query(query, params, f"Inserted video data for {video_id}")

    def insert_thumbnail_data(self, video_id, thumb_num, file_path, thumb_file_name):
        query = "INSERT INTO thumbnails (video_id, thumb_num, file_dir, file_path, file_name, file_type) VALUES (%s, %s, %s, %s, %s, 'image/jpeg')"
        params = (video_id, thumb_num, [], file_path, thumb_file_name)
        self.execute_query(query, params, f"Inserted thumbnail {thumb_num} data for video {video_id}")

    def insert_video_info_data(self, video_id, video_title, video_description):
        query = "INSERT INTO info (video_id, video_title, video_description) VALUES (%s, %s, %s)"
        params = (video_id, video_title, video_description)
        self.execute_query(query, params, f"Inserted video info data for video {video_id}")

