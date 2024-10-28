import subprocess, os
from util import print_log


class VideoResize:
    def __init__(self):
        pass

    def resize(self, filename):
        new_filename = f"resize_{filename}".split(".")[0]
        input_video = f"data/video/{filename}"
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

            return new_filename
        except Exception as e:
            os.remove(input_video)
            print_log(e, 1)
            raise Exception
