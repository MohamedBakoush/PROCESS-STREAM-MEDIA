import ffmpeg
import re

class VideoStatus:
    def __init__(self, db_manager, logger):
        self.db_manager = db_manager
        self.logger = logger

    def get_video_duration(self, file_path):
        try:
            probe = ffmpeg.probe(file_path)
            return float(probe['format']['duration'])
        except Exception as e:
            self.logger.error(f"Error getting video duration: {e}")
            return 0