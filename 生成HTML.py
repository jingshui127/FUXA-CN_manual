#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FUXA 汉化文档 - Markdown 转 HTML 转换器
将所有Markdown文档转换为HTML并合并到一个文件中
"""

import os
import re
import json
from pathlib import Path

# Markdown 转 HTML 的简单转换器
def markdown_to_html(markdown):
    html = markdown

    # 先处理代码块（避免被其他规则影响）
    # 先处理代码块，标记它们的位置
    code_blocks = []
    def save_code_block(match):
        code_blocks.append(match.group(0))
        return f'__CODE_BLOCK_{len(code_blocks)-1}__'
    
    html = re.sub(r'```(\w+)?\n([\s\S]*?)```', save_code_block, html)
    
    # 转换标题
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*$)', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # 转换粗体
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)

    # 转换斜体
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)

    # 转换行内代码（避免影响代码块）
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # 转换图片
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', html)

    # 转换链接 - 区分内部文档链接和外部链接
    def convert_link(match):
        text = match.group(1)
        url = match.group(2)
        # 检查是否是内部文档链接（以.md结尾）
        if url.endswith('.md'):
            # 转换为锚点跳转
            # 移除可能的 ./ 前缀
            clean_url = url.replace('./', '')
            section_id = clean_url.replace('.md', '')
            return f'<a href="#section-{section_id}" class="internal-link">{text}</a>'
        else:
            # 外部链接，在新窗口打开
            return f'<a href="{url}" target="_blank">{text}</a>'
    
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', convert_link, html)

    # 转换无序列表
    html = re.sub(r'^- (.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n)+', r'<ul>\g<0></ul>', html)

    # 转换有序列表
    html = re.sub(r'^\d+\. (.*)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # 转换引用
    html = re.sub(r'^> (.*)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)

    # 转换水平线
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)

    # 转换表格
    lines = html.split('\n')
    in_table = False
    table_rows = []
    result_lines = []

    for line in lines:
        if '|' in line and line.strip().startswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
        else:
            if in_table:
                # 生成表格HTML
                if len(table_rows) > 1:
                    result_lines.append('<table>')
                    for i, row in enumerate(table_rows):
                        if i == 0:
                            result_lines.append('<tr>' + ''.join([f'<th>{cell}</th>' for cell in row]) + '</tr>')
                        elif not all(re.match(r'^-+$', cell) for cell in row):
                            result_lines.append('<tr>' + ''.join([f'<td>{cell}</td>' for cell in row]) + '</tr>')
                    result_lines.append('</table>')
                in_table = False
                table_rows = []
            result_lines.append(line)

    html = '\n'.join(result_lines)

    # 恢复代码块并转换为HTML（在段落转换之前）
    for i, block in enumerate(code_blocks):
        # 提取语言和代码内容
        match = re.match(r'```(\w+)?\n([\s\S]*?)```', block)
        if match:
            lang = match.group(1) or ''
            code = match.group(2)
            # 使用换行符包裹，确保被段落转换识别为独立段落
            code_html = f'\n\n<pre><code class="{lang}">{code}</code></pre>\n\n'
            html = html.replace(f'__CODE_BLOCK_{i}__', code_html)

    # 转换段落
    html = re.sub(r'\n\n', '</p><p>', html)
    html = '<p>' + html + '</p>'

    # 清理空段落
    html = re.sub(r'<p>\s*</p>', '', html)

    # 修复嵌套标签（使用多行匹配）
    html = re.sub(r'<p>(<h[1-6]>.*?</h[1-6]>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ul>.*?</ul>)</p>', r'\1', html)
    html = re.sub(r'<p>(<ol>.*?</ol>)</p>', r'\1', html)
    html = re.sub(r'(?s)<p>(<pre>.*?</pre>)</p>', r'\1', html)
    html = re.sub(r'(?s)<p>(<blockquote>.*?</blockquote>)</p>', r'\1', html)
    html = re.sub(r'(?s)<p>(<table>.*?</table>)</p>', r'\1', html)
    html = re.sub(r'<p>(<hr>)</p>', r'\1', html)
    
    # 修复代码块周围的段落标签
    html = re.sub(r'</p>\s*<pre>', r'<pre>', html)
    html = re.sub(r'</pre>\s*<p>', r'</pre>', html)
    
    # 清理多余的空行
    html = re.sub(r'\n\s*\n\s*\n', '\n\n', html)

    return html

# 读取案例1的Markdown文件
def read_markdown_files(directory):
    documents = {}
    # 读取所有Markdown文件，除了README.md
    for file in sorted(os.listdir(directory)):
        if file.endswith('.md') and file != 'README.md':
            file_path = os.path.join(directory, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                documents[file] = markdown_to_html(content)
    return documents

# 生成HTML文件
def generate_html(documents, output_file):
    # 生成导航菜单
    nav_items = []
    for i, (filename, _) in enumerate(sorted(documents.items())):
        section_id = filename.replace('.md', '')
        # 从文件名提取标题
        if filename.startswith('案例'):
            # 案例文件：案例1-连接MQTT服务器实现SCADA.md -> 案例1: 连接MQTT服务器实现SCADA
            parts = filename.replace('.md', '').split('-', 1)
            if len(parts) == 2:
                title = f"{parts[0]}: {parts[1]}"
            else:
                title = filename.replace('.md', '')
        else:
            # 教程文件：01-主页介绍.md -> 01. 主页介绍
            title = filename.replace('.md', '').replace('-', '. ')
        nav_items.append(f'<li class="nav-item" data-section="{section_id}">{title}</li>')

    # 生成内容区域
    content_sections = []
    for filename, html_content in sorted(documents.items()):
        section_id = filename.replace('.md', '')
        content_sections.append(f'''
        <div class="content-section" id="section-{section_id}">
            {html_content}
        </div>''')

    # HTML模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FUXA 完整汉化文档</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}

        .container {{
            display: flex;
            min-height: 100vh;
        }}

        .sidebar {{
            width: 320px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            z-index: 1000;
        }}

        .sidebar h1 {{
            font-size: 24px;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            text-align: center;
        }}

        .search-box {{
            margin-bottom: 20px;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 25px;
            font-size: 14px;
            background: rgba(255,255,255,0.2);
            color: #fff;
            outline: none;
            transition: background 0.3s;
        }}

        .search-box input::placeholder {{
            color: rgba(255,255,255,0.7);
        }}

        .search-box input:focus {{
            background: rgba(255,255,255,0.3);
        }}

        .nav-menu {{
            list-style: none;
        }}

        .nav-item {{
            padding: 12px 15px;
            cursor: pointer;
            border-radius: 8px;
            margin-bottom: 5px;
            transition: all 0.3s;
            font-size: 14px;
        }}

        .nav-item:hover {{
            background: rgba(255,255,255,0.2);
            transform: translateX(5px);
        }}

        .nav-item.active {{
            background: rgba(255,255,255,0.3);
            font-weight: bold;
        }}

        .main-content {{
            flex: 1;
            margin-left: 320px;
            padding: 40px;
            background: #fff;
            max-width: 1200px;
        }}

        .content-section {{
            display: none;
            animation: fadeIn 0.3s ease-in;
        }}

        .content-section.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .content-section h1 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 32px;
        }}

        .content-section h2 {{
            color: #764ba2;
            margin-top: 40px;
            margin-bottom: 20px;
            padding-left: 15px;
            border-left: 4px solid #667eea;
            font-size: 24px;
        }}

        .content-section h3 {{
            color: #333;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 20px;
        }}

        .content-section p {{
            margin-bottom: 15px;
            line-height: 1.8;
            color: #555;
        }}

        .content-section ul, .content-section ol {{
            margin: 15px 0 15px 30px;
            color: #555;
        }}

        .content-section li {{
            margin-bottom: 8px;
        }}

        .content-section table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .content-section th, .content-section td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}

        .content-section th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            font-weight: bold;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}

        .content-section tr:hover {{
            background: #f8f9fa;
        }}

        .content-section pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .content-section code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            font-size: 0.9em;
        }}

        .content-section pre code {{
            background: none;
            color: inherit;
            padding: 0;
            font-size: 14px;
        }}

        .content-section img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 20px 0;
        }}

        .content-section blockquote {{
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin: 20px 0;
            background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
            color: #555;
            border-radius: 0 8px 8px 0;
        }}

        .content-section hr {{
            border: none;
            border-top: 2px solid #eee;
            margin: 40px 0;
        }}

        .back-to-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            text-align: center;
            line-height: 50px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: none;
            transition: all 0.3s;
            font-size: 24px;
            z-index: 1000;
        }}

        .back-to-top:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
            }}

            .main-content {{
                margin-left: 0;
                padding: 20px;
            }}

            .content-section h1 {{
                font-size: 24px;
            }}

            .content-section h2 {{
                font-size: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h1>📚 FUXA 文档</h1>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 搜索文档...">
            </div>
            <ul class="nav-menu" id="navMenu">
                {''.join(nav_items)}
            </ul>
        </div>

        <div class="main-content" id="mainContent">
            {''.join(content_sections)}
        </div>
    </div>

    <div class="back-to-top" id="backToTop">↑</div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const navItems = document.querySelectorAll('.nav-item');
            const contentSections = document.querySelectorAll('.content-section');
            const searchInput = document.getElementById('searchInput');
            const backToTop = document.getElementById('backToTop');

            // 初始化：显示第一个文档
            if (navItems.length > 0 && contentSections.length > 0) {{
                navItems[0].classList.add('active');
                contentSections[0].classList.add('active');
            }}

            // 导航菜单点击
            navItems.forEach(item => {{
                item.addEventListener('click', function() {{
                    const section = this.getAttribute('data-section');
                    
                    // 移除所有active类
                    navItems.forEach(nav => nav.classList.remove('active'));
                    contentSections.forEach(sec => sec.classList.remove('active'));
                    
                    // 添加active类到当前项
                    this.classList.add('active');
                    const targetSection = document.getElementById('section-' + section);
                    if (targetSection) {{
                        targetSection.classList.add('active');
                    }}
                    
                    // 滚动到顶部
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }});
            }});

            // 搜索功能
            searchInput.addEventListener('input', function() {{
                const query = this.value.toLowerCase();
                navItems.forEach(item => {{
                    const text = item.textContent.toLowerCase();
                    if (text.includes(query)) {{
                        item.style.display = 'block';
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});
            }});

            // 返回顶部
            window.addEventListener('scroll', function() {{
                if (window.scrollY > 300) {{
                    backToTop.style.display = 'block';
                }} else {{
                    backToTop.style.display = 'none';
                }}
            }});

            backToTop.addEventListener('click', function() {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});

            // 处理hash变化，显示对应的section
            function handleHashChange() {{
                const hash = window.location.hash;
                if (hash && hash.startsWith('#section-')) {{
                    // 解码URL编码的中文
                    const sectionId = decodeURIComponent(hash.replace('#section-', ''));
                    
                    // 隐藏所有section
                    contentSections.forEach(sec => sec.classList.remove('active'));
                    
                    // 移除所有导航项的active类
                    navItems.forEach(nav => nav.classList.remove('active'));
                    
                    // 显示目标section
                    const targetSection = document.getElementById('section-' + sectionId);
                    if (targetSection) {{
                        targetSection.classList.add('active');
                    }}
                    
                    // 更新导航菜单的active状态
                    navItems.forEach(nav => {{
                        if (nav.getAttribute('data-section') === sectionId) {{
                            nav.classList.add('active');
                        }}
                    }});
                    
                    // 滚动到顶部
                    window.scrollTo({{ top: 0, behavior: 'smooth' }});
                }}
            }}

            // 监听hash变化
            window.addEventListener('hashchange', handleHashChange);
            
            // 页面加载时检查hash
            handleHashChange();
        }});
    </script>
</body>
</html>'''

    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"✅ HTML文件已生成: {output_file}")

# 主函数
def main():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 读取所有Markdown文件
    print("📖 正在读取Markdown文件...")
    documents = read_markdown_files(current_dir)
    print(f"✅ 已读取 {len(documents)} 个文档")
    
    # 生成HTML文件
    output_file = os.path.join(current_dir, 'FUXA中文手册_完整版.html')
    print("🔄 正在生成HTML文件...")
    generate_html(documents, output_file)
    
    print("\n🎉 完成！")
    print(f"📄 请在浏览器中打开: {output_file}")

if __name__ == '__main__':
    main()
