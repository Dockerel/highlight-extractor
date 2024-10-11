from core.subtitleAdder import SubtitleAdder

urls = [
    "https://www.youtube.com/watch?v=ySrznInAJCk",
    "http://youtube.com/watch?v=ySrznInAJCk",
    "https://www.youtube.com/embed/ySrznInAJCk",
    "https://youtu.be/ySrznInAJCk",
    "https://youtu.be/ySrznInAJCk?t=9s",
    "https://www.youtube.com/shorts/ySrznInAJCk",
    "https://www.youtube.com/watch?v=ySrznInAJCk",
    "https://youtu.be/ySrznInAJCk",
    "https://www.youtube.com/shorts/ySrznInAJCk",
]


def test_youtube_url():
    for url in urls:
        adder = SubtitleAdder(url)
        adder.determine_is_youtube_url()
        assert adder.is_youtube == True
