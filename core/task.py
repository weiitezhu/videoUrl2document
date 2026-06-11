from concurrent.futures import ThreadPoolExecutor, as_completed
from .platform import PlatformParser
from .transcribe import TranscribeService
from .storage import Storage

class TaskProcessor:
    def __init__(self, parser: PlatformParser, service: TranscribeService, storage: Storage):
        self.parser = parser
        self.service = service
        self.storage = storage

    def process_one(self, url: str):
        """处理单个任务"""
        print(f"[任务] 解析: {url}")
        video = self.parser.parse(url)

        print(f"[任务] 标题: {video.title}")
        print(f"[任务] 提交转录: {video.audio_url}")
        task_id = self.service.submit(video.audio_url)

        print(f"[任务] 任务ID: {task_id}")
        result = self.service.get_result(task_id)

        hashtags = getattr(video, 'hashtags', None)
        filename = self.storage.save(video.title, result.text, result.keywords, hashtags)
        print(f"[完成] {filename}")
        return filename

    def process_batch(self, urls: list, max_workers: int = 3):
        """批量处理任务"""
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.process_one, url): url for url in urls}
            for future in as_completed(futures):
                url = futures[future]
                try:
                    result = future.result()
                    results.append((url, result, None))
                except Exception as e:
                    print(f"[错误] {url}: {e}")
                    results.append((url, None, str(e)))
        return results
