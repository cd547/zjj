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
        
        # 初始化文件路径和URL
        self.excel_file = ""
        self.config_file = ""
        self.url = ""
        self.automator = None
        # 初始化日志文件
        self.log_file = self._init_log_file()
    
    def _init_log_file(self):
        """初始化日志文件
        
        Returns:
            str: 日志文件路径
        """
        import os
        import sys
        import datetime
        import tempfile
        
        # 尝试使用多种目录作为日志存储位置
        possible_dirs = []
        
        # 1. 优先使用可执行文件所在目录的logs子目录
        try:
            # 获取可执行文件所在的目录
            if getattr(sys, 'frozen', False):
                # 程序被打包成可执行文件
                exe_dir = os.path.dirname(os.path.abspath(sys.executable))
                logs_dir_candidate = os.path.join(exe_dir, "logs")
                possible_dirs.append(logs_dir_candidate)
        except:
            pass
        
        # 2. 尝试使用程序所在目录的logs子目录
        try:
            program_dir = os.path.dirname(os.path.abspath(__file__))
            logs_dir_candidate = os.path.join(program_dir, "logs")
            possible_dirs.append(logs_dir_candidate)
        except:
            pass
        
        # 3. 尝试使用当前工作目录的logs子目录
        try:
            current_dir = os.getcwd()
            logs_dir_candidate = os.path.join(current_dir, "logs")
            possible_dirs.append(logs_dir_candidate)
        except:
            pass
        
        # 4. 最后使用临时目录的logs子目录
        temp_dir = os.path.join(tempfile.gettempdir(), "logs")
        possible_dirs.append(temp_dir)
        
        # 尝试创建日志目录
        logs_dir = None
        for dir_path in possible_dirs:
            try:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                # 测试目录是否可写
                test_file = os.path.join(dir_path, "test_write.txt")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                logs_dir = dir_path
                break
            except:
                continue
        
        # 如果所有目录都失败，使用临时目录
        if logs_dir is None:
            logs_dir = temp_dir
            if not os.path.exists(logs_dir):
                os.makedirs(logs_dir)
        
        # 生成日志文件名（基于当前时间）
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(logs_dir, f"excel_web_filler_{timestamp}.log")
        
        # 写入日志文件头
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"=== Excel Web Filler 日志文件 ===\n")
                f.write(f"创建时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"日志文件: {log_file}\n")
                f.write("==================================\n\n")
        except Exception as e:
            print(f"创建日志文件失败: {e}")
            # 如果创建失败，使用临时文件
            log_file = os.path.join(tempfile.gettempdir(), f"excel_web_filler_{timestamp}.log")
            try:
                with open(log_file, 'w', encoding='utf-8') as f:
                    f.write(f"=== Excel Web Filler 日志文件 ===\n")
                    f.write(f"创建时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"日志文件: {log_file}\n")
                    f.write(f"使用临时目录，因为其他目录不可写\n")
                    f.write(f"创建日志文件失败: {e}\n")
                    f.write("==================================\n\n")
            except:
                # 如果临时文件也失败，返回空字符串
                return ""
        
        # 打印日志文件路径，方便调试
        print(f"日志文件路径: {log_file}")
        
        return log_file
    
    def create_file_selection(self):
        """创建文件选择部分"""
        file_frame = tk.Frame(self.main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        # URL输入框（放在最上面）
        url_label = tk.Label(file_frame, text="URL地址:", font=self.font)
        url_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.url_var = tk.StringVar()
        url_entry = tk.Entry(file_frame, textvariable=self.url_var, width=60, font=self.font)
        url_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Excel文件选择
        excel_label = tk.Label(file_frame, text="Excel文件:", font=self.font)
        excel_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.excel_var = tk.StringVar()
        excel_entry = tk.Entry(file_frame, textvariable=self.excel_var, width=60, font=self.font)
        excel_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        excel_button = tk.Button(file_frame, text="浏览", command=self.browse_excel, font=self.font)
        excel_button.grid(row=1, column=2, padx=10, pady=5)
        
        # 配置文件按钮（打开弹出框）
        config_label = tk.Label(file_frame, text="配置文件:", font=self.font)
        config_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.config_var = tk.StringVar()
        config_entry = tk.Entry(file_frame, textvariable=self.config_var, width=50, font=self.font, state=tk.DISABLED)
        config_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        config_button = tk.Button(file_frame, text="配置", command=self.open_config_dialog, font=self.font)
        config_button.grid(row=2, column=2, padx=10, pady=5)
    
    def create_start_button(self):
        """创建启动按钮"""
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # 创建两个按钮
        self.connect_button = tk.Button(button_frame, text="连接网页", command=self.connect_to_webpage, 
                                     font=(self.font[0], self.font[1], "bold"), 
                                     bg="#2196F3", fg="white", 
                                     height=2, width=15)
        self.connect_button.pack(side=tk.LEFT, padx=10)
        
        self.fill_button = tk.Button(button_frame, text="自动填表", command=self.fill_table, 
                                 font=(self.font[0], self.font[1], "bold"), 
                                 bg="#4CAF50", fg="white", 
                                 height=2, width=15, state=tk.DISABLED)
        self.fill_button.pack(side=tk.LEFT, padx=10)
    
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
    
    def open_config_dialog(self):
        """打开配置文件弹出框"""
        # 创建弹出框
        dialog = tk.Toplevel(self.root)
        dialog.title("配置文件管理")
        dialog.geometry("800x600")
        dialog.resizable(True, True)
        
        # 设置弹出框为模态窗口
        dialog.grab_set()
        
        # 创建主框架
        main_frame = tk.Frame(dialog, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 配置文件选择部分
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        config_label = tk.Label(file_frame, text="配置文件:", font=self.font)
        config_label.pack(side=tk.LEFT, padx=10)
        
        config_var = tk.StringVar()
        if self.config_file:
            config_var.set(self.config_file)
        
        config_entry = tk.Entry(file_frame, textvariable=config_var, width=50, font=self.font)
        config_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        def browse_config_in_dialog():
            file_path = filedialog.askopenfilename(
                title="选择配置文件",
                filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
            )
            if file_path:
                config_var.set(file_path)
                # 加载配置文件内容到文本框
                load_config_content(file_path)
        
        browse_button = tk.Button(file_frame, text="浏览", command=browse_config_in_dialog, font=self.font)
        browse_button.pack(side=tk.LEFT, padx=10)
        
        # 配置内容展示部分
        content_frame = tk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        content_label = tk.Label(content_frame, text="配置内容:", font=self.font)
        content_label.pack(anchor=tk.W, pady=5)
        
        # 创建文本框用于展示配置内容
        content_text = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, 
                                               font=("Courier New", 10), 
                                               height=20)
        content_text.pack(fill=tk.BOTH, expand=True)
        
        def load_config_content(file_path):
            """加载配置文件内容到文本框"""
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                content_text.delete(1.0, tk.END)
                content_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("错误", f"读取配置文件失败: {e}")
        
        # 如果当前有配置文件，加载其内容
        if self.config_file:
            load_config_content(self.config_file)
        else:
            # 尝试查找默认配置文件
            import sys
            import os
            default_config_paths = []
            
            # 1. 尝试从可执行文件所在目录的cfg文件夹读取
            try:
                if getattr(sys, 'frozen', False):
                    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
                    default_config_paths.append(os.path.join(exe_dir, "cfg", "default.json"))
            except:
                pass
            
            # 2. 尝试从程序所在目录的cfg文件夹读取
            try:
                program_dir = os.path.dirname(os.path.abspath(__file__))
                default_config_paths.append(os.path.join(program_dir, "cfg", "default.json"))
            except:
                pass
            
            # 3. 尝试从当前工作目录的cfg文件夹读取
            try:
                current_dir = os.getcwd()
                default_config_paths.append(os.path.join(current_dir, "cfg", "default.json"))
            except:
                pass
            
            # 尝试读取默认配置文件
            for default_config_path in default_config_paths:
                if os.path.exists(default_config_path):
                    try:
                        config_var.set(default_config_path)
                        load_config_content(default_config_path)
                        break
                    except:
                        continue
        
        # 按钮部分
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def load_config():
            """加载配置文件"""
            import os
            file_path = config_var.get().strip()
            if not file_path:
                messagebox.showerror("错误", "请选择配置文件")
                return
            
            if not os.path.exists(file_path):
                messagebox.showerror("错误", f"配置文件不存在: {file_path}")
                return
            
            try:
                # 更新主界面的配置文件路径
                self.config_var.set(file_path)
                self.config_file = file_path
                
                # 重置按钮状态，恢复到程序刚打开时的状态
                self.connect_button.config(state=tk.NORMAL)
                self.fill_button.config(state=tk.DISABLED)
                
                # 重置automator对象
                self.automator = None
                
                messagebox.showinfo("成功", "配置文件加载成功")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"加载配置文件失败: {e}")
        
        load_button = tk.Button(button_frame, text="加载", command=load_config, 
                              font=(self.font[0], self.font[1], "bold"), 
                              bg="#4CAF50", fg="white", 
                              height=1, width=10)
        load_button.pack(side=tk.RIGHT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=dialog.destroy, 
                                font=(self.font[0], self.font[1], "bold"), 
                                bg="#f44336", fg="white", 
                                height=1, width=10)
        cancel_button.pack(side=tk.RIGHT, padx=10)
    
    def connect_to_webpage(self):
        """连接到网页"""
        # 获取文件路径和URL
        self.excel_file = self.excel_var.get().strip()
        self.config_file = self.config_var.get().strip()
        self.url = self.url_var.get().strip()
        
        # 检查文件路径是否为空
        if not self.excel_file:
            messagebox.showerror("错误", "请选择Excel文件")
            return
        
        # 配置文件为选填项，不检查
        
        # 检查文件是否存在
        if not os.path.exists(self.excel_file):
            messagebox.showerror("错误", f"Excel文件不存在: {self.excel_file}")
            return
        
        # 配置文件为选填项，不检查是否存在
        
        # 清空输出窗口
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # 禁用连接按钮
        self.connect_button.config(state=tk.DISABLED)
        
        # 执行连接命令
        self.execute_connect()
    
    def execute_connect(self):
        """执行连接网页命令"""
        try:
            self.append_output("开始连接到网页...\n")
            
            # 导入WebAutomator
            from web_automator import WebAutomator
            self.append_output("WebAutomator模块导入成功\n")
            
            # 导入json和os
            import json
            import os
            self.append_output("json模块导入成功\n")
            
            # 加载配置文件
            config = None
            
            # 如果用户指定了配置文件，使用用户指定的
            if self.config_file:
                if not os.path.exists(self.config_file):
                    self.append_output(f"配置文件不存在: {self.config_file}\n")
                    messagebox.showerror("错误", f"配置文件不存在: {self.config_file}")
                    self.connect_button.config(state=tk.NORMAL)
                    return
                
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    self.append_output(f"使用用户指定的配置文件: {self.config_file}\n")
                except Exception as e:
                    self.append_output(f"读取配置文件失败: {e}\n")
                    messagebox.showerror("错误", f"读取配置文件失败: {e}")
                    self.connect_button.config(state=tk.NORMAL)
                    return
            else:
                # 用户未指定配置文件，尝试从默认位置读取
                import sys
                import os
                default_config_paths = []
                
                # 1. 尝试从可执行文件所在目录的cfg文件夹读取
                try:
                    if getattr(sys, 'frozen', False):
                        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
                        default_config_paths.append(os.path.join(exe_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 2. 尝试从程序所在目录的cfg文件夹读取
                try:
                    program_dir = os.path.dirname(os.path.abspath(__file__))
                    default_config_paths.append(os.path.join(program_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 3. 尝试从当前工作目录的cfg文件夹读取
                try:
                    current_dir = os.getcwd()
                    default_config_paths.append(os.path.join(current_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 尝试读取默认配置文件
                config_file_found = False
                default_config_path = None
                for default_config_path in default_config_paths:
                    if os.path.exists(default_config_path):
                        try:
                            with open(default_config_path, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                            self.append_output(f"使用默认配置文件: {default_config_path}\n")
                            config_file_found = True
                            # 更新主界面的配置文件路径
                            self.config_var.set(default_config_path)
                            self.config_file = default_config_path
                            break
                        except Exception as e:
                            self.append_output(f"读取默认配置文件失败: {e}\n")
                            continue
                
                if not config_file_found:
                    self.append_output("错误: 未找到配置文件\n")
                    messagebox.showerror("错误", "未找到配置文件，请选择配置文件或在cfg文件夹中放置default.json")
                    self.connect_button.config(state=tk.NORMAL)
                    return
            
            # 获取URL，优先使用界面输入的URL
            url = self.url if self.url else config.get('url', '')
            if not url:
                self.append_output("警告: 未提供网页URL\n")
                messagebox.showwarning("警告", "未提供网页URL")
                self.connect_button.config(state=tk.NORMAL)
                return
            
            # 连接到网页
            self.append_output("连接到网页...\n")
            self.append_output(f"使用URL: {url}\n")
            self.automator = WebAutomator(url)
            if not self.automator.is_connected:
                self.append_output("错误: 网页连接失败，无法继续执行任务\n")
                messagebox.showerror("错误", "网页连接失败")
                self.connect_button.config(state=tk.NORMAL)
                return
            self.append_output("网页连接成功\n")
            
            # 启用填表按钮
            self.fill_button.config(state=tk.NORMAL)
            self.append_output("现在可以点击'自动填表'按钮开始填表\n")
            
        except Exception as e:
            self.append_output(f"连接网页时出错: {e}\n")
            import traceback
            traceback_str = traceback.format_exc()
            self.append_output(traceback_str)
            messagebox.showerror("错误", f"连接网页时出错: {e}")
            self.connect_button.config(state=tk.NORMAL)
    
    def fill_table(self):
        """执行填表操作"""
        # 禁用填表按钮
        self.fill_button.config(state=tk.DISABLED)
        
        # 执行填表命令
        self.execute_fill()
    
    def execute_fill(self):
        """执行填表命令"""
        try:
            if not self.automator:
                self.append_output("错误: 请先连接到网页\n")
                messagebox.showerror("错误", "请先连接到网页")
                self.fill_button.config(state=tk.NORMAL)
                return
            
            self.append_output("开始执行填表任务...\n")
            
            # 导入ExcelReader
            from excel_reader import ExcelReader
            self.append_output("ExcelReader模块导入成功\n")
            
            # 导入json和os
            import json
            import os
            self.append_output("json模块导入成功\n")
            
            # 加载配置文件
            config = None
            
            # 如果用户指定了配置文件，使用用户指定的
            if self.config_file:
                if not os.path.exists(self.config_file):
                    self.append_output(f"配置文件不存在: {self.config_file}\n")
                    messagebox.showerror("错误", f"配置文件不存在: {self.config_file}")
                    self.fill_button.config(state=tk.NORMAL)
                    return
                
                try:
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    self.append_output(f"使用用户指定的配置文件: {self.config_file}\n")
                except Exception as e:
                    self.append_output(f"读取配置文件失败: {e}\n")
                    messagebox.showerror("错误", f"读取配置文件失败: {e}")
                    self.fill_button.config(state=tk.NORMAL)
                    return
            else:
                # 用户未指定配置文件，尝试从默认位置读取
                import sys
                import os
                default_config_paths = []
                
                # 1. 尝试从可执行文件所在目录的cfg文件夹读取
                try:
                    if getattr(sys, 'frozen', False):
                        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
                        default_config_paths.append(os.path.join(exe_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 2. 尝试从程序所在目录的cfg文件夹读取
                try:
                    program_dir = os.path.dirname(os.path.abspath(__file__))
                    default_config_paths.append(os.path.join(program_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 3. 尝试从当前工作目录的cfg文件夹读取
                try:
                    current_dir = os.getcwd()
                    default_config_paths.append(os.path.join(current_dir, "cfg", "default.json"))
                except:
                    pass
                
                # 尝试读取默认配置文件
                config_file_found = False
                for default_config_path in default_config_paths:
                    if os.path.exists(default_config_path):
                        try:
                            with open(default_config_path, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                            self.append_output(f"使用默认配置文件: {default_config_path}\n")
                            config_file_found = True
                            # 更新主界面的配置文件路径
                            self.config_var.set(default_config_path)
                            self.config_file = default_config_path
                            break
                        except Exception as e:
                            self.append_output(f"读取默认配置文件失败: {e}\n")
                            continue
                
                if not config_file_found:
                    self.append_output("错误: 未找到配置文件\n")
                    messagebox.showerror("错误", "未找到配置文件，请选择配置文件或在cfg文件夹中放置default.json")
                    self.fill_button.config(state=tk.NORMAL)
                    return
            
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
            
            # 获取满足条件的表格列表
            matching_tables = self.automator.matching_tables
            if not matching_tables:
                self.append_output("警告: 未找到满足条件的表格，无法继续执行任务\n")
                messagebox.showwarning("警告", "未找到满足条件的表格")
                self.fill_button.config(state=tk.NORMAL)
                return
            
            self.append_output(f"找到 {len(matching_tables)} 个满足条件的表格\n")
            
            # 初始化Excel数据行索引
            excel_row_index = 0
            
            # 按表格顺序处理数据
            for table_index, table_id in enumerate(matching_tables):
                self.append_output(f"\n处理表格 {table_index + 1}/{len(matching_tables)}: {table_id}\n")
                
                # 动态生成table_identifier
                table_identifier = f"//table[@id='{table_id}']//tr[position()>=3]"
                self.append_output(f"使用table_identifier: {table_identifier}\n")
                
                # 获取当前表格的行数
                try:
                    # 使用web_automator的page对象来获取表格行数
                    table_locator = self.automator.page.locator(f"//table[@id='{table_id}']//tr[position()>=3]")
                    table_row_count = self.automator._run_async(table_locator.count())
                    self.append_output(f"当前表格有 {table_row_count} 行可填写\n")
                except Exception as e:
                    self.append_output(f"获取表格行数失败: {e}\n")
                    table_row_count = 0
                
                # 处理当前表格的每一行
                for table_row_index in range(table_row_count):
                    # 检查Excel数据是否已用完
                    if excel_row_index >= len(data):
                        self.append_output("Excel数据已全部填写完毕\n")
                        break
                    
                    # 获取当前Excel行数据
                    row = data[excel_row_index]
                    self.append_output(f"处理Excel第 {excel_row_index + 1} 行数据，填写到表格第 {table_row_index + 1} 行...\n")
                    
                    # 填入数据
                    for field_mapping in config.get('field_mappings', []):
                        excel_field = field_mapping.get('excel_field')
                        web_element = field_mapping.get('web_element')
                        element_type = field_mapping.get('element_type', 'input')
                        default_value = field_mapping.get('default_value')
                        
                        # 动态生成web_element，替换table_identifier
                        if 'table_identifier' in web_element:
                            web_element = web_element.copy()
                            web_element['table_identifier'] = table_identifier
                        
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
                                self.automator.fill_input(web_element, value, table_row_index)
                            elif element_type == 'select':
                                self.automator.select_option(web_element, value, table_row_index)
                            elif element_type == 'textarea':
                                self.automator.fill_textarea(web_element, value, table_row_index)
                            else:
                                self.append_output(f"警告: 不支持的元素类型 {element_type}\n")
                        except Exception as e:
                            self.append_output(f"填入 {excel_field} 时出错: {e}\n")
                            self.append_output("继续处理下一个字段...\n")
                            # 出错时不退出，继续处理下一个字段
                    
                    # Excel行索引递增
                    excel_row_index += 1
                
                self.append_output(f"表格 {table_index + 1} 处理完成\n")
                
                # 如果Excel数据已全部填写完毕，退出循环
                if excel_row_index >= len(data):
                    self.append_output("所有Excel数据已填写完毕\n")
                    break
            
            # 任务完成
            self.append_output("\n" + "="*60 + "\n")
            self.append_output("任务完成！")
            self.append_output("浏览器保持打开状态，您可以继续使用。")
            
        except Exception as e:
            self.append_output(f"执行填表命令时出错: {e}\n")
            import traceback
            traceback_str = traceback.format_exc()
            self.append_output(traceback_str)
            messagebox.showerror("错误", f"执行填表命令时出错: {e}")
        finally:
            # 启用填表按钮
            self.fill_button.config(state=tk.NORMAL)
    
    def append_output(self, text):
        """向输出窗口添加文本并写入日志文件"""
        # 添加到输出窗口
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)  # 滚动到末尾
        self.output_text.config(state=tk.DISABLED)
        self.root.update()  # 立即更新界面
        
        # 写入日志文件
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(text)
            except Exception as e:
                # 日志写入失败时不影响主程序运行
                print(f"写入日志文件失败: {e}")

def main():
    """主函数"""
    root = tk.Tk()
    app = ExcelWebFillerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()