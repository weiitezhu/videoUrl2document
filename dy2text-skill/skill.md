---
name: dy2text
description: Convert Douyin (抖音) video URLs to text documents with transcription
version: 1.0.0
---

# Douyin to Text Skill

Converts Douyin video URLs to markdown documents with full transcription and keyword extraction.

## Capabilities

- Parse Douyin video URLs and extract metadata
- Transcribe audio using Aliyun Tingwu API or local Whisper
- Extract keywords and hashtags automatically
- Batch processing support
- Output as formatted markdown files

## Usage

User can invoke this skill by typing:
```
/dy2text <urls or file>
```

Examples:
- `/dy2text https://v.douyin.com/xxxxx/`
- `/dy2text url1 url2 url3`
- `/dy2text urls.txt`

## Workflow

1. **Parse input**: Accept URLs from command line or text file
2. **Choose transcription service**: 
   - Check if Aliyun credentials exist → use Aliyun Tingwu
   - Otherwise → use local Whisper (requires FFmpeg)
3. **Process videos**: Parse URL → download audio → transcribe → extract keywords
4. **Save results**: Output to `./output/{title}.md` with keywords and content

## Environment Requirements

### For Aliyun Tingwu (Cloud API)
- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_APPKEY`

### For Local Whisper (No API needed)
- FFmpeg installed
- faster-whisper (GPU) or openai-whisper (CPU)
- Optional: jieba for better Chinese keyword extraction

## Output Format

```markdown
# {video_title}

## 关键词

`keyword1`, `keyword2`, `#hashtag`

## 内容

{transcribed_text_content}
```

## Error Handling

- Invalid URLs → skip and continue with valid ones
- Missing FFmpeg → prompt user to install
- Missing API credentials → fallback to local Whisper
- Transcription failure → report error and continue with next video
