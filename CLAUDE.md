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

## Key Flow

1. Parse URL → VideoInfo (with title cleanup and hashtag extraction)
2. Submit audio URL → task_id
3. Poll for completion → TranscribeResult
4. Save to `./output/{title}.md` with keywords and hashtags merged

## Commands

```bash
# Single URL
python main.py "https://v.douyin.com/xxxxx/"

# Batch from command line
python batch.py "url1" "url2" "url3"

# Batch from file (one URL per line, filters for douyin.com)
python batch.py urls.txt

# Install
pip install -r requirements.txt
cp .env.example .env
```

## Environment Variables

Required in `.env`:
- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_APPKEY` (Tingwu project)

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
