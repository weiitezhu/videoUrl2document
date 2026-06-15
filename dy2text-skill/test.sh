# Douyin to Text Skill - 测试脚本

## 测试 1：单个 URL
python dy2text-skill/dy2text.py "https://v.douyin.com/2riL8TmD5Ps/"

## 测试 2：多个 URL
python dy2text-skill/dy2text.py "https://v.douyin.com/url1/" "https://v.douyin.com/url2/"

## 测试 3：从文件读取
python dy2text-skill/dy2text.py urls.txt

## 测试 4：检查依赖
python -c "
import os
import sys
from pathlib import Path

print('=== 环境检查 ===')

# 检查 Python 版本
print(f'Python: {sys.version}')

# 检查 FFmpeg
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
    print('✓ FFmpeg: 已安装')
except FileNotFoundError:
    print('✗ FFmpeg: 未安装')

# 检查 .env
if Path('.env').exists():
    print('✓ .env: 存在')
else:
    print('✗ .env: 不存在')

# 检查依赖包
packages = ['requests', 'dotenv', 'torch']
optional = ['faster_whisper', 'whisper', 'jieba']

for pkg in packages:
    try:
        __import__(pkg)
        print(f'✓ {pkg}: 已安装')
    except ImportError:
        print(f'✗ {pkg}: 未安装')

print('\n=== 可选包 ===')
for pkg in optional:
    try:
        __import__(pkg)
        print(f'✓ {pkg}: 已安装')
    except ImportError:
        print(f'- {pkg}: 未安装')
"
