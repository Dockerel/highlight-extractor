from ..models import HighlightExtractorDto
from ..core.sendMail import SendMail
from ..core.downloadVideo import DownloadVideo
from ..core.subtitleAdder import SubtitleAdder
from ..core.videoResize import VideoResize
from ..core.highlightExtractor import HighlightExtractor
from ..core.status_manager import set_status, delete_status
from ..crud import CRUD
from ..util import print_log
import uuid, os, glob

processing_status = {}

class HighlightProcessor:
    def __init__(self, dto: HighlightExtractorDto, task_id: str):
        self.dto = dto
        self.task_id = task_id
        self.filename = str(uuid.uuid4())
        self.dir = [
            ["audio", f"{self.filename}.wav"],
            ["concat", f"{self.filename}.txt"],
            ["subtitle", f"{self.filename}.srt"],
            ["video", f"{self.filename}.mp4"],
        ]

        set_status(self.task_id, "started")

    def update_status(self, status):
        set_status(self.task_id, status)

    def download_video(self):
        self.update_status("downloading video")
        downloader = DownloadVideo(self.filename, self.dto.url)
        downloader.download_video()

    def resize_video(self):
        self.update_status("resizing video")
        resizer = VideoResize(self.filename)
        resizer.resize()

    def add_subtitle(self):
        self.update_status("adding subtitle")
        adder = SubtitleAdder(self.filename)
        adder.subtitleAdder()

    def extract_highlights(self):
        self.update_status("extracting highlights")
        extractor = HighlightExtractor(self.filename,1)
        extractor.run()

    def save_video(self):
        self.update_status("saving video to S3")
        saver = CRUD(self.filename, self.dto)
        saver.save_to_s3()

    def send_email(self):
        sender = SendMail(self.dto.email)
        sender.smtp_callback()

    def delete_remain_files(self):
        # self.update_status("cleaning up files")
        for _dir, _filename in self.dir:
            if os.path.exists(f"data/{_dir}/{_filename}"):
                os.remove(f"data/{_dir}/{_filename}")

        for file_path in glob.glob(f"data/clip/{self.filename}_*.mp4"):
            os.remove(file_path)

        for file_path in glob.glob(f"data/output/{self.filename}_*.mp4"):
            os.remove(file_path)

    def process(self):
        try:
            self.update_status("processing started")
            self.download_video()
            self.resize_video()
            self.add_subtitle()
            self.extract_highlights()
            self.save_video()
            self.update_status("completed")
            self.send_email()
        except Exception as e:
            print_log(e, 1)
            self.update_status("failed")
        finally:
            self.delete_remain_files()
            return
