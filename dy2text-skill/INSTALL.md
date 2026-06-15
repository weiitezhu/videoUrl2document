# dy2text Skill 安装指南

## 快速安装（3 步）

### 1️⃣ 创建配置文件

在项目根目录创建 `.claude` 目录（如果不存在）：

```bash
mkdir .claude
```

### 2️⃣ 配置 Skill

编辑或创建 `.claude/settings.json`，添加以下内容：

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

**Linux/Mac 用户**：将 `dy2text.bat` 改为 `dy2text.sh`

### 3️⃣ 测试 Skill

在 Claude Code 对话中输入：

```
/dy2text urls.txt
```

或测试单个 URL：

```
/dy2text https://v.douyin.com/xxxxx/
```

## 详细配置选项

### 选项 A：项目级 Skill（推荐）

在 **项目根目录** `.claude/settings.json` 中配置：

```json
{
  "skills": {
    "dy2text": {
      "command": "dy2text-skill/dy2text.bat",
      "description": "Convert Douyin videos to text documents with transcription",
      "cwd": "${workspaceFolder}",
      "allowedPrompts": [
        {
          "tool": "Bash",
          "prompt": "run Python scripts in dy2text-skill"
        }
      ]
    }
  }
}
```

**优点**：仅在当前项目可用，不会污染全局配置

### 选项 B：全局 Skill

在 **用户目录** `~/.claude/settings.json` 中配置：

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

**优点**：在任何 Claude Code 会话中都可用

**注意**：需要使用绝对路径

## 验证安装

### 方法 1：通过 Claude Code

在对话中输入：

```
请列出可用的 skills
```

应该能看到 `dy2text` 出现在列表中。

### 方法 2：直接运行

```bash
cd C:\Users\user1\Documents\videoUrl2document
python dy2text-skill/dy2text.py urls.txt
```

应该看到成功处理的输出。

## 故障排查

### 问题 1：Skill 未出现

**症状**：Claude Code 无法识别 `/dy2text`

**解决**：
1. 确认 `.claude/settings.json` 存在且语法正确
2. 重启 Claude Code
3. 检查路径是否正确（相对路径或绝对路径）

### 问题 2：编码错误

**症状**：`UnicodeEncodeError: 'gbk' codec...`

**解决**：已在代码中修复，确保使用最新版本的 `dy2text.py`

### 问题 3：找不到模块

**症状**：`ModuleNotFoundError: No module named 'core'`

**解决**：
1. 确保在项目根目录运行
2. 检查 `cwd` 配置是否为 `${workspaceFolder}`
3. 激活虚拟环境：`.venv\Scripts\activate`

### 问题 4：权限错误（Linux/Mac）

**症状**：`Permission denied: dy2text.sh`

**解决**：
```bash
chmod +x dy2text-skill/dy2text.sh
```

## 使用示例

### 示例 1：单个视频

```
/dy2text https://v.douyin.com/2riL8TmD5Ps/
```

输出：
```
找到 1 个有效链接
✓ 使用阿里云听悟 API
开始处理 1 个任务...
============================================================
✓ 完成: 1/1
```

### 示例 2：批量处理

创建 `my_urls.txt`：
```
https://v.douyin.com/url1/
https://v.douyin.com/url2/
https://v.douyin.com/url3/
```

运行：
```
/dy2text my_urls.txt
```

### 示例 3：命令行多个 URL

```
/dy2text https://v.douyin.com/url1/ https://v.douyin.com/url2/
```

## 下一步

- ✅ 配置阿里云 API（见主 README.md）
- ✅ 或配置本地 Whisper（见 README_WHISPER.md）
- ✅ 开始转录视频！

## 相关文档

- [Skill 使用说明](README.md)
- [项目主文档](../README.md)
- [本地 Whisper 配置](../README_WHISPER.md)
- [架构说明](../CLAUDE.md)
