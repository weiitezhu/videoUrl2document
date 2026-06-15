# 抖音视频转文档

将抖音视频自动转换为文本文档，支持批量处理和多种转录服务。

## ✨ 特性

- 🎬 **抖音视频解析**：自动提取标题、音频和话题标签
- 🗣️ **多种转录服务**：
  - 阿里云听悟 API（云端，高准确度）
  - 本地 Whisper（离线，保护隐私）
- 🚀 **批量处理**：支持多线程并发处理
- 🤖 **Claude Code Skill**：在 AI 对话中一键使用
- 📝 **Markdown 输出**：包含关键词和格式化内容

## 🏗️ 架构设计

```
videoUrl2document/
├── core/                    # 核心抽象层
│   ├── platform.py          # 平台解析接口
│   ├── transcribe.py        # 转录服务接口
│   ├── storage.py           # 存储层
│   └── task.py              # 任务调度器（多线程）
├── platforms/               # 平台实现
│   └── douyin.py            # 抖音解析器
├── services/                # 转录服务实现
│   ├── aliyun_tingwu.py     # 阿里云听悟 API
│   └── local_whisper.py     # 本地 Whisper（GPU/CPU）
├── dy2text-skill/           # Claude Code 自定义 Skill
│   ├── dy2text.py           # Skill 主程序
│   ├── setup.py             # 一键安装脚本
│   └── *.md                 # 文档
├── main.py                  # 单任务入口（已弃用）
├── batch.py                 # 批量处理（阿里云）
└── batch_local.py           # 批量处理（本地 Whisper）
```

## 🚀 快速开始

### 方式 1：Claude Code Skill（推荐）

**一键安装：**
```bash
python dy2text-skill/setup.py
```

**使用（需重启 Claude Code）：**
```
/dy2text https://v.douyin.com/xxxxx/
/dy2text urls.txt
```

详见：[dy2text-skill/QUICKSTART.md](dy2text-skill/QUICKSTART.md)

### 方式 2：命令行脚本

**安装依赖：**
```bash
pip install -r requirements.txt
```

**配置（使用阿里云）：**
```bash
cp .env.example .env
# 编辑 .env 填入阿里云凭证
```

**运行：**
```bash
# 使用阿里云听悟
python batch.py urls.txt

# 使用本地 Whisper（需安装 FFmpeg）
python batch_local.py urls.txt
```

## 📋 环境配置

### 使用阿里云听悟（云 API）

编辑 `.env` 文件：
```env
ALIYUN_ACCESS_KEY_ID=your_access_key_id
ALIYUN_ACCESS_KEY_SECRET=your_access_key_secret
ALIYUN_APPKEY=your_tingwu_appkey
```

### 使用本地 Whisper（免费）

**依赖：**
1. 安装 FFmpeg：
   ```bash
   choco install ffmpeg  # Windows
   ```

2. 安装 Whisper（二选一）：
   ```bash
   # GPU 版本（推荐，需要 NVIDIA 显卡）
   pip install faster-whisper
   
   # CPU 版本
   pip install openai-whisper
   ```

详见：[README_WHISPER.md](README_WHISPER.md)

## 📖 使用示例

### 单个 URL

```bash
python batch.py "https://v.douyin.com/2riL8TmD5Ps/"
```

### 批量处理（命令行）

```bash
python batch.py "url1" "url2" "url3"
```

### 批量处理（文件）

创建 `urls.txt`，每行一个链接：
```
https://v.douyin.com/url1/
https://v.douyin.com/url2/
https://v.douyin.com/url3/
```

运行：
```bash
python batch.py urls.txt
```

### 输出示例

保存到 `./output/{标题}.md`：

```markdown
# 奥德赛时期｜愿我们都能游过那片海🌊

## 关键词

`碎碎念`, `talk`, `治愈`, `#抖音热点`

## 内容

这是一段关于奥德赛时期的分享...
（转录的完整文本）
```

## 🔧 扩展开发

### 扩展新平台

实现 `core.platform.PlatformParser` 接口：

```python
from core.platform import PlatformParser, VideoInfo

class BilibiliParser(PlatformParser):
    def parse(self, url: str) -> VideoInfo:
        # 实现 B 站解析逻辑
        return VideoInfo(
            title="视频标题",
            audio_url="https://...",
            platform="bilibili",
            hashtags=["标签1", "标签2"]
        )
```

### 扩展新转录服务

实现 `core.transcribe.TranscribeService` 接口：

```python
from core.transcribe import TranscribeService, TranscribeResult

class AzureSpeech(TranscribeService):
    def submit(self, audio_url: str) -> str:
        # 提交转录任务
        return "task_id"
    
    def get_result(self, task_id: str) -> TranscribeResult:
        # 获取转录结果（自动轮询）
        return TranscribeResult(
            text="转录文本",
            keywords=["关键词1", "关键词2"]
        )
```

## 📚 文档

- [Claude Code Skill 快速开始](dy2text-skill/QUICKSTART.md)
- [本地 Whisper 配置指南](README_WHISPER.md)
- [架构说明](CLAUDE.md)

## 🛠️ 技术栈

- **语言**：Python 3.7+
- **核心库**：requests, python-dotenv
- **转录服务**：
  - 阿里云 SDK (`aliyun-python-sdk-core`)
  - faster-whisper / openai-whisper
  - jieba（中文分词）
- **任务调度**：ThreadPoolExecutor（多线程）

## 📊 性能对比

| 转录服务 | 准确度 | 速度 | 成本 | 隐私 |
|---------|--------|------|------|------|
| 阿里云听悟 | ⭐⭐⭐⭐⭐ | 快 | 按量计费 | 云端 |
| Whisper (GPU) | ⭐⭐⭐⭐ | 很快 | 免费 | 本地 |
| Whisper (CPU) | ⭐⭐⭐⭐ | 较慢 | 免费 | 本地 |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可

MIT License

---

**提示**：推荐使用 Claude Code Skill 方式，一键安装，随时可用！
