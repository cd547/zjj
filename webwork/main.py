#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主脚本，用于将Excel数据自动填入网页
"""

import json
import argparse
import sys
import os
from excel_reader import ExcelReader
from web_automator import WebAutomator

# 确保标准输出无缓冲
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8', line_buffering=True)
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8', line_buffering=True)

print("=== 程序开始执行 ===")
print(f"Python版本: {sys.version}")
print(f"命令行参数: {sys.argv}")
print(f"当前工作目录: {os.getcwd()}")
print(f"文件列表: {os.listdir('.')}")
print(f"ExcelReader模块是否存在: {'ExcelReader' in dir()}")
print(f"WebAutomator模块是否存在: {'WebAutomator' in dir()}")


def load_config(config_file):
    """加载配置文件"""
    print(f"=== 进入load_config函数 ===")
    print(f"配置文件路径: {config_file}")
    print(f"配置文件是否存在: {os.path.exists(config_file)}")
    try:
        print(f"尝试打开配置文件: {config_file}")
        with open(config_file, 'r', encoding='utf-8') as f:
            print(f"成功打开配置文件: {config_file}")
            content = f.read()
            print(f"配置文件内容长度: {len(content)}")
            # 尝试解析JSON
            print(f"尝试解析JSON")
            config = json.loads(content)
            print(f"成功解析JSON")
            print(f"配置文件键值: {list(config.keys())}")
            return config
    except Exception as e:
        print(f"加载配置文件失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """主函数"""
    print("=== 进入main函数 ===")
    print(f"命令行参数数量: {len(sys.argv)}")
    print(f"命令行参数列表: {sys.argv}")
    try:
        parser = argparse.ArgumentParser(description='将Excel数据自动填入网页')
        print("创建参数解析器成功")
        parser.add_argument('excel_file', help='Excel文件路径')
        parser.add_argument('config_file', help='配置文件路径')
        parser.add_argument('--url', help='网页URL（可选，默认为配置文件中的URL）')
        print("添加参数成功")
        args = parser.parse_args()
        print("解析参数成功")
        print(f"Excel文件: {args.excel_file}")
        print(f"配置文件: {args.config_file}")
        print(f"URL: {args.url}")
    except Exception as e:
        print(f"解析命令行参数失败: {e}")
        import traceback
        traceback.print_exc()
        return

    # 加载配置
    config = load_config(args.config_file)
    
    # 使用命令行参数中的URL（如果提供）
    url = args.url if args.url else config.get('url')
    if not url:
        print('警告: 未提供网页URL')
        # 出错时不退出，继续执行
    
    # 获取discount值
    discount = config.get('excel_config', {}).get('discount', None)

    # 读取Excel数据
    print('正在读取Excel文件...')
    # 从配置文件中获取Excel行数配置
    excel_config = config.get('excel_config', {})
    header_row = excel_config.get('header_row', 16)  # 默认表头行
    start_row = excel_config.get('start_row', 17)  # 默认数据开始行
    end_row = excel_config.get('end_row', None)  # 默认结束行（None表示到文件末尾）
    
    reader = ExcelReader(args.excel_file, header_row, start_row, end_row)
    data = reader.read_data()
    if not data:
        print('警告: Excel文件中没有数据')
        # 出错时不退出，继续执行

    # 连接到网页并填入数据
    print('正在连接到网页...')
    automator = WebAutomator(url)
    
    if not automator.is_connected:
        print('警告: 无法连接到网页，请确保网页已打开')
        # 出错时不退出，继续执行

    # 处理每个数据行
    for row_index, row in enumerate(data):
        print(f'\n正在填入第 {row_index + 1} 行数据...')
        # 填入数据
        for field_mapping in config.get('field_mappings', []):
            excel_field = field_mapping.get('excel_field')
            web_element = field_mapping.get('web_element')
            element_type = field_mapping.get('element_type', 'input')
            default_value = field_mapping.get('default_value')
            
            # 确定使用的值
            value = None
            # 首先检查是否有默认值
            if default_value is not None:
                value = default_value
                print(f'使用默认值: {value} 填入字段 {excel_field}')
            else:
                # 没有默认值，检查excel_field是否为空
                if not excel_field:
                    # excel_field为空，无法从Excel中获取值
                    print(f'警告: excel_field为空，且未配置默认值')
                    continue
                # 尝试使用Excel中的值
                if excel_field in row:
                    value = row[excel_field]
                    if value is not None:
                        # 处理Brand列的特殊映射
                        if excel_field == 'Brand':
                            # 获取oem_type映射
                            oem_type_list = config.get('excel_config', {}).get('oem_type', [])
                            # 定义Brand到oem_type的映射
                            brand_mapping = {
                                'LOCAL BRAND': 'Compatible',
                                'OEM': 'OEM',
                                'GENUINE': 'Genuine'
                            }
                            # 转换Brand值为oem_type值
                            if value in brand_mapping:
                                oem_value = brand_mapping[value]
                                # 查找oem_type的索引
                                if oem_value in oem_type_list:
                                    oem_index = oem_type_list.index(oem_value)
                                    value = oem_index
                                    print(f'使用Excel值: {row[excel_field]} 填入字段 {excel_field}')
                                    print(f'转换为oem_type索引: {oem_index} ({oem_value})')
                                else:
                                    print(f'警告: 未找到对应的oem_type值: {oem_value}')
                                    continue
                            else:
                                print(f'警告: 未知的Brand值: {value}')
                                continue
                        else:
                            print(f'使用Excel值: {value} 填入字段 {excel_field}')
                    else:
                        # 如果Excel中值为None，尝试使用discount值
                        if discount is not None:
                            value = discount
                            print(f'Excel值为None，使用discount值: {value} 填入字段 {excel_field}')
                        else:
                            print(f'警告: Excel中字段 {excel_field} 的值为None')
                            continue
                else:
                    # 如果Excel中缺少字段，尝试使用discount值
                    if discount is not None:
                        value = discount
                        print(f'Excel中缺少字段 {excel_field}，使用discount值: {value} 填入字段 {excel_field}')
                    else:
                        print(f'警告: Excel中缺少字段 {excel_field}，且未配置discount值')
                        continue
            
            # 填入网页元素
            try:
                if element_type == 'input':
                    automator.fill_input(web_element, value, row_index)
                elif element_type == 'select':
                    automator.select_option(web_element, value, row_index)
                elif element_type == 'textarea':
                    automator.fill_textarea(web_element, value, row_index)
                else:
                    print(f'警告: 不支持的元素类型 {element_type}')
            except Exception as e:
                print(f'填入 {excel_field} 时出错: {e}')
                print('继续处理下一个字段...')
                # 出错时不退出，继续处理下一个字段
        
        # 自动处理所有行，不需要用户确认
        # if len(data) > 1:
        #     user_input = input('\n是否继续处理下一行数据？(y/n): ')
        #     if user_input.lower() != 'y':
        #         break

    # 关闭浏览器（已禁用）
    automator.close()  # 此方法已被修改，不会关闭浏览器
    print('\n任务完成！浏览器保持打开状态。')
    print('数据已成功填入网页。')
    print('浏览器已保持打开状态，您可以继续使用。')
    print('按Enter键退出程序...')
    # 等待用户输入，确保浏览器保持打开状态
    # 这样可以防止Python解释器在程序结束时清理资源导致浏览器关闭
    input()


if __name__ == '__main__':
    main()
