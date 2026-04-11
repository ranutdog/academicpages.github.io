# Publications markdown generator for AcademicPages
# 已升级：支持自动添加论文配图（header.teaser）
# 使用方法：python3 publications.py [filename]

import csv
import os
import sys

# Flag to indicate an error occurred
EXIT_ERROR = 0

# 升级后的表头：增加了 image 列（论文配图路径）
HEADER_FINAL = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url', 'category', 'image']

# 兼容旧表头
HEADER_LEGACY  = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url']
HEADER_UPDATED = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'slides_url', 'category']

HTML_ESCAPE_TABLE = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def create_md(lines: list, layout: list):
    for item in lines:
        # 文件名
        md_filename = f"{item[layout.index('pub_date')]}-{item[layout.index('url_slug')]}.md"
        html_filename = f"{item[layout.index('pub_date')]}-{item[layout.index('url_slug')]}"
        
        # YAML 开始
        md = f"---\ntitle: \"{item[layout.index('title')]}\"\n"
        md += "collection: publications\n"
        
        if 'category' in layout:
            md += f"category: {item[layout.index('category')]}\n"
        else:
            md += "category: manuscripts\n"
            
        md += f"permalink: /publication/{html_filename}\n"
        
        if len(str(item[layout.index('excerpt')])) > 5:
            md += f"excerpt: '{html_escape(item[layout.index('excerpt')])}'\n"
            
        md += f"date: {item[layout.index('pub_date')]}\n"
        md += f"venue: '{html_escape(item[layout.index('venue')])}'\n"
        
        if len(str(item[layout.index('paper_url')])) > 5:
            md += f"paperurl: '{item[layout.index('paper_url')]}'\n"
            
        md += f"citation: '{html_escape(item[layout.index('citation')])}'\n"

        # ====================== 【关键：自动加图片】 ======================
        if 'image' in layout:
            img_path = item[layout.index('image')].strip()
            if img_path:  # 如果有图片路径，才插入
                md += f"header:\n  teaser: {img_path}\n"
        # ==================================================================

        md += "---\n"

        # 正文部分
        if len(str(item[layout.index('paper_url')])) > 5:
            md += f"\n<a href='{item[layout.index('paper_url')]}'>Download paper here</a>\n"
        if len(str(item[layout.index('excerpt')])) > 5:
            md += f"\n{html_escape(item[layout.index('excerpt')])}\n"
        md += f"\nRecommended citation: {item[layout.index('citation')]}"

        # 写入文件
        md_filename = os.path.join("../_publications/", os.path.basename(md_filename))
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(md)

def html_escape(text):
    return "".join(HTML_ESCAPE_TABLE.get(c,c) for c in text)

def read(filename: str) -> tuple[list, list]:
    lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        delimiter = ',' if filename.endswith('.csv') else '\t'
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            lines.append(row)

    if len(lines) <= 1:
        print(f'Not enough lines', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    # 自动识别最新表头（含image）
    header = lines[0]
    if header == HEADER_FINAL:
        layout = HEADER_FINAL
    elif header == HEADER_UPDATED:
        layout = HEADER_UPDATED
    elif header == HEADER_LEGACY:
        layout = HEADER_LEGACY
    else:
        print("表头不匹配，请使用升级后的带 image 列的表格")
        print("正确表头：" + "\t".join(HEADER_FINAL))
        sys.exit(EXIT_ERROR)

    lines = lines[1:]
    return lines, layout

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 publications.py [filename]', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    filename = sys.argv[1]
    if not (filename.endswith('.csv') or filename.endswith('.tsv')):
        print(f'Expected csv/tsv', file=sys.stderr)
        sys.exit(EXIT_ERROR)

    lines, layout = read(filename)
    create_md(lines, layout)
    