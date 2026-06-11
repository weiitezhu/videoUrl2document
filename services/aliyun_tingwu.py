import json
import time
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from core.transcribe import TranscribeService, TranscribeResult

class AliyunTingwu(TranscribeService):
    def __init__(self, access_key_id: str, access_key_secret: str, app_key: str):
        self.client = AcsClient(access_key_id, access_key_secret, 'cn-beijing')
        self.app_key = app_key

    def submit(self, audio_url: str) -> str:
        req = CommonRequest()
        req.set_accept_format('json')
        req.set_domain('tingwu.cn-beijing.aliyuncs.com')
        req.set_version('2023-09-30')
        req.set_protocol_type('https')
        req.set_method('PUT')
        req.set_uri_pattern('/openapi/tingwu/v2/tasks')
        req.add_query_param('type', 'offline')
        req.add_header('Content-Type', 'application/json')

        req.set_content(json.dumps({
            'AppKey': self.app_key,
            'Input': {'SourceLanguage': 'cn', 'FileUrl': audio_url},
            'Parameters': {'TextPolishEnabled': True}
        }).encode('utf-8'))

        resp = json.loads(self.client.do_action_with_exception(req))
        return resp['Data']['TaskId']

    def get_result(self, task_id: str) -> TranscribeResult:
        while True:
            req = CommonRequest()
            req.set_accept_format('json')
            req.set_domain('tingwu.cn-beijing.aliyuncs.com')
            req.set_version('2023-09-30')
            req.set_protocol_type('https')
            req.set_method('GET')
            req.set_uri_pattern(f'/openapi/tingwu/v2/tasks/{task_id}')

            resp = json.loads(self.client.do_action_with_exception(req))
            data = resp['Data']

            if data['TaskStatus'] == 'COMPLETED':
                return self._parse_result(data['Result'])
            if data['TaskStatus'] == 'FAILED':
                raise Exception(data.get('ErrorMessage', '识别失败'))

            time.sleep(10)

    def _parse_result(self, result: dict) -> TranscribeResult:
        text = ""
        keywords = []

        text_polish = result.get('TextPolish')
        if text_polish:
            text = self._parse_text_polish(text_polish)

        meeting = result.get('MeetingAssistance')
        if meeting:
            keywords = self._parse_keywords(meeting)

        return TranscribeResult(text=text, keywords=keywords)

    def _parse_text_polish(self, url: str) -> str:
        data = requests.get(url).json()
        paragraphs = [item['FormalParagraphText'] for item in data.get('TextPolish', []) if item.get('FormalParagraphText')]
        return '\n\n'.join(paragraphs)

    def _parse_keywords(self, url: str) -> list:
        data = requests.get(url).json()
        return data.get('MeetingAssistance', {}).get('Keywords', [])
