# Douyin to Text Skill

自定义 Claude Code skill，用于将抖音视频 URL 转换为文本文档。

## 功能特性

- ✅ 解析抖音视频 URL 并提取元数据
- ✅ 自动选择转录服务（阿里云 API 或本地 Whisper）
- ✅ 提取关键词和话题标签
- ✅ 批量处理支持
- ✅ 输出为格式化的 Markdown 文件

## 安装到 Claude Code

### 方法 1：作为项目 Skill（推荐）

在项目根目录的 `.claude/settings.json` 中添加：

```json
{
  "skills": {
    "dy2text": {
      "command": "dy2text-skill/dy2text.bat",
      "description": "Convert Douyin videos to text documents",
      "cwd": "${workspaceFolder}"
    }
  }
}
```

### 方法 2：作为全局 Skill

在 `~/.claude/settings.json` 中添加：

```json
{
  "skills": {
    "dy2text": {
      "command": "C:/Users/user1/Documents/videoUrl2document/dy2text-skill/dy2text.bat",
      "description": "Convert Douyin videos to text documents"
    }
  }
}
```

## 使用方法

在 Claude Code 对话中输入：

```
/dy2text https://v.douyin.com/xxxxx/
```

### 单个 URL
```
/dy2text https://v.douyin.com/xxxxx/
```

### 多个 URL
```
/dy2text url1 url2 url3
```

### 从文件读取
```
/dy2text urls.txt
```

## 工作流程

1. **解析输入**：从命令行或文件中提取抖音 URL
2. **选择服务**：
   - 检测到阿里云凭证 → 使用阿里云听悟 API
   - 否则 → 使用本地 Whisper（需要 FFmpeg）
3. **处理视频**：解析 URL → 下载音频 → 转录 → 提取关键词
4. **保存结果**：输出到 `./output/{标题}.md`

## 环境要求

### 使用阿里云听悟（云 API）
在项目根目录的 `.env` 文件中配置：
```
ALIYUN_ACCESS_KEY_ID=your_key_id
ALIYUN_ACCESS_KEY_SECRET=your_key_secret
ALIYUN_APPKEY=your_app_key
```

### 使用本地 Whisper（无需 API）
- 安装 FFmpeg: `choco install ffmpeg`
- 安装 Whisper：
  - GPU: `pip install faster-whisper`
  - CPU: `pip install openai-whisper`

## 输出格式

```markdown
# {视频标题}

## 关键词

`关键词1`, `关键词2`, `#话题标签`

## 内容

{转录的文本内容...}
```

## 错误处理

- ❌ 无效 URL → 跳过并继续处理有效链接
- ❌ 缺少 FFmpeg → 提示用户安装
- ❌ 缺少 API 凭证 → 回退到本地 Whisper
- ❌ 转录失败 → 报告错误并继续下一个视频

## 文件结构

```
dy2text-skill/
├── skill.md          # Skill 元数据和文档
├── dy2text.py        # 主实现（Python）
├── dy2text.sh        # Shell 包装器（Linux/Mac）
├── dy2text.bat       # Batch 包装器（Windows）
└── README.md         # 本文件
```

## 故障排查

### 问题 1：Skill 未识别

确保在 `.claude/settings.json` 中正确配置了 skill，并且路径正确。

### 问题 2：找不到模块

确保在项目根目录有 `.venv` 虚拟环境，并且已安装所有依赖：
```bash
pip install -r requirements.txt
```

### 问题 3：权限错误（Linux/Mac）

给 shell 脚本添加执行权限：
```bash
chmod +x dy2text-skill/dy2text.sh
```

## 示例

```
用户: /dy2text https://v.douyin.com/2riL8TmD5Ps/

Claude Code 执行:
✓ 使用阿里云听悟 API
找到 1 个有效链接
开始处理 1 个任务...
============================================================
[1/1] 处理: 奥德赛时期｜愿我们都能游过那片海
  ✓ 解析完成
  ✓ 提交转录任务: task_abc123
  ✓ 转录完成
  ✓ 保存到: output/奥德赛时期｜愿我们都能游过那片海.md
============================================================

✓ 完成: 1/1
```

## 相关文档

- [项目 README](../README.md)
- [本地 Whisper 文档](../README_WHISPER.md)
- [架构说明](../CLAUDE.md)
