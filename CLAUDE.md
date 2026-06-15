# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture

Three-layer architecture for video-to-document conversion:

**Core Layer** (`core/`) - Abstract interfaces:
- `platform.py`: `PlatformParser` interface returns `VideoInfo(title, audio_url, platform)`
- `transcribe.py`: `TranscribeService` interface with `submit()` and `get_result()` returning `TranscribeResult(text, keywords)`
- `storage.py`: Saves results as Markdown with title, keywords (including hashtags), and content
- `task.py`: `TaskProcessor` orchestrates the pipeline and handles batch processing with ThreadPoolExecutor

**Platform Layer** (`platforms/`):
- `douyin.py`: Calls bugpk API, extracts `#hashtags` from title, cleans and truncates title to 50 chars, attaches hashtags to VideoInfo object

**Service Layer** (`services/`):
- `aliyun_tingwu.py`: Uses Aliyun Tingwu API for speech-to-text, polls every 10s until completion, fetches TextPolish and MeetingAssistance URLs for parsed results
- `local_whisper.py`: Local Whisper transcription service, auto-detects GPU (uses faster-whisper if NVIDIA GPU available, otherwise openai-whisper), requires FFmpeg, includes jieba-based keyword extraction

## Key Flow

1. Parse URL → VideoInfo (with title cleanup and hashtag extraction)
2. Submit audio URL → task_id
3. Poll for completion → TranscribeResult
4. Save to `./output/{title}.md` with keywords and hashtags merged

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
cp .env.example .env

# === Aliyun Tingwu (cloud API) ===
# Single URL
python main.py "https://v.douyin.com/xxxxx/"

# Batch from command line
python batch.py "url1" "url2" "url3"

# Batch from file (one URL per line, filters for douyin.com)
python batch.py urls.txt

# === Local Whisper (no API, requires FFmpeg) ===
# Install FFmpeg: choco install ffmpeg (Windows)
# Install Whisper engine (choose one):
#   GPU: pip install faster-whisper
#   CPU: pip install openai-whisper
# Optional: pip install jieba (better Chinese keyword extraction)

# Batch processing with local Whisper
python batch_local.py "url1" "url2" "url3"
python batch_local.py urls.txt

# Change model size in batch_local.py:
#   LocalWhisper(model_size="base")  # tiny, base, small, medium, large
```

## Environment Variables

Required in `.env` (for Aliyun Tingwu only):
- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_APPKEY` (Tingwu project)

**Note**: Local Whisper does not require API credentials.

## Output Format

Markdown files in `./output/`:
```markdown
# {cleaned_title}

## 关键词

`keyword1`, `keyword2`, `#hashtag1`

## 内容

{transcribed_text}
```

## Extending

**New platform**: Implement `PlatformParser`, return `VideoInfo` with audio URL
**New transcription service**: Implement `TranscribeService.submit()` and `get_result()`

Note: `main.py` is legacy single-task entry point. `batch.py` uses the layered architecture and is preferred.
