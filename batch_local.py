import sys
from pathlib import Path
from dotenv import load_dotenv

from core.task import TaskProcessor
from core.storage import Storage
from platforms.douyin import DouyinParser
from services.local_whisper import LocalWhisper

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print('用法: python batch_local.py <链接1> [链接2] [链接3] ...')
        print('或: python batch_local.py urls.txt')
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

    # 初始化组件 - 使用本地 Whisper
    parser = DouyinParser()

    # 模型大小选项: tiny, base, small, medium, large, large-v2, large-v3
    # - tiny/base: 快速但准确度较低
    # - small/medium: 平衡速度和准确度 (推荐)
    # - large: 最高准确度但速度较慢
    service = LocalWhisper(model_size="base")  # 可改为 "small", "medium" 等

    storage = Storage('./output')
    processor = TaskProcessor(parser, service, storage)

    # 执行任务
    print(f"开始处理 {len(urls)} 个任务...")
    print("=" * 60)
    results = processor.process_batch(urls, max_workers=2)  # 本地转录建议降低并发数

    # 统计结果
    success = sum(1 for _, result, err in results if err is None)
    print("=" * 60)
    print(f"\n✓ 完成: {success}/{len(urls)}")

if __name__ == '__main__':
    main()
