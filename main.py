import requests
import time
import sys
import json
from pathlib import Path
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from dotenv import load_dotenv
import os

load_dotenv()

client = AcsClient(
    os.getenv('ALIYUN_ACCESS_KEY_ID'),
    os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
    'cn-beijing'
)

def parse_douyin(url):
    resp = requests.get('https://api.bugpk.com/api/douyin', params={'url': url})
    data = resp.json()
    if data['code'] != 200:
        raise Exception(data['msg'])
    return data['data']

def submit_task(audio_url):
    req = CommonRequest()
    req.set_accept_format('json')
    req.set_domain('tingwu.cn-beijing.aliyuncs.com')
    req.set_version('2023-09-30')
    req.set_protocol_type('https')
    req.set_method('PUT')
    req.set_uri_pattern('/openapi/tingwu/v2/tasks')
    req.add_query_param('type', 'offline')
    req.add_header('Content-Type', 'application/json')
    
    parameters = get_parameters()
    
    req.set_content(json.dumps({
        'AppKey': os.getenv('ALIYUN_APPKEY'),
        'Input': {'SourceLanguage': 'cn', 'FileUrl': audio_url},
        "Parameters": parameters
    }).encode('utf-8'))

    resp = json.loads(client.do_action_with_exception(req))
    return resp['Data']['TaskId']

def get_parameters():
    parameters = dict()
    # 口语书面化
    parameters['TextPolishEnabled'] = True
    # parameters["MeetingAssistanceEnabled"] = True
    # parameters["MeetingAssistance"] = dict()
    # parameters["MeetingAssistance"]["Types"] = ["Actions", "KeyInformation"]
    return parameters


def get_result(task_id):
    req = CommonRequest()
    req.set_accept_format('json')
    req.set_domain('tingwu.cn-beijing.aliyuncs.com')
    req.set_version('2023-09-30')
    req.set_protocol_type('https')
    req.set_method('GET')
    req.set_uri_pattern(f'/openapi/tingwu/v2/tasks/{task_id}')

    resp = json.loads(client.do_action_with_exception(req))
    return resp['Data']

def poll_result(task_id):
    while True:
        result = get_result(task_id)
        print(result)
        if result['TaskStatus'] == 'COMPLETED':
            return result
        if result['TaskStatus'] == 'FAILED':
            raise Exception(result.get('ErrorMessage', '识别失败'))
        print("等待任务完成！！")
        time.sleep(10)
    
def save_result(result):
    result = result.get("Result")
    Transcription = result.get("Transcription") # 原始数据
    TextPolish = result.get("TextPolish") # 段落转化
    Summarization = result.get("Summarization") # 全文摘要
    MeetingAssistance = result.get("MeetingAssistance") #关键字和重点内容
    if TextPolish is None:
        raise
    data = ""
    
    raw = ""
    
    key_world = []
    
    raw =  parsing_TextPolish(TextPolish)
    
    MeetingAssistance and parsing_MeetingAssistance(MeetingAssistance, key_world)

    save_to_file(raw, None, key_world)
    

def parsing_TextPolish(url):
    """请求 URL 获取 TextPolish JSON 数据并解析"""
    data = requests.get(url).json()
    paragraphs = []
    for item in data.get('TextPolish', []):
        text = item.get('FormalParagraphText', '')
        if text:
            paragraphs.append(text)
    return '\n\n'.join(paragraphs)

def parsing_MeetingAssistance(url, l_result: list):
    """请求 URL 获取 MeetingAssistance JSON 数据并提取关键词"""
    data = requests.get(url).json()
    keywords = data.get('MeetingAssistance', {}).get('Keywords', [])
    l_result.extend(keywords)

def save_to_file(raw, title, key_world=None, path="."):
    """保存文本内容和关键词到文件"""
    if key_world is None:
        key_world = []

    content = raw
    if key_world:
        content = f"关键词：{', '.join(key_world)}\n\n{raw}"

    filename = Path(path) / f"{int(time.time())}.txt"
    filename.write_text(content, encoding='utf-8')
    print(f"已保存到: {filename}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python main.py <抖音分享链接>')
        sys.exit(1)

    print('解析抖音链接...')
    video = parse_douyin(sys.argv[1])
    print(f"标题: {video['title']}")
    print(f"音频链接: {video['music']['url']}")

    print('提交语音识别...')
    task_id = submit_task(video['music']['url'])
    print(f"任务ID: {task_id}")

    print('等待识别结果...')
    result = poll_result(task_id)

    print("保存结果")
    save_result(result=result)
    # text = result.get('Result', {}).get('Transcription', {}).get('Sentences', [])
    # content = '\n'.join(s.get('Text', '') for s in text)
    # filename = f"{video['title'].translate(str.maketrans('', '', '/:*?\"<>|'))}.txt"
    # Path(filename).write_text(content, encoding='utf-8')
    # print(f"已保存到: {filename}")
