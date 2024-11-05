import subprocess, os
from ..util import print_log


class VideoResize:
    def __init__(self, filename):
        self.filename = filename

    def resize(self):
        print_log("Video resizing started.")
        video_path = f"data/video/{self.filename}.mp4"
        temp_output_video = f"data/video/temp_{self.filename}.mp4"
        try:
            # FFmpeg 명령어를 subprocess로 실행
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video_path,
                    "-vf",
                    "crop=iw*3/4:ih,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                    "-c:a",
                    "copy",
                    temp_output_video,
                ],
                check=True,
            )
            os.replace(temp_output_video, video_path)
            print_log("Video resized successfully.")
        except Exception as e:
            raise Exception(e)
