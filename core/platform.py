from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class VideoInfo:
    title: str
    audio_url: str
    platform: str

class PlatformParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> VideoInfo:
        pass
