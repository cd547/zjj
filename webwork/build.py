#!/usr/bin/env python3
"""
打包脚本，用于将Excel内容自动填入网页工具打包成可执行文件
"""

import os
import subprocess
import sys

def main():
    """主函数"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"项目根目录: {project_root}")
    
    # 检查必要文件是否存在
    required_files = [
        "gui.py",
        "main.py",
        "excel_reader.py",
        "web_automator.py",
        "config_szq_template.json"
    ]
    
    for file in required_files:
        file_path = os.path.join(project_root, file)
        if os.path.exists(file_path):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")
            sys.exit(1)
    
    # 构建打包命令（只使用gui.py作为入口）
    command = [
        "pyinstaller",
        "--onefile",
        "--name", "excel_web_filler",
        "--add-data", f"excel_reader.py;.",
        "--add-data", f"web_automator.py;.",
        "--add-data", f"config_szq_template.json;.",
        "--hidden-import", "playwright",
        "--hidden-import", "openpyxl",
        "gui.py"
    ]
    
    print("\n执行打包命令:")
    print(' '.join(command))
    print("\n开始打包，这可能需要几分钟时间...")
    
    # 执行打包命令
    try:
        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True
        )
        
        # 输出打包结果
        print("\n打包输出:")
        print(result.stdout)
        
        if result.stderr:
            print("\n打包错误:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✓ 打包成功!")
            print(f"可执行文件位置: {os.path.join(project_root, 'dist', 'excel_web_filler.exe')}")
            print("\n" + "="*60)
            print("使用说明:")
            print("="*60)
            print("1. 将excel_web_filler.exe和config_szq_template.json复制到同一目录")
            print("2. 双击excel_web_filler.exe运行")
            print("3. 在界面中选择Excel文件和配置文件，然后点击'启动'按钮")
            print("\n" + "="*60)
            print("打包完成!")
        else:
            print(f"\n✗ 打包失败，返回代码: {result.returncode}")
    except Exception as e:
        print(f"\n✗ 执行打包命令时出错: {e}")

if __name__ == "__main__":
    main()