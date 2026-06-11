from pathlib import Path
import time

class Storage:
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save(self, title: str, text: str, keywords: list = None, hashtags: list = None):
        # 合并关键词和标签
        all_keywords = []
        if keywords:
            all_keywords.extend(keywords)
        if hashtags:
            all_keywords.extend([f"#{tag}" for tag in hashtags])

        # 构建 Markdown 格式
        content = f"# {title}\n\n"

        if all_keywords:
            content += "## 关键词\n\n"
            content += ", ".join(f"`{kw}`" for kw in all_keywords) + "\n\n"

        content += "## 内容\n\n"
        content += text

        safe_title = title.translate(str.maketrans('', '', '/:*?"<>|')) or str(int(time.time()))
        filename = self.output_dir / f"{safe_title}.md"
        filename.write_text(content, encoding='utf-8')
        return filename
