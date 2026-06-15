# 本地 Whisper 转录服务

本项目支持使用本地 Whisper 模型进行语音转录，无需调用阿里云 API。

## 特性

- ✅ 自动检测 GPU：有 NVIDIA GPU 时自动使用 faster-whisper，否则使用标准 openai-whisper
- ✅ 多种模型大小：从 tiny 到 large-v3，平衡速度和准确度
- ✅ 完全本地化：无需网络 API，保护数据隐私
- ✅ 自动关键词提取：基于词频统计
- ✅ 中文优化：支持中文语音识别

## 依赖要求

### 1. FFmpeg（必需）

Whisper 依赖 FFmpeg 进行音频处理。

**Windows 安装：**
```bash
# 使用 Chocolatey
choco install ffmpeg

# 或者下载：https://ffmpeg.org/download.html
# 解压后将 bin 目录添加到系统 PATH
```

**验证安装：**
```bash
ffmpeg -version
```

### 2. Whisper 库（二选一）

#### 选项 A：faster-whisper（推荐，需要 GPU）

适用于有 NVIDIA GPU 的环境，速度更快：

```bash
# 安装 CUDA 版本的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 安装 faster-whisper
pip install faster-whisper
```

#### 选项 B：openai-whisper（CPU 友好）

适用于没有 GPU 或 CPU 环境：

```bash
pip install openai-whisper
```

### 3. 其他依赖

```bash
pip install jieba  # 中文分词，用于关键词提取
```

## 使用方法

### 单个 URL

```bash
python batch_local.py "https://v.douyin.com/xxxxx/"
```

### 批量处理（命令行）

```bash
python batch_local.py "url1" "url2" "url3"
```

### 批量处理（文件）

```bash
# urls.txt 每行一个 URL
python batch_local.py urls.txt
```

## 模型选择

在 `batch_local.py` 中可以修改模型大小：

```python
service = LocalWhisper(model_size="base")  # 改为其他大小
```

| 模型 | 大小 | 速度 | 准确度 | 推荐场景 |
|------|------|------|--------|----------|
| `tiny` | ~75MB | 最快 | 较低 | 快速测试 |
| `base` | ~150MB | 快 | 一般 | 日常使用（默认） |
| `small` | ~500MB | 中等 | 良好 | 平衡选择 |
| `medium` | ~1.5GB | 较慢 | 很好 | 高质量需求 |
| `large` | ~3GB | 慢 | 最佳 | 专业转录 |
| `large-v2` | ~3GB | 慢 | 最佳 | 最新优化 |
| `large-v3` | ~3GB | 慢 | 最佳 | 多语言优化 |

**首次运行**会自动下载模型到 `~/.cache/whisper/` 目录。

## 性能对比

| 环境 | 引擎 | 1 分钟音频耗时 |
|------|------|----------------|
| NVIDIA RTX 3090 | faster-whisper (float16) | ~10 秒 |
| CPU (Intel i7) | openai-whisper | ~60 秒 |

## 配置选项

在 `LocalWhisper` 初始化时可以自定义参数：

```python
service = LocalWhisper(
    model_size="base",      # 模型大小
    device="auto",          # 设备: "auto", "cuda", "cpu"
    compute_type="auto"     # 计算类型: "auto", "float16", "int8" (仅 faster-whisper)
)
```

## 故障排查

### 问题 1：找不到 FFmpeg

**症状：** `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**解决：** 确保 FFmpeg 已安装并在 PATH 中。运行 `ffmpeg -version` 验证。

### 问题 2：CUDA 不可用

**症状：** `torch.cuda.is_available()` 返回 `False`

**解决：** 
- 确认 NVIDIA 驱动已安装
- 重新安装 CUDA 版本的 PyTorch：
  ```bash
  pip uninstall torch
  pip install torch --index-url https://download.pytorch.org/whl/cu118
  ```

### 问题 3：内存不足

**症状：** `RuntimeError: CUDA out of memory`

**解决：**
- 使用更小的模型（如 `base` 或 `small`）
- 降低并发数（在 `batch_local.py` 中设置 `max_workers=1`）
- 使用 int8 量化：`compute_type="int8"`

### 问题 4：转录结果不准确

**解决：**
- 使用更大的模型（如 `medium` 或 `large`）
- 确认音频质量良好
- 检查语言设置（代码中已设为中文 `language="zh"`）

## 与阿里云服务对比

| 特性 | 本地 Whisper | 阿里云听悟 |
|------|-------------|-----------|
| **成本** | 免费（需硬件） | 按量计费 |
| **速度** | GPU 快 / CPU 慢 | 稳定快速 |
| **准确度** | 优秀 | 优秀（针对中文优化） |
| **隐私** | 完全本地 | 数据上传云端 |
| **网络** | 仅下载音频 | 需稳定网络 |
| **关键词提取** | 基础词频统计 | AI 智能提取 |
| **文本润色** | 无 | 支持 |

## 扩展 LocalWhisper

如需优化关键词提取，可以集成更强的 NLP 工具：

```python
# 安装 jieba 分词
pip install jieba

# 在 _extract_keywords 方法中使用
import jieba.analyse
keywords = jieba.analyse.extract_tags(text, topK=10)
```

## 示例输出

转录完成后，输出到 `./output/{标题}.md`：

```markdown
# 【清洁标题】

## 关键词

`视频`, `技术`, `教程`, `#抖音热点`

## 内容

这是转录的文本内容...
```
