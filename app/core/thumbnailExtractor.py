import ffmpeg
from ..util import print_log


class ThumbnailExtractor:
    def __init__(self, filename):
        self.filename = filename

    def extract_thumbnail(self, video_path, output_image_path):
        probe = ffmpeg.probe(video_path, v='error', select_streams='v:0', show_entries='format=duration')
        duration = float(probe['format']['duration'])
        
        middle_time = duration / 2
        
        ffmpeg.input(video_path, ss=middle_time).output(output_image_path, vframes=1).run()

    def run(self):
        print_log("Thumbnails extraction started.")
        try:
            for i in range(5):
                video_path = f"data/output/{self.filename}_{i}.mp4"
                output_image_path = f"data/thumbnail/{self.filename}_{i}.jpg"
                self.extract_thumbnail(video_path, output_image_path)
            print_log("Thumbnails extracted successfully.")
        except Exception as e:
            raise Exception(e)

