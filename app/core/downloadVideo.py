import requests
from util import print_log


class DownloadVideo:
    def __init__(self, filename, url):
        self.filename = filename
        self.url = url

    def download_video(self):
        try:
            r = requests.get(self.url)
            with open(f"data/video/{self.filename}.mp4", "wb") as outfile:
                outfile.write(r.content)
            print_log("Video downloaded successfully.")
        except Exception as e:
            print_log(e, 1)
            raise Exception
