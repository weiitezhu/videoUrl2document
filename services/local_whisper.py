import os
import tempfile
import requests
from pathlib import Path
from collections import Counter
from core.transcribe import TranscribeService, TranscribeResult

class LocalWhisper(TranscribeService):
    """本地 Whisper 转录服务

    自动检测 NVIDIA GPU：
    - 有 GPU: 使用 faster-whisper (更快)
    - 无 GPU: 使用 openai-whisper (标准版)

    依赖:
    - FFmpeg (必需)
    - faster-whisper (GPU 版本) 或 openai-whisper (CPU 版本)
    """

    def __init__(self, model_size: str = "base", device: str = "auto", compute_type: str = "auto"):
        """初始化 Whisper 服务

        Args:
            model_size: 模型大小 (tiny, base, small, medium, large, large-v2, large-v3)
            device: 设备选择 (auto, cuda, cpu)
            compute_type: 计算类型 (auto, float16, int8) - 仅 faster-whisper
        """
        self.model_size = model_size
        self.temp_dir = Path(tempfile.mkdtemp(prefix="whisper_"))

        # 自动检测使用哪个引擎
        self.use_faster_whisper = False
        if device == "auto":
            device = "cuda" if self._has_cuda() else "cpu"

        # 优先使用 faster-whisper (如果有 GPU)
        if device == "cuda":
            try:
                from faster_whisper import WhisperModel
                if compute_type == "auto":
                    compute_type = "float16"
                self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
                self.use_faster_whisper = True
                print(f"✓ 使用 faster-whisper ({device}, {compute_type})")
            except ImportError:
                print("⚠ faster-whisper 未安装，降级使用 openai-whisper")
                self._init_openai_whisper(device)
        else:
            self._init_openai_whisper(device)

    def _has_cuda(self) -> bool:
        """检测是否有可用的 CUDA GPU"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False

    def _init_openai_whisper(self, device: str):
        """初始化标准 openai-whisper"""
        try:
            import whisper
            self.model = whisper.load_model(self.model_size, device=device)
            print(f"✓ 使用 openai-whisper ({device})")
        except ImportError:
            raise ImportError(
                "请安装 Whisper:\n"
                "  GPU 版本: pip install faster-whisper\n"
                "  CPU 版本: pip install openai-whisper"
            )

    def submit(self, audio_url: str) -> str:
        """下载音频文件，返回本地路径作为 task_id"""
        print(f"正在下载音频: {audio_url}")

        # 下载音频文件
        response = requests.get(audio_url, stream=True, timeout=60)
        response.raise_for_status()

        # 保存到临时文件
        audio_path = self.temp_dir / "audio.mp3"
        with open(audio_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✓ 音频已下载: {audio_path}")
        return str(audio_path)

    def get_result(self, task_id: str) -> TranscribeResult:
        """执行 Whisper 转录"""
        audio_path = task_id
        print(f"开始转录: {audio_path}")

        if self.use_faster_whisper:
            return self._transcribe_faster_whisper(audio_path)
        else:
            return self._transcribe_openai_whisper(audio_path)

    def _transcribe_faster_whisper(self, audio_path: str) -> TranscribeResult:
        """使用 faster-whisper 转录"""
        segments, info = self.model.transcribe(
            audio_path,
            language="zh",
            vad_filter=True,  # 语音活动检测
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        print(f"✓ 检测到语言: {info.language} (概率: {info.language_probability:.2f})")

        # 收集所有文本段
        texts = []
        for segment in segments:
            texts.append(segment.text.strip())

        full_text = "\n\n".join(texts)
        keywords = self._extract_keywords(full_text)

        print(f"✓ 转录完成，共 {len(texts)} 段")
        return TranscribeResult(text=full_text, keywords=keywords)

    def _transcribe_openai_whisper(self, audio_path: str) -> TranscribeResult:
        """使用 openai-whisper 转录"""
        result = self.model.transcribe(
            audio_path,
            language="zh",
            verbose=False
        )

        full_text = result["text"].strip()
        keywords = self._extract_keywords(full_text)

        print(f"✓ 转录完成")
        return TranscribeResult(text=full_text, keywords=keywords)

    def _extract_keywords(self, text: str, top_k: int = 10) -> list:
        """关键词提取（优先使用 jieba，降级到词频统计）"""
        if not text.strip():
            return []

        # 尝试使用 jieba 的 TF-IDF 算法提取关键词
        try:
            import jieba.analyse
            keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=False)
            if keywords:
                return keywords
        except ImportError:
            pass  # jieba 未安装，使用备选方案

        # 备选方案：基于词频统计的简单提取
        import re
        # 移除标点符号，保留中文、英文和数字
        text = re.sub(r'[^一-龥a-zA-Z0-9\s]', ' ', text)

        # 简单分词（按空格分，适用于英文混合文本）
        words = text.split()

        # 扩展的停用词表
        stopwords = {
            '的', '了', '是', '在', '有', '和', '我', '你', '他', '她', '它',
            '这', '那', '也', '就', '都', '而', '及', '与', '或', '等', '对',
            '个', '人', '们', '中', '来', '大', '上', '下', '说', '去', '会',
            '能', '要', '着', '用', '从', '以', '把', '可以', '一个', '这个'
        }
        words = [w for w in words if len(w) >= 2 and w not in stopwords]

        if not words:
            return []

        # 统计词频并返回 top_k
        counter = Counter(words)
        keywords = [word for word, _ in counter.most_common(top_k)]

        return keywords

    def cleanup(self):
        """清理临时文件"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print(f"✓ 已清理临时文件: {self.temp_dir}")

    def __del__(self):
        """析构时自动清理"""
        try:
            self.cleanup()
        except:
            pass
