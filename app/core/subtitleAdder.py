import os, uuid, requests, ffmpeg, math, re
from pytubefix import YouTube
from pytubefix.cli import on_progress
from faster_whisper import WhisperModel
from models import SubtitleAdderCallbackResponse


class SubtitleAdder:

    def __init__(self, url):
        self.url = url
        self.is_youtube = True
        self.post_callback_url = os.getenv("POST_CALLBACK_URL")

    def determine_is_youtube_url(self):
        pattern = re.compile(
            r"^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/(watch\?v=|embed\/|shorts\/|[\w-]+)?([\w-]{11})(\S*)$"
        )
        matcher = pattern.match(self.url)
        if matcher:
            self.is_youtube = True
            return
        self.is_youtube = False

    def download_youtube_video(self, url, filename):
        yt = YouTube(url, on_progress_callback=on_progress)
        ys = yt.streams.get_highest_resolution()
        video = ys.download(output_path="data/video")

        os.rename(video, "data/video/" + filename)

    def download_regular_video(self, url, filename):
        r = requests.get(url)
        with open("data/video/" + filename, "wb") as outfile:
            outfile.write(r.content)

    def download_video(self):
        unique_id = str(uuid.uuid4())
        if self.is_youtube:
            self.download_youtube_video(self.url, unique_id)
        else:
            self.download_regular_video(self.url, unique_id)
        return unique_id

    def extract_audio(self, input_file):
        extracted_audio = f"audio-{input_file}.wav"
        stream = ffmpeg.input("data/video/" + input_file)
        stream = ffmpeg.output(stream, "data/audio/" + extracted_audio)
        ffmpeg.run(stream, overwrite_output=True)
        return extracted_audio

    def transcribe(self, audio):
        model = WhisperModel("medium", device="cpu")
        segments, info = model.transcribe("data/audio/" + audio)
        language = info[0]
        segments = list(segments)
        return language, segments

    def format_time_for_srt(self, seconds):
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        miliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        formatted_time = (
            f"{hours :02d}:{minutes :02d}:{seconds :02d},{miliseconds :03d}"
        )

        return formatted_time

    def generate_subtitle_file(self, input_file, language, segments):
        subtitle_file = f"sub-{input_file}.{language}.srt"
        text = ""
        for index, segment in enumerate(segments):
            segment_start = self.format_time_for_srt(segment.start)
            segment_end = self.format_time_for_srt(segment.end)

            text += f"{str(index + 1)}\n"
            text += f"{segment_start} --> {segment_end}\n"
            text += f"{segment.text}\n\n"

        # UTF-8 인코딩으로 파일을 열기
        with open("data/subtitle/" + subtitle_file, "w", encoding="utf-8") as f:
            f.write(text)

        return subtitle_file

    def add_subtitle_to_video(self, input_file, subtitle_file):
        video_input_stream = ffmpeg.input("data/video/" + input_file)
        output_video = f"output-{input_file}.mp4"
        stream = ffmpeg.output(
            video_input_stream,
            "data/output/" + output_video,
            vf=f"subtitles='data/subtitle/{subtitle_file}'",
        )
        ffmpeg.run(stream, overwrite_output=True)
        return output_video

    def remove_files(self, unique_id, language):
        os.remove(f"data/audio/audio-{unique_id}.wav")
        os.remove(f"data/subtitle/sub-{unique_id}.{language}.srt")
        os.remove(f"data/video/{unique_id}")

    def subtitleAdder(self):
        self.determine_is_youtube_url()

        filename = self.download_video()

        audio_file = self.extract_audio(filename)

        language, segments = self.transcribe(audio_file)

        subtitle_file = self.generate_subtitle_file(filename, language, segments)

        output_filename = self.add_subtitle_to_video(filename, subtitle_file)

        self.remove_files(filename, language)

        return output_filename

    def callback_request(self, email, url, filename):
        data = SubtitleAdderCallbackResponse(email, url, filename)
        requests.post(self.post_callback_url, data)
