import subprocess, os
from util import print_log


class VideoResize:
    def __init__(self):
        pass

    def resize(self, filename):
        new_filename = f"resize_{filename}"
        input_video = f"data/video/{filename}.mp4"
        try:
            # FFmpeg 명령어를 subprocess로 실행
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    input_video,
                    "-vf",
                    "crop=iw*3/4:ih,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                    "-c:a",
                    "copy",
                    f"data/video/{new_filename}.mp4",
                ],
                check=True,
            )
            os.remove(input_video)
            os.rename(f"data/video/{new_filename}.mp4", f"data/video/{new_filename}")
            print_log("Video resized successfully.")
        except Exception as e:
            print_log(e, 1)
            raise Exception
