import os
import re

# 获取所有Markdown文件
md_files = [
    '01-主页介绍.md',
    '02-快速入门指南.md',
    '03-安装和运行指南.md',
    '04-设备和标签配置.md',
    '05-组件开发教程.md',
    '06-高级功能配置.md',
    '07-系统设置与使用技巧.md',
    '08-Node-RED集成教程.md',
    '09-ODBC数据库集成教程.md',
    '10-调度器使用教程.md',
    '11-视图管理教程.md',
    '12-WebSocket通信教程.md',
    '13-图表控制教程.md',
    '14-UI布局设置教程.md',
    '15-管道动画教程.md',
    '16-控件绑定教程.md',
    '17-形状绑定教程.md',
    '18-脚本配置教程.md',
    '19-事件配置教程.md',
    '20-系统配置教程.md',
    '21-视图复用教程.md',
    '22-报警配置教程.md',
    '23-项目管理教程.md',
    '24-自定义形状定义教程.md',
    '25-脚本配置教程.md',
    '26-事件配置教程.md',
    '27-形状绑定教程.md',
    '28-控件绑定教程.md',
    '29-小组件开发教程.md',
    '30-视图创建教程.md',
    '31-编辑器快捷键技巧.md'
]

# 要插入的图片标记
image_markdown = '\n\n![微信公众号](images/微信公众号.jpg)\n'

# 处理每个文件
for md_file in md_files:
    file_path = f'C:\\Users\\Administrator\\Downloads\\FUXA汉化文档\\{md_file}'
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经包含该图片
    if '微信公众号.jpg' in content:
        print(f'✓ {md_file} 已经包含微信公众号图片，跳过')
        continue
    
    # 在文件末尾添加图片
    content = content.rstrip() + image_markdown
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'✓ {md_file} 已添加微信公众号图片')

print('\n所有文件处理完成！')
