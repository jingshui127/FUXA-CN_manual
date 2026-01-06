import re

def fix_links_to_html_sections(file_path):
    """将Markdown链接替换为HTML内部锚点链接"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 链接映射：Markdown文件名 -> HTML锚点
    link_mappings = {
        '02-快速入门指南.md': '#section-02-快速入门指南',
        '03-安装和运行指南.md': '#section-03-安装和运行指南',
        '04-设备和标签配置.md': '#section-04-设备和标签配置',
        '05-组件开发教程.md': '#section-05-组件开发教程',
        '06-高级功能配置.md': '#section-06-高级功能配置',
        '07-系统设置与使用技巧.md': '#section-07-系统设置与使用技巧',
        '08-Node-RED集成教程.md': '#section-08-Node-RED集成教程',
        '09-ODBC数据库集成教程.md': '#section-09-ODBC数据库集成教程',
        '10-调度器使用教程.md': '#section-10-调度器使用教程',
        '11-视图管理教程.md': '#section-11-视图管理教程',
        '12-WebSocket通信教程.md': '#section-12-WebSocket通信教程',
        '13-图表控制教程.md': '#section-13-图表控制教程',
        '14-UI布局设置教程.md': '#section-14-UI布局设置教程',
        '15-管道动画教程.md': '#section-15-管道动画教程',
        '16-控件绑定教程.md': '#section-16-控件绑定教程',
        '17-形状绑定教程.md': '#section-17-形状绑定教程',
        '18-脚本配置教程.md': '#section-18-脚本配置教程',
        '19-事件配置教程.md': '#section-19-事件配置教程',
        '20-系统配置教程.md': '#section-20-系统配置教程',
        '21-视图复用教程.md': '#section-21-视图复用教程',
        '22-报警配置教程.md': '#section-22-报警配置教程',
        '23-项目管理教程.md': '#section-23-项目管理教程',
        '24-自定义形状定义教程.md': '#section-24-自定义形状定义教程',
        '25-脚本配置教程.md': '#section-25-脚本配置教程',
        '26-事件配置教程.md': '#section-26-事件配置教程',
        '27-形状绑定教程.md': '#section-27-形状绑定教程',
        '28-控件绑定教程.md': '#section-28-控件绑定教程',
        '29-小组件开发教程.md': '#section-29-小组件开发教程',
        '30-视图创建教程.md': '#section-30-视图创建教程',
        '31-编辑器快捷键技巧.md': '#section-31-编辑器快捷键技巧',
        # 英文文件名映射
        'Installing-and-Running.md': '#section-03-安装和运行指南',
        'HowTo-Devices-and-Tags.md': '#section-04-设备和标签配置',
        'HowTo-View.md': '#section-30-视图创建教程',
        'HowTo-bind-Controls.md': '#section-16-控件绑定教程',
        'HowTo-bind-Shapes.md': '#section-17-形状绑定教程',
        'HowTo-Chart-Control.md': '#section-13-图表控制教程',
        'HowTo-UI-Layout.md': '#section-14-UI布局设置教程',
        'HowTo-setup-Alarms.md': '#section-22-报警配置教程',
        'HowTo-configure-Script.md': '#section-18-脚本配置教程',
        'HowTo-configure-events.md': '#section-19-事件配置教程',
        'HowTo-Scheduler.md': '#section-10-调度器使用教程',
        'HowTo-WebSockets.md': '#section-12-WebSocket通信教程'
    }
    
    # 替换所有Markdown链接为HTML锚点
    for md_file, html_anchor in link_mappings.items():
        pattern = rf'href="{md_file}"'
        replacement = f'href="{html_anchor}"'
        content = re.sub(pattern, replacement, content)
    
    # 移除target="_blank"属性，因为现在是内部跳转
    content = re.sub(r'(href="#section-[^"]+")\s+target="_blank"', r'\1', content)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 链接修复完成！所有Markdown链接已替换为HTML内部锚点")

if __name__ == '__main__':
    html_file = r'C:\Users\Administrator\Downloads\FUXA汉化文档\FUXA汉化文档_完整版.html'
    fix_links_to_html_sections(html_file)
