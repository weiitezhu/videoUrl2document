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

        content = text
        if all_keywords:
            content = f"关键词：{', '.join(all_keywords)}\n\n{text}"

        safe_title = title.translate(str.maketrans('', '', '/:*?"<>|')) or str(int(time.time()))
        filename = self.output_dir / f"{safe_title}.txt"
        filename.write_text(content, encoding='utf-8')
        return filename
