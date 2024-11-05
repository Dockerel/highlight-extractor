from ..models import SubtitleAdderDto
from ..core.sendMail import SendMail
from ..core.downloadVideo import DownloadVideo
from ..core.subtitleAdder import SubtitleAdder
from ..core.videoResize import VideoResize
from ..core.highlightExtractor import HighlightExtractor
from ..crud import CRUD
from ..util import print_log
import uuid, os, glob


class SubtitleProcessor:
    def __init__(self, dto: SubtitleAdderDto):
        self.dto = dto
        self.filename = str(uuid.uuid4())
        self.dir = [
            ["audio", f"{self.filename}.wav"],
            ["concat", f"{self.filename}.txt"],
            ["subtitle", f"{self.filename}.srt"],
            ["video", f"{self.filename}.mp4"],
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

    def extract_highlights(self):
        extractor = HighlightExtractor(self.filename)
        extractor.run()

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

        for file_path in glob.glob(f"data/clip/{self.filename}_*.mp4"):
            os.remove(file_path)

        for file_path in glob.glob(f"data/output/{self.filename}_*.mp4"):
            os.remove(file_path)

    def process(self):
        try:
            self.download_video()
            self.resize_video()
            self.add_subtitle()
            self.extract_highlights()
            self.save_video()
            self.send_email()
        except Exception as e:
            print_log(e, 1)
        finally:
            self.delete_remain_files()
            return
