from subtitle_adder import SubtitleAdder
from fastapi import FastAPI

adder = SubtitleAdder(
    "https://www.youtube.com/shorts/xSU8hKEHnLU",
    True,
)
adder.subtitleAdder()

app=FastAPI()

@app.post("") # 자막 추출하고 자막 입히는 기능을 따로 구현할까?
