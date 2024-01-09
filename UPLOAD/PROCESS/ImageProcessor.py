import ffmpeg
import os

class ImageProcessor:
    def __init__(self, db_manager, video_status, logger):
        self.db_manager = db_manager
        self.video_status = video_status
        self.logger = logger
                
    def create_thumbnails(self, video_file, output_path, file_name_uuid, file_title, supabase_user_id, number_of_images=8, file_type=".jpg"):
        duration = self.video_status.get_video_duration(video_file)
        if duration <= 0:
            self.logger.error("Video duration is less or equal to 0, cannot create thumbnails.")
            return

        thumb_file_names = []  # Initialize the list here

        try:
            # FFmpeg command to create thumbnails
            thumb_file_name_pattern = f"{file_name_uuid}-thumbnail%03d{file_type}"
            ffmpeg.input(video_file).output(os.path.join(output_path, file_name_uuid, thumb_file_name_pattern), vf=f"fps={number_of_images}/{duration}").run(overwrite_output=True)

            # Populate thumb_file_names list
            for i in range(1, number_of_images + 1):
                thumb_file_name = f"{file_name_uuid}-thumbnail{i:03d}{file_type}"
                thumb_file_names.append(thumb_file_name)

            self.logger.info("Thumbnails created successfully")

            # Insert video data into the psql database
            self.db_manager.execute_video_user_id_data_insert(file_name_uuid[:8], file_title, "Description", [], file_name_uuid, f"{file_name_uuid}.mp4", "video/mp4", thumb_file_names, "image/jpeg", number_of_images, supabase_user_id),

        except Exception as e:
            self.logger.error(f"Error during thumbnail creation: {e}")

            # Log the specific FFmpeg error if available
            ffmpeg_error = getattr(e, 'stderr', None)
            try:
                self.logger.error(f"FFmpeg Error Details: {ffmpeg_error}")
            except Exception as e:
                self.logger.error(f"Error logging FFmpeg error details: {e}")