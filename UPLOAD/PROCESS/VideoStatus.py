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
      
    def track_ffmpeg_progress(self, process, total_duration, file_name_uuid):
        for line in process.stderr:
            time_match = re.search(r"time=(\d+:\d+:\d+.\d+)", line)
            if time_match:
                elapsed_time_str = time_match.group(1)
                hours, minutes, seconds = elapsed_time_str.split(':')
                hours, minutes = int(hours), int(minutes)
                seconds = float(seconds)
                elapsed_time = hours * 3600 + minutes * 60 + seconds
                progress_percent = (elapsed_time / total_duration) * 100
                self.logger.info(f"FFmpeg Progress: {progress_percent:.2f}%")
                self.db_manager.update_download_status(file_name_uuid[:8], f"{progress_percent:.2f}%", 'Waiting')
