# 🚀 dy2text Skill - 快速开始

将抖音视频转换为文本文档的 Claude Code 自定义 skill。

## ⚡ 一键安装

```bash
cd C:\Users\user1\Documents\videoUrl2document
python dy2text-skill/setup.py
```

然后**重启 Claude Code**。

## 💡 使用方法

在 Claude Code 对话中输入：

```
/dy2text https://v.douyin.com/xxxxx/
```

### 更多用法

```bash
# 单个 URL
/dy2text https://v.douyin.com/2riL8TmD5Ps/

# 多个 URL
/dy2text url1 url2 url3

# 从文件批量处理
/dy2text urls.txt
```

## 📂 文件结构

```
dy2text-skill/
├── skill.md                    # Skill 元数据
├── dy2text.py                  # 核心实现
├── dy2text.bat / dy2text.sh    # 启动脚本
├── setup.py                    # 一键安装脚本
├── README.md                   # 详细文档
├── INSTALL.md                  # 安装指南
├── QUICKSTART.md               # 本文件
└── settings.json.example       # 配置示例
```

## ✅ 已完成

- [x] 自动选择转录服务（阿里云 API / 本地 Whisper）
- [x] 支持单个和批量处理
- [x] Windows 编码兼容
- [x] 关键词和话题标签提取
- [x] Markdown 格式输出
- [x] 一键配置脚本

## 🎯 工作原理

1. **解析 URL** → 提取视频信息和音频链接
2. **选择服务** → 自动检测可用的转录服务
3. **转录音频** → 生成文本和关键词
4. **保存结果** → 输出到 `./output/{标题}.md`

## 🔧 配置

### 使用阿里云听悟（推荐）

在 `.env` 文件中配置：
```
ALIYUN_ACCESS_KEY_ID=your_key
ALIYUN_ACCESS_KEY_SECRET=your_secret
ALIYUN_APPKEY=your_appkey
```

### 使用本地 Whisper（免费）

安装依赖：
```bash
choco install ffmpeg
pip install faster-whisper  # GPU
pip install openai-whisper  # CPU
```

## 📊 示例输出

```markdown
# 奥德赛时期｜愿我们都能游过那片海🌊

## 关键词

`视频`, `碎碎念`, `#talk`, `#治愈`

## 内容

[转录的文本内容...]
```

## 🆘 遇到问题？

查看详细文档：
- [完整安装指南](INSTALL.md)
- [使用说明](README.md)
- [项目文档](../README.md)

---

**提示**：Skill 已安装到 `.claude/settings.json`，可随时编辑配置。
