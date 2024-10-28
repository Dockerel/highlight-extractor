from models import SubtitleAdderDto
from core.subtitleAdder import SubtitleAdder
from core.videoResize import VideoResize
from crud import save_to_s3
from util import download_video, smtp_callback


class SubtitleProcessor:
    def __init__(self, dto: SubtitleAdderDto):
        self.dto = dto
        self.filename = None
        self.resized_filename = None
        self.output_filename = None

    def download_video(self):
        self.filename = download_video(self.dto.url)

    def resize_video(self):
        resizer = VideoResize()
        self.resized_filename = resizer.resize(self.filename)

    def add_subtitle(self):
        adder = SubtitleAdder(self.resized_filename)
        self.output_filename = adder.subtitleAdder()

    def save_video(self):
        save_to_s3(self.output_filename, self.dto)

    def send_email(self):
        smtp_callback(self.dto.email)

    def delete_remain_files(self):
        pass

    def process(self):
        try:
            self.download_video()
            self.resize_video()
            self.add_subtitle()
            self.save_video()
            self.send_email()
        except:
            # delete remain files
            return
