# 抖音视频转文档

将抖音分享的视频内容转换为文本文档。

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
- `ALIYUN_REGION`: 地域 (cn-shanghai/cn-beijing/cn-shenzhen)

## 使用

```bash
python main.py "https://v.douyin.com/xxxxx/"
```

识别完成后会在当前目录生成以视频标题命名的txt文件。
