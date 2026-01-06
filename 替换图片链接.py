import os
import re

def replace_image_links(file_path):
    """替换文件中的GitHub图片链接为本地路径"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换GitHub图片链接为本地路径
    pattern = r'https://github\.com/frangoteam/FUXA\.wiki/raw/master/images/([^)]+)'
    replacement = r'images/\1'
    
    new_content = re.sub(pattern, replacement, content)
    
    # 如果内容有变化，写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 查找所有.md文件
    md_files = []
    for file in os.listdir(current_dir):
        if file.endswith('.md'):
            md_files.append(file)
    
    print(f"📖 找到 {len(md_files)} 个Markdown文件")
    print()
    
    # 替换每个文件中的图片链接
    replaced_count = 0
    for md_file in sorted(md_files):
        file_path = os.path.join(current_dir, md_file)
        if replace_image_links(file_path):
            print(f"✅ 已更新: {md_file}")
            replaced_count += 1
        else:
            print(f"⏭️  无需更新: {md_file}")
    
    print()
    print(f"🎉 完成！共更新了 {replaced_count} 个文件")
    print(f"📁 所有图片链接已改为本地路径: images/")

if __name__ == '__main__':
    main()
