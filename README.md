# 抖音视频转文档

将视频平台的内容转换为文本文档，支持批量处理。

## 架构设计

```
├── core/              # 核心抽象层
│   ├── platform.py    # 平台解析接口
│   ├── transcribe.py  # 转录服务接口
│   ├── storage.py     # 存储层
│   └── task.py        # 任务处理
├── platforms/         # 平台实现
│   └── douyin.py      # 抖音
├── services/          # 转录服务实现
│   └── aliyun_tingwu.py  # 阿里云通义听悟
├── main.py            # 单任务入口
└── batch.py           # 批量处理入口
```

## 安装

```bash
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 为 `.env` 并填入阿里云凭证：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
- `ALIYUN_ACCESS_KEY_ID`: 阿里云访问密钥ID
- `ALIYUN_ACCESS_KEY_SECRET`: 阿里云访问密钥Secret
- `ALIYUN_APPKEY`: 语音识别项目Appkey

## 使用

**单个任务：**
```bash
python main.py "https://v.douyin.com/xxxxx/"
```

**批量处理（命令行）：**
```bash
python batch.py "https://v.douyin.com/url1/" "https://v.douyin.com/url2/"
```

**批量处理（文件）：**
```bash
# 创建 urls.txt，每行一个链接
python batch.py urls.txt
```

结果保存在 `./output` 目录。

## 扩展其他平台

实现 `core.platform.PlatformParser` 接口：

```python
from core.platform import PlatformParser, VideoInfo

class BilibiliParser(PlatformParser):
    def parse(self, url: str) -> VideoInfo:
        # 实现B站解析逻辑
        return VideoInfo(title="...", audio_url="...", platform="bilibili")
```

## 扩展其他转录服务

实现 `core.transcribe.TranscribeService` 接口：

```python
from core.transcribe import TranscribeService, TranscribeResult

class OpenAIWhisper(TranscribeService):
    def submit(self, audio_url: str) -> str:
        # 实现提交逻辑
        pass
    
    def get_result(self, task_id: str) -> TranscribeResult:
        # 实现获取结果逻辑
        pass
```
