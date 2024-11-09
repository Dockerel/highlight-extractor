import whisper, os, ffmpeg, math
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
        # model = whisper.load_model("medium")
        model = whisper.load_model("medium").to("cuda")
        result = model.transcribe(
            f"{self.audio_path}/{self.filename}.wav", word_timestamps=True
        )
        segments = result["segments"]
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
            segment_start = self.format_time_for_srt(segment["start"])
            segment_end = self.format_time_for_srt(segment["end"])
            segment_text = segment["text"].strip()

            text += f"{str(index + 1)}\n"
            text += f"{segment_start} --> {segment_end}\n"
            text += f"{segment_text}\n\n"

        with open(f"{self.subtitle_path}/{subtitle_file}", "w", encoding="utf-8") as f:
            f.write(text)

    def add_subtitle_to_video(self):
        video_input_stream = ffmpeg.input(f"{self.video_path}/{self.filename}.mp4")
        temp_output_video = f"{self.video_path}/temp_{self.filename}.mp4"
        video_path = f"{self.video_path}/{self.filename}.mp4"

        subtitle_filter = (
            f"subtitles='{self.subtitle_path}/{self.filename}.srt':force_style="
            "'Alignment=2,Fontname=/usr/share/fonts/truetype/nanum/NanumGothic.ttf,"
            "Fontsize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
            "BackColour=&H00000000,BorderStyle=3,Outline=2'"
        )

        stream = ffmpeg.output(
            video_input_stream,
            f"{self.video_path}/temp_{self.filename}.mp4",
            vf=subtitle_filter,
            vcodec="h264_nvenc",  # 비디오 코덱으로 h264_nvenc 설정
            acodec="copy",
        ).global_args("-hwaccel", "cuda")
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
