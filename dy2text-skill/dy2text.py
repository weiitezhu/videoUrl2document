"""
Douyin to Text Skill - Main Implementation

This skill converts Douyin video URLs to text documents with transcription.
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from core.task import TaskProcessor
from core.storage import Storage
from platforms.douyin import DouyinParser


def check_aliyun_credentials():
    """Check if Aliyun credentials are configured"""
    return all([
        os.getenv('ALIYUN_ACCESS_KEY_ID'),
        os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
        os.getenv('ALIYUN_APPKEY')
    ])


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def parse_input(args):
    """Parse input arguments to extract URLs"""
    if not args:
        return []

    # Check if first arg is a file
    if len(args) == 1 and Path(args[0]).exists():
        urls = Path(args[0]).read_text(encoding='utf-8').strip().split('\n')
    else:
        urls = args

    # Filter valid Douyin URLs
    import re
    douyin_pattern = r'https?://[^\s]*(?:douyin\.com|v\.douyin\.com)'
    urls = [url.strip() for url in urls if re.search(douyin_pattern, url.strip())]

    return urls


def main(args):
    """Main entry point for the skill"""
    load_dotenv(project_root / '.env')

    # Parse URLs
    urls = parse_input(args)
    if not urls:
        print('❌ 错误: 没有找到有效的抖音链接')
        print('\n用法:')
        print('  /dy2text https://v.douyin.com/xxxxx/')
        print('  /dy2text url1 url2 url3')
        print('  /dy2text urls.txt')
        return 1

    print(f"找到 {len(urls)} 个有效链接")

    # Choose transcription service
    parser = DouyinParser()

    if check_aliyun_credentials():
        print("✓ 使用阿里云听悟 API")
        from services.aliyun_tingwu import AliyunTingwu
        service = AliyunTingwu(
            os.getenv('ALIYUN_ACCESS_KEY_ID'),
            os.getenv('ALIYUN_ACCESS_KEY_SECRET'),
            os.getenv('ALIYUN_APPKEY')
        )
        max_workers = 3
    else:
        print("⚠ 未配置阿里云凭证，使用本地 Whisper")

        if not check_ffmpeg():
            print("❌ 错误: 未安装 FFmpeg")
            print("请安装 FFmpeg: choco install ffmpeg")
            return 1

        try:
            from services.local_whisper import LocalWhisper
            service = LocalWhisper(model_size="base")
            max_workers = 2
        except ImportError as e:
            print(f"❌ 错误: {e}")
            print("\n请安装 Whisper:")
            print("  GPU: pip install faster-whisper")
            print("  CPU: pip install openai-whisper")
            return 1

    # Process videos
    storage = Storage(project_root / 'output')
    processor = TaskProcessor(parser, service, storage)

    print(f"\n开始处理 {len(urls)} 个任务...")
    print("=" * 60)
    results = processor.process_batch(urls, max_workers=max_workers)

    # Report results
    success = sum(1 for _, result, err in results if err is None)
    print("=" * 60)
    print(f"\n✓ 完成: {success}/{len(urls)}")

    if success < len(urls):
        print(f"⚠ 失败: {len(urls) - success} 个任务")
        for url, _, err in results:
            if err:
                print(f"  - {url}: {err}")

    return 0 if success > 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
