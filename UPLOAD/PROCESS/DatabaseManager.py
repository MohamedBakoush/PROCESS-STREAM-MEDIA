import psycopg2  
from psycopg2 import pool
import os  

class DatabaseManager:
    def __init__(self, logger):
        self.logger = logger
        self.db_pool = self.get_db_pool()
        self.temp_storage = {}

    def get_db_pool(self):
        try:
            return psycopg2.pool.SimpleConnectionPool(
                1,  # minconn
                10,  # maxconn
                host=os.getenv('POSTGRES_HOST'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                dbname=os.getenv('POSTGRES_DB')
            )
        except Exception as e:
            self.logger.error(f"Error creating the database connection pool: {e}")
            return None

    def execute_query(self, query, params, success_message=None):
        connection = self.db_pool.getconn()
        if connection:
            try:
                with connection, connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    if success_message:
                        self.logger.info(success_message)
            except Exception as e:
                self.logger.error(f"Database error: {e}")
                connection.rollback()
            finally:
                self.db_pool.putconn(connection)
        else:
            self.logger.error("Unable to get a database connection from the pool.")

    def execute_video_user_id_data_insert(self, video_id, video_title, video_description, video_directory, video_path, video_name, video_type, auto_generated_thumbnail_names, auto_generated_thumbnail_type, auto_generated_thumbnail_num, supabase_user_id):
         
        supabase_user_id_modified = supabase_user_id.replace('-', '_')
        TableName = "video_" + supabase_user_id_modified

        query = f"""
            INSERT INTO {TableName} (
                video_id, video_title, video_description, video_directory, video_path,
                video_name, video_type, auto_generated_thumbnail_names, 
                auto_generated_thumbnail_type, auto_generated_thumbnail_num, supabase_user_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            video_id, video_title, video_description, video_directory, video_path,
            video_name, video_type, auto_generated_thumbnail_names, 
            auto_generated_thumbnail_type, auto_generated_thumbnail_num, supabase_user_id
        )

        self.execute_query(query, params, f"Inserted data into {TableName} table")