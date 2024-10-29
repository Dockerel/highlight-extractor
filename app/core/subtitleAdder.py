import os, ffmpeg, math
from faster_whisper import WhisperModel
from util import print_log


class SubtitleAdder:

    def __init__(self, filename):
        self.filename = "resize_" + filename
        self.audio_path = "data/audio"
        self.output_path = "data/output"
        self.subtitle_path = "data/subtitle"
        self.video_path = "data/video"

    def extract_audio(self, input_file):
        extracted_audio = f"audio-{input_file}.wav"
        stream = ffmpeg.input(f"{self.video_path}/{input_file}")
        stream = ffmpeg.output(stream, f"{self.audio_path}/{extracted_audio}")
        ffmpeg.run(stream, overwrite_output=True)
        return extracted_audio

    def transcribe(self, audio):
        model = WhisperModel("medium", device="cpu")
        segments, info = model.transcribe(f"{self.audio_path}/{audio}")
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
        with open(f"{self.subtitle_path}/{subtitle_file}", "w", encoding="utf-8") as f:
            f.write(text)

        return subtitle_file

    def add_subtitle_to_video(self, input_file, subtitle_file):
        video_input_stream = ffmpeg.input(f"{self.video_path}/{input_file}")
        output_video = f"output-{input_file}.mp4"
        stream = ffmpeg.output(
            video_input_stream,
            f"{self.output_path}/{output_video}",
            vf=f"subtitles='{self.subtitle_path}/{subtitle_file}'",
        )
        ffmpeg.run(stream, overwrite_output=True)
        return output_video

    def remove_files(self, filename, language):
        os.remove(f"{self.audio_path}/audio-{filename}.wav")
        os.remove(f"{self.subtitle_path}/sub-{filename}.{language}.srt")
        os.remove(f"{self.video_path}/{filename}")

    def subtitleAdder(self):
        try:
            filename = self.filename
            audio_file = self.extract_audio(filename)
            language, segments = self.transcribe(audio_file)
            subtitle_file = self.generate_subtitle_file(filename, language, segments)
            self.add_subtitle_to_video(filename, subtitle_file)
            self.remove_files(filename, language)
            print_log("Subtitle added successfully.")
        except Exception as e:
            print_log(e, 1)
            raise Exception
