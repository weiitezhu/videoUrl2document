from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class TranscribeResult:
    text: str
    keywords: list

class TranscribeService(ABC):
    @abstractmethod
    def submit(self, audio_url: str) -> str:
        """提交转录任务，返回任务ID"""
        pass

    @abstractmethod
    def get_result(self, task_id: str) -> TranscribeResult:
        """获取转录结果，自动轮询直到完成"""
        pass
