import os, re, ffmpeg, glob
from openai import OpenAI
from dotenv import load_dotenv
from ..util import print_log

# OpenAI API 키 설정
load_dotenv()


class HighlightExtractor:
    def __init__(self, filename, mode=0):
        self.filename = filename
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.mode = mode

    def load_script(self):
        script = []
        with open(f"data/subtitle/{self.filename}.srt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if re.match(r"^\d+$", line):
                time_line = lines[i + 1].strip()
                text_lines = []
                j = i + 2
                while j < len(lines) and lines[j].strip():
                    text_lines.append(lines[j].strip())
                    j += 1
                text = " ".join(text_lines)

                start_str, end_str = time_line.split(" --> ")
                start = self.parse_srt_time(start_str)
                end = self.parse_srt_time(end_str)

                script.append({"start": start, "end": end, "text": text})
                i = j
            else:
                i += 1
        return script

    @staticmethod
    def parse_srt_time(time_str):
        hours, minutes, seconds = time_str.split(":")
        seconds = seconds.replace(",", ".")
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    # 하이라이트 추출 후
    def extract_highlights(self, script):
        """주어진 모드에 따라 하이라이트 구간을 추출합니다."""
        script_text = "\n".join(
            f"[{entry['start']}초 - {entry['end']}초] {entry['text']}"
            for entry in script
        )
        # "summarize_to_1_minute"
        if self.mode == 0:
            prompt = (
                "다음은 영상의 스크립트입니다. 영상 전체에서 흥미롭거나 유용한 정보가 포함된 구간을 찾아, "
                "구간의 총 합이 **최대 1분**이 되도록 여러 구간을 선택해 하이라이트를 구성해 주세요. 1분 30초를 넘어서는 절대 안됩니다. "
                "각 구간은 자연스럽게 이어져야 하고, 구간의 시작과 끝을 포함하는 하나의 하이라이트 리스트를 반환해 주세요.\n\n"
                "하이라이트 형식 예시:\n"
                "[[시작, 끝], [시작, 끝], ...]\n"
                "스크립트는 다음과 같습니다.\n"
                f"{script_text}\n\n"
                "또한 이때 설명하는 말 없이 하이라이트를 파이썬 리스트 형식으로 반환하되, 리스트의 이름이나 기타 등등 필요 없이 리스트만 반환해야 합니다.."
            )
        # "extract_1_minute"
        elif self.mode == 1:
            prompt = (
                "다음 스크립트에서 재미있는 부분이나 유용한 정보가 포함된 **1분 길이의 구간 단 하나**를 추출하세요. 구간 여러개를 추출해서는 절대 안됩니다. "
                "즉, 반환해야하는 하이라이트 형식은 단 하나여야 합니다. "
                "이때 길이가 1분이 되어야 함에 주의해야 합니다."
                "하이라이트 형식 예시:\n"
                "[시작, 시작 + 60s]\n"
                "스크립트는 다음과 같습니다.\n"
                f"{script_text}\n\n"
                "또한 이때 설명하는 말 없이 하이라이트를 파이썬 리스트 형식으로 반환하되, 리스트의 이름이나 기타 등등 필요 없이 리스트만 반환해야 합니다.."
            )
        else:
            raise ValueError(
                "Invalid mode. Choose '[0] : summarize_to_1_minute' or '[1] : extract_1_minute_segment'."
            )

        highlights = []
        client = OpenAI(api_key=self.api_key)
        for i in range(5):  # API 호출을 5번 반복
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an assistant that extracts highlights from scripts.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            highlight = response.choices[0].message.content
            highlights.append(eval(highlight))

        return highlights

    @staticmethod
    def remove_duplicates_and_validate(highlights, min_duration=40):
        unique_highlights = []

        for segment in highlights:
            if isinstance(segment[0], list):  # 하이라이트가 여러 구간으로 구성된 경우
                unique_segment = []
                total_duration = 0

                for sub_segment in segment:
                    if sub_segment not in unique_segment:
                        unique_segment.append(sub_segment)
                        start, end = sub_segment
                        total_duration += end - start

                if total_duration >= min_duration:
                    unique_highlights.append(unique_segment)

            else:  # 단일 구간으로 이루어진 경우
                start, end = segment
                duration = end - start

                if segment not in unique_highlights and duration >= min_duration:
                    unique_highlights.append(segment)

        return unique_highlights

    def video_cut_concat(self, highlights):
        for i in range(5):
            file = open(f"data/concat/{self.filename}.txt", "w")
            highlight = highlights[i]
            for j in range(len(highlight)):
                timestamp = highlight[j]
                output_path = f"data/clip/{self.filename}_{j}.mp4"
                stream = (
                    ffmpeg.input(
                        f"data/video/{self.filename}.mp4",
                        ss=timestamp[0],
                        to=timestamp[1],
                    )
                    .output(
                        output_path,
                        vcodec="h264_nvenc",
                        acodec="copy"
                    )
                    .global_args("-hwaccel", "cuda")
                )
                ffmpeg.run(stream, overwrite_output=True)
                file.write(f"file ../clip/{self.filename}_{j}.mp4\n")
            file.close()

            # concat
            (
                ffmpeg.input(
                    f"data/concat/{self.filename}.txt", format="concat", safe=0
                )
                .output(f"data/output/{self.filename}_{i}.mp4", c="copy")
                .run(overwrite_output=True)
            )
            os.remove(f"data/concat/{self.filename}.txt")
            for file_path in glob.glob(f"data/clip/{self.filename}_*.mp4"):
                os.remove(file_path)

    def video_cut(self, highlights):
        print(highlights)
        for i in range(5):
            timestamp = highlights[i]
            # [[0.0, 60.0], [[90.94, 150.94]], [92.58, 152.58], [92.58, 152.58], [91.94, 151.94]]
            # [[72.84, 132.84], [92.58, 152.58], [[90.94, 150.94]], [124.54, 184.54], [[72.84, 132.84]]]
            # 와 같이 timestamp의 depth가 일정하지 않은 버그
            if len(timestamp)!=2:
                timestamp=timestamp[0]
            output_path = f"data/output/{self.filename}_{i}.mp4"
            stream = (
                ffmpeg.input(
                    f"data/video/{self.filename}.mp4", ss=timestamp[0], to=timestamp[1]
                )
                .output(
                    output_path,
                    vcodec="h264_nvenc",
                    acodec="copy"
                )
                .global_args("-hwaccel", "cuda")
            )
            ffmpeg.run(stream, overwrite_output=True)

    # 비디오 자르는 코드
    def return_short_videos(self, highlights):
        if self.mode == 0:
            self.video_cut_concat(highlights)
        else:
            self.video_cut(highlights)

    def run(self):
        print_log("Highlights extraction started.")
        try:
            script = self.load_script()
            highlights = self.extract_highlights(script)
            # 하이라이트가 5개보다 적어지는 현상 발생
            # highlights = self.remove_duplicates_and_validate(highlights)
            self.return_short_videos(highlights)
            print_log("Highlights extracted successfully.")
        except Exception as e:
            raise Exception(e)

