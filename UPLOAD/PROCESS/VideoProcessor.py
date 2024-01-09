import ffmpeg
import subprocess
import uuid
import os
import re

class VideoProcessor:
    def __init__(self, db_manager, video_status, image_processor, logger):
        self.db_manager = db_manager
        self.video_status = video_status
        self.image_processor = image_processor
        self.logger = logger
 
    def execute_ffmpeg(self, command):
        try:
            process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True)
            return process
        except Exception as e:
            self.logger.error(f"Error executing FFmpeg command: {e}")
            return None
        
    def ffmpeg_progress(self, file_path, output_path, supabase_user_id):
        file_name_uuid = str(uuid.uuid4())  # Generate a unique UUID
        os.makedirs(os.path.join(output_path, file_name_uuid), exist_ok=True)
        output_file = os.path.join(output_path, file_name_uuid, f"{file_name_uuid}.mp4")

        total_duration = self.video_status.get_video_duration(file_path)
        if total_duration is None:
            self.logger.error("Unable to determine video duration")
            return

        command = ['ffmpeg', '-i', file_path, '-c', 'copy', output_file]
        process = self.execute_ffmpeg(command)
        if process:
            process.wait()

            if process.returncode == 0:
                self.handle_successful_encoding(file_path, output_path, output_file, file_name_uuid, supabase_user_id)
            else:
                self.handle_failed_encoding(file_name_uuid)

    def handle_successful_encoding(self, file_path, output_path, output_file, file_name_uuid, supabase_user_id):
        try:
            file_title = file_path.split('/').pop().split('.')[0];
            os.remove(file_path)
            self.logger.info(f"Original file deleted: {file_path}") 
            
            # Create thumbnails
            self.image_processor.create_thumbnails(output_file, output_path, file_name_uuid, file_title, supabase_user_id)

        except OSError as e:
            self.logger.error(f"Error deleting original file: {e}")

    def handle_failed_encoding(self, file_name_uuid):
        self.logger.error("Re-encoding failed, original file not deleted.")