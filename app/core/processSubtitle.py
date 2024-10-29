from models import SubtitleAdderDto
from core.sendMail import SendMail
from core.downloadVideo import DownloadVideo
from core.subtitleAdder import SubtitleAdder
from core.videoResize import VideoResize
from crud import CRUD
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
        downloader = DownloadVideo(self.filename, self.dto.url)
        downloader.download_video()

    def resize_video(self):
        resizer = VideoResize(self.filename)
        resizer.resize()

    def add_subtitle(self):
        adder = SubtitleAdder(self.filename)
        adder.subtitleAdder()

    def save_video(self):
        saver = CRUD(self.filename, self.dto)
        saver.save_to_s3()

    def send_email(self):
        sender = SendMail(self.dto.email)
        sender.smtp_callback()

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
