#!/usr/bin/env python3
"""
Quick setup script for dy2text skill
"""

import json
import os
import sys
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def setup_skill():
    """Configure dy2text skill in Claude Code"""

    project_root = Path(__file__).parent.parent
    claude_dir = project_root / '.claude'
    settings_file = claude_dir / 'settings.json'

    # Create .claude directory if needed
    claude_dir.mkdir(exist_ok=True)

    # Detect platform
    if os.name == 'nt':
        command = 'dy2text-skill/dy2text.bat'
    else:
        command = 'dy2text-skill/dy2text.sh'
        # Make shell script executable
        sh_file = project_root / 'dy2text-skill' / 'dy2text.sh'
        os.chmod(sh_file, 0o755)

    # Load or create settings
    if settings_file.exists():
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    else:
        settings = {}

    # Add skill configuration
    if 'skills' not in settings:
        settings['skills'] = {}

    settings['skills']['dy2text'] = {
        'command': command,
        'description': 'Convert Douyin videos to text documents',
        'cwd': '${workspaceFolder}'
    }

    # Save settings
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)

    print('✓ dy2text skill 已配置')
    print(f'✓ 配置文件: {settings_file}')
    print('\n使用方法:')
    print('  /dy2text https://v.douyin.com/xxxxx/')
    print('  /dy2text urls.txt')
    print('\n需要重启 Claude Code 使配置生效')


if __name__ == '__main__':
    setup_skill()
