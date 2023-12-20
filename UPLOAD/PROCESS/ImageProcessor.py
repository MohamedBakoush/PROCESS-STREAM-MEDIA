import ffmpeg
import os

class ImageProcessor:
    def __init__(self, db_manager, video_status, logger):
        self.db_manager = db_manager
        self.video_status = video_status
        self.logger = logger
        
    def create_thumbnails(self, video_file, output_path, file_name_uuid, number_of_images=8, file_type=".jpg"):
        duration = self.video_status.get_video_duration(video_file)
        if duration <= 0:
            self.logger.error("Video duration is less or equal to 0, cannot create thumbnails.")
            return

        try:
            thumb_file_name_pattern = f"{file_name_uuid}-thumbnail%03d{file_type}"
            ffmpeg.input(video_file).output(os.path.join(output_path, file_name_uuid, thumb_file_name_pattern), vf=f"fps={number_of_images}/{duration}").run(overwrite_output=True)

            # FFmpeg command to create thumbnails
            # Insert thumbnail data into the database
            for i in range(1, number_of_images + 1):
                thumb_file_name = f"{file_name_uuid}-thumbnail{i:03d}{file_type}"
                self.db_manager.insert_thumbnail_data(file_name_uuid[:8], i, file_name_uuid, thumb_file_name)

            self.db_manager.update_download_status(file_name_uuid[:8], 'Download complete', 'Complete')
            self.logger.info("Thumbnails created successfully")

        except Exception as e:
            self.logger.error(f"Error during thumbnail creation: {e}")
            self.db_manager.update_download_status(file_name_uuid[:8], 'Download complete', 'Thumbnail creation failed')
 