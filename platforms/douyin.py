import requests
import re
from core.platform import PlatformParser, VideoInfo

class DouyinParser(PlatformParser):
    def parse(self, url: str) -> VideoInfo:
        resp = requests.get('https://api.bugpk.com/api/douyin', params={'url': url})
        data = resp.json()
        if data['code'] != 200:
            raise Exception(data['msg'])

        video_data = data['data']
        raw_title = video_data['title']

        # 提取 # 开头的关键字
        hashtags = re.findall(r'#([^#\s]+)', raw_title)

        # 清理标题：移除 # 标签，截断到50字
        clean_title = re.sub(r'#[^\s]+', '', raw_title).strip()
        if len(clean_title) > 50:
            clean_title = clean_title[:50] + '...'

        video_info = VideoInfo(
            title=clean_title if clean_title else raw_title[:50],
            audio_url=video_data['music']['url'],
            platform='douyin'
        )
        video_info.hashtags = hashtags
        return video_info
