import os, ffmpeg, math
from faster_whisper import WhisperModel
from ..util import print_log


class SubtitleAdder:

    def __init__(self, filename):
        self.filename = filename
        self.audio_path = "data/audio"
        self.subtitle_path = "data/subtitle"
        self.video_path = "data/video"
        self.output_path = "data/output"

    def extract_audio(self):
        extracted_audio = f"{self.filename}.wav"
        stream = ffmpeg.input(f"{self.video_path}/{self.filename}.mp4")
        stream = ffmpeg.output(stream, f"{self.audio_path}/{extracted_audio}")
        ffmpeg.run(stream, overwrite_output=True)

    def transcribe(self):
        model = WhisperModel("medium", device="cpu")
        segments, _ = model.transcribe(f"{self.audio_path}/{self.filename}.wav")
        segments = list(segments)
        return segments

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

    def generate_subtitle_file(self, segments):
        subtitle_file = f"{self.filename}.srt"
        text = ""
        for index, segment in enumerate(segments):
            segment_start = self.format_time_for_srt(segment.start)
            segment_end = self.format_time_for_srt(segment.end)

            text += f"{str(index + 1)}\n"
            text += f"{segment_start} --> {segment_end}\n"
            text += f"{segment.text}\n\n"

        with open(f"{self.subtitle_path}/{subtitle_file}", "w", encoding="utf-8") as f:
            f.write(text)

    def add_subtitle_to_video(self):
        video_input_stream = ffmpeg.input(f"{self.video_path}/{self.filename}.mp4")
        temp_output_video = f"{self.video_path}/temp_{self.filename}.mp4"
        video_path = f"{self.video_path}/{self.filename}.mp4"
        stream = ffmpeg.output(
            video_input_stream,
            f"{self.video_path}/temp_{self.filename}.mp4",
            vf=f"subtitles='{self.subtitle_path}/{self.filename}.srt'",
        )
        ffmpeg.run(stream, overwrite_output=True)
        os.replace(temp_output_video, video_path)

    def subtitleAdder(self):
        print_log("Subtitle adding started.")
        try:
            self.extract_audio()
            segments = self.transcribe()
            self.generate_subtitle_file(segments)
            self.add_subtitle_to_video()
            print_log("Subtitle added successfully.")
        except Exception as e:
            raise Exception(e)
