from models import SubtitleAdderDto
from core.subtitleAdder import SubtitleAdder
from core.videoResize import VideoResize
from crud import save_to_s3
from util import download_video, smtp_callback
import uuid, os


class SubtitleProcessor:
    def __init__(self, dto: SubtitleAdderDto):
        self.dto = dto
        self.filename = str(uuid.uuid4())
        self.dir = [
            ["video", f"{self.filename}.mp4"],
            ["video", f"resize_{self.filename}.mp4"],
            ["video", f"resize_{self.filename}"],
            ["audio", f"audio-resize_{self.filename}.wav"],
            ["subtitle", f"sub-resize_{self.filename}.srt"],
            ["output", f"output-resize_{self.filename}.mp4"],
        ]

    def download_video(self):
        download_video(self.filename, self.dto.url)

    def resize_video(self):
        resizer = VideoResize()
        resizer.resize(self.filename)

    def add_subtitle(self):
        adder = SubtitleAdder(self.filename)
        adder.subtitleAdder()

    def save_video(self):
        save_to_s3(self.filename, self.dto)

    def send_email(self):
        smtp_callback(self.dto.email)

    def delete_remain_files(self):
        for _dir, _filename in self.dir:
            if os.path.exists(f"data/{_dir}/{_filename}"):
                os.remove(f"data/{_dir}/{_filename}")

    def process(self):
        try:
            self.download_video()
            self.resize_video()
            self.add_subtitle()
            self.save_video()
            self.send_email()
        except:
            # delete remain files
            self.delete_remain_files()
            return
