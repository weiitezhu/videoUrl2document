import sys
from pathlib import Path
from dotenv import load_dotenv
import os

from core.task import TaskProcessor
from core.storage import Storage
from platforms.douyin import DouyinParser
from services.aliyun_tingwu import AliyunTingwu

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print('用法: python batch.py <链接1> [链接2] [链接3] ...')
        print('或: python batch.py urls.txt')
        sys.exit(1)

    # 解析输入
    if Path(sys.argv[1]).exists():
        urls = Path(sys.argv[1]).read_text(encoding='utf-8').strip().split('\n')
    else:
        urls = sys.argv[1:]

    # 过滤有效的抖音链接
    import re
    douyin_pattern = r'https?://[^\s]*(?:douyin\.com|v\.douyin\.com)'
    urls = [url.strip() for url in urls if re.search(douyin_pattern, url.strip())]

    if not urls:
        print('错误: 没有找到有效的抖音链接')
        sys.exit(1)

    # 初始化组件
    parser = DouyinParser()
    service = AliyunTingwu(
        os.getenv('ALIYUN_ACCESS_KEY_ID'),
        os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
        os.getenv('ALIYUN_APPKEY')
    )
    storage = Storage('./output')
    processor = TaskProcessor(parser, service, storage)

    # 执行任务
    print(f"开始处理 {len(urls)} 个任务...")
    results = processor.process_batch(urls, max_workers=3)

    # 统计结果
    success = sum(1 for _, result, err in results if err is None)
    print(f"\n完成: {success}/{len(urls)}")

if __name__ == '__main__':
    main()
