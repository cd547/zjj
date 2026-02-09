#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel内容自动填入网页工具 - GUI界面

使用tkinter实现图形用户界面，替代命令行参数
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import sys
import os

class ExcelWebFillerGUI:
    """Excel内容自动填入网页工具的GUI界面"""
    
    def __init__(self, root):
        """初始化GUI界面
        
        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title("Excel内容自动填入网页工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 设置字体
        self.font = ("SimHei", 10)
        
        # 创建主框架
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文件选择部分
        self.create_file_selection()
        
        # 创建启动按钮
        self.create_start_button()
        
        # 创建输出窗口
        self.create_output_window()
        
        # 初始化文件路径
        self.excel_file = ""
        self.config_file = ""
    
    def create_file_selection(self):
        """创建文件选择部分"""
        file_frame = tk.Frame(self.main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        # Excel文件选择
        excel_label = tk.Label(file_frame, text="Excel文件:", font=self.font)
        excel_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.excel_var = tk.StringVar()
        excel_entry = tk.Entry(file_frame, textvariable=self.excel_var, width=60, font=self.font)
        excel_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        excel_button = tk.Button(file_frame, text="浏览", command=self.browse_excel, font=self.font)
        excel_button.grid(row=0, column=2, padx=10, pady=5)
        
        # 配置文件选择
        config_label = tk.Label(file_frame, text="配置文件:", font=self.font)
        config_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.config_var = tk.StringVar()
        config_entry = tk.Entry(file_frame, textvariable=self.config_var, width=60, font=self.font)
        config_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        config_button = tk.Button(file_frame, text="浏览", command=self.browse_config, font=self.font)
        config_button.grid(row=1, column=2, padx=10, pady=5)
    
    def create_start_button(self):
        """创建启动按钮"""
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = tk.Button(button_frame, text="启动", command=self.start_process, 
                                     font=(self.font[0], self.font[1], "bold"), 
                                     bg="#4CAF50", fg="white", 
                                     height=2, width=20)
        self.start_button.pack(anchor=tk.CENTER)
    
    def create_output_window(self):
        """创建输出窗口"""
        output_frame = tk.Frame(self.main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        output_label = tk.Label(output_frame, text="执行输出:", font=self.font)
        output_label.pack(anchor=tk.W)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                   font=("Courier New", 9), 
                                                   height=15)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # 禁止编辑输出窗口
        self.output_text.config(state=tk.DISABLED)
    
    def browse_excel(self):
        """浏览选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
        )
        if file_path:
            self.excel_var.set(file_path)
            self.excel_file = file_path
    
    def browse_config(self):
        """浏览选择配置文件"""
        file_path = filedialog.askopenfilename(
            title="选择配置文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if file_path:
            self.config_var.set(file_path)
            self.config_file = file_path
    
    def start_process(self):
        """启动处理过程"""
        # 获取文件路径
        self.excel_file = self.excel_var.get().strip()
        self.config_file = self.config_var.get().strip()
        
        # 检查文件路径是否为空
        if not self.excel_file:
            messagebox.showerror("错误", "请选择Excel文件")
            return
        
        if not self.config_file:
            messagebox.showerror("错误", "请选择配置文件")
            return
        
        # 检查文件是否存在
        if not os.path.exists(self.excel_file):
            messagebox.showerror("错误", f"Excel文件不存在: {self.excel_file}")
            return
        
        if not os.path.exists(self.config_file):
            messagebox.showerror("错误", f"配置文件不存在: {self.config_file}")
            return
        
        # 清空输出窗口
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # 禁用启动按钮
        self.start_button.config(state=tk.DISABLED)
        
        # 执行命令
        self.execute_command()
    
    def execute_command(self):
        """执行命令"""
        try:
            self.append_output("开始执行任务...\n")
            
            # 检查文件是否存在
            if not os.path.exists(self.excel_file):
                self.append_output(f"错误: Excel文件不存在: {self.excel_file}\n")
                return
            
            if not os.path.exists(self.config_file):
                self.append_output(f"错误: 配置文件不存在: {self.config_file}\n")
                return
            
            self.append_output(f"Excel文件: {self.excel_file}\n")
            self.append_output(f"配置文件: {self.config_file}\n")
            
            # 直接导入并调用必要的模块
            self.append_output("导入必要的模块...\n")
            
            # 导入ExcelReader
            from excel_reader import ExcelReader
            self.append_output("ExcelReader模块导入成功\n")
            
            # 导入WebAutomator
            from web_automator import WebAutomator
            self.append_output("WebAutomator模块导入成功\n")
            
            # 导入json
            import json
            self.append_output("json模块导入成功\n")
            
            # 加载配置文件
            self.append_output("加载配置文件...\n")
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.append_output("配置文件加载成功\n")
            
            # 获取Excel配置
            excel_config = config.get('excel_config', {})
            header_row = excel_config.get('header_row', 16)  # 默认表头行
            start_row = excel_config.get('start_row', 17)  # 默认数据开始行
            end_row = excel_config.get('end_row', None)  # 默认结束行
            discount = excel_config.get('discount', None)  # 折扣值
            
            # 读取Excel数据
            self.append_output("读取Excel数据...\n")
            reader = ExcelReader(self.excel_file, header_row, start_row, end_row)
            data = reader.read_data()
            self.append_output(f"Excel数据读取成功，共 {len(data)} 行\n")
            
            # 获取URL
            url = config.get('url', '')
            if not url:
                self.append_output("警告: 未提供网页URL\n")
            
            # 连接到网页
            self.append_output("连接到网页...\n")
            automator = WebAutomator(url)
            if not automator.is_connected:
                self.append_output("错误: 网页连接失败，无法继续执行任务\n")
                return
            self.append_output("网页连接成功\n")
            
            # 处理每个数据行
            self.append_output("处理数据...\n")
            for row_index, row in enumerate(data):
                self.append_output(f"处理第 {row_index + 1} 行数据...\n")
                
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
                        self.append_output(f"使用默认值: {value} 填入字段 {excel_field}\n")
                    else:
                        # 没有默认值，检查excel_field是否为空
                        if not excel_field:
                            # excel_field为空，无法从Excel中获取值
                            self.append_output(f"警告: excel_field为空，且未配置默认值\n")
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
                                            self.append_output(f"使用Excel值: {row[excel_field]} 填入字段 {excel_field}\n")
                                            self.append_output(f"转换为oem_type索引: {oem_index} ({oem_value})\n")
                                        else:
                                            self.append_output(f"警告: 未找到对应的oem_type值: {oem_value}\n")
                                            continue
                                    else:
                                        self.append_output(f"警告: 未知的Brand值: {value}\n")
                                        continue
                                else:
                                    self.append_output(f"使用Excel值: {value} 填入字段 {excel_field}\n")
                            else:
                                # 如果Excel中值为None，尝试使用discount值
                                if discount is not None:
                                    value = discount
                                    self.append_output(f"Excel值为None，使用discount值: {value} 填入字段 {excel_field}\n")
                                else:
                                    self.append_output(f"警告: Excel中字段 {excel_field} 的值为None\n")
                                    continue
                        else:
                            # 如果Excel中缺少字段，尝试使用discount值
                            if discount is not None:
                                value = discount
                                self.append_output(f"Excel中缺少字段 {excel_field}，使用discount值: {value} 填入字段 {excel_field}\n")
                            else:
                                self.append_output(f"警告: Excel中缺少字段 {excel_field}，且未配置discount值\n")
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
                            self.append_output(f"警告: 不支持的元素类型 {element_type}\n")
                    except Exception as e:
                        self.append_output(f"填入 {excel_field} 时出错: {e}\n")
                        self.append_output("继续处理下一个字段...\n")
                        # 出错时不退出，继续处理下一个字段
            
            # 任务完成
            self.append_output("\n" + "="*60 + "\n")
            self.append_output("任务完成！")
            self.append_output("浏览器保持打开状态，您可以继续使用。")
            
        except Exception as e:
            self.append_output(f"执行命令时出错: {e}\n")
            import traceback
            traceback_str = traceback.format_exc()
            self.append_output(traceback_str)
        finally:
            # 启用启动按钮
            self.start_button.config(state=tk.NORMAL)
    
    def append_output(self, text):
        """向输出窗口添加文本"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)  # 滚动到末尾
        self.output_text.config(state=tk.DISABLED)
        self.root.update()  # 立即更新界面

def main():
    """主函数"""
    root = tk.Tk()
    app = ExcelWebFillerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()