import requests
from core.platform import PlatformParser, VideoInfo

class DouyinParser(PlatformParser):
    def parse(self, url: str) -> VideoInfo:
        resp = requests.get('https://api.bugpk.com/api/douyin', params={'url': url})
        data = resp.json()
        if data['code'] != 200:
            raise Exception(data['msg'])

        video_data = data['data']
        return VideoInfo(
            title=video_data['title'],
            audio_url=video_data['music']['url'],
            platform='douyin'
        )
