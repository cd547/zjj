#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页自动化模块，用于连接到已打开的网页并填入数据
"""

from playwright.async_api import async_playwright
import time
import os
import asyncio


class WebAutomator:
    """网页自动化工具"""
    
    def __init__(self, url):
        """初始化WebAutomator
        
        Args:
            url (str): 网页URL
        """
        self.url = url
        self.playwright = None
        self.browser = None
        self.page = None
        self.is_connected = False
        self.loop = None
        self.matching_tables = []
        self.logs = []  # 存储日志信息
        self._connect()
    
    def _log(self, message):
        """记录日志信息
        
        Args:
            message (str): 日志信息
        """
        print(message)
        self.logs.append(message)
    
    def _connect(self):
        """连接到网页"""
        try:
            # 创建并保存事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # 在事件循环中运行异步连接
            self.loop.run_until_complete(self._connect_async())
            
        except Exception as e:
            self._log(f"连接到网页失败: {e}")
            self.is_connected = False
            # 不清理资源，保持浏览器打开
            self._log('保持浏览器打开状态，不清理资源')
    
    async def _connect_async(self):
        """异步连接到网页"""
        try:
            # 启动Playwright
            self.playwright = await async_playwright().start()
            # 启动浏览器（默认使用Chrome）
            self._log('正在启动浏览器...')
            
            # 尝试使用系统已安装的Chrome浏览器
            chrome_paths = [
                "C:\Program Files\Google\Chrome\Application\chrome.exe",
                "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            
            browser_launched = False
            for chrome_path in chrome_paths:
                try:
                    self._log(f'尝试使用Chrome路径: {chrome_path}')
                    self.browser = await self.playwright.chromium.launch(
                        headless=False,  # 显示浏览器窗口
                        slow_mo=50,  # 减慢操作速度，便于观察（从100ms减少到50ms）
                        executable_path=chrome_path,  # 系统Chrome路径
                        args=["--enable-scroll-bars"]  # 强制显示滚动条
                    )
                    browser_launched = True
                    break
                except Exception as e:
                    self._log(f'使用路径 {chrome_path} 失败: {e}')
            
            # 如果所有路径都失败，使用Playwright默认的浏览器
            if not browser_launched:
                self._log('使用系统Chrome失败，尝试使用Playwright默认浏览器...')
                self.browser = await self.playwright.chromium.launch(
                    headless=False,  # 显示浏览器窗口
                    slow_mo=50,  # 减慢操作速度，便于观察
                    args=["--enable-scroll-bars"]  # 强制显示滚动条
                )
            # 创建新页面
            self.page = await self.browser.new_page()
            # 导航到目标URL
            self._log(f'正在导航到: {self.url}')
            # 减少页面加载等待时间，从'networkidle'改为'load'，这样页面加载完成后就开始操作
            await self.page.goto(self.url, wait_until='load')
            
            # 注入CSS以强制显示滚动条
            await self.page.add_style_tag(content="""
                /* 强制显示滚动条 */
                ::-webkit-scrollbar {
                    width: 12px !important;
                    height: 12px !important;
                    display: block !important;
                }
                ::-webkit-scrollbar-track {
                    background: #f1f1f1 !important;
                }
                ::-webkit-scrollbar-thumb {
                    background: #888 !important;
                    border-radius: 6px !important;
                }
                ::-webkit-scrollbar-thumb:hover {
                    background: #555 !important;
                }
                /* 为body和所有可滚动元素添加滚动条 */
                body {
                    overflow: auto !important;
                    scrollbar-width: auto !important;
                    -ms-overflow-style: auto !important;
                }
                /* 确保所有可滚动容器都显示滚动条 */
                .scrollable,
                .overflow-auto,
                .overflow-x-auto,
                .overflow-y-auto {
                    overflow: auto !important;
                    scrollbar-width: auto !important;
                    -ms-overflow-style: auto !important;
                }
            """)
            
            # 检测满足条件的table元素
            await self._detect_tables()
            
            self.is_connected = True
            self._log('连接成功！')
                
        except Exception as e:
            self._log(f"连接到网页失败: {e}")
            self.is_connected = False
            # 不清理资源，保持浏览器打开
            self._log('保持浏览器打开状态，不清理资源')
    
    async def _detect_tables(self):
        """检测满足条件的table元素
        
        查找所有id符合"CPH_QGV_dxdt"+数字+"_QDGV_"+数字+"_DXMainTable"格式的table元素
        两个数字保持一致
        """
        try:
            import time
            start_time = time.time()
            self._log('\n开始检测满足条件的table元素...')
            
            # 优化方法：使用更精确的CSS选择器和批处理
            matching_tables = []
            
            # 方法1：使用更精确的CSS选择器（最快）
            try:
                # 使用更精确的CSS选择器，直接匹配id格式
                # 先获取所有可能的候选元素
                candidate_tables = await self.page.locator('table[id*="CPH_QGV_dxdt"][id*="_QDGV_"][id*="_DXMainTable"]').all()
                
                if candidate_tables:
                    self._log(f'使用精确CSS选择器筛选到 {len(candidate_tables)} 个候选table元素')
                    
                    # 对候选元素进行批处理
                    import re
                    pattern = r'^CPH_QGV_dxdt(\d+)_QDGV_\1_DXMainTable$'
                    
                    # 遍历候选元素
                    for table in candidate_tables:
                        # 获取table元素的id
                        table_id = await table.get_attribute('id')
                        if table_id:
                            # 检查id是否符合格式
                            if re.match(pattern, table_id):
                                matching_tables.append(table_id)
                                self._log(f'找到符合条件的table元素: {table_id}')
            except Exception as css_error:
                self._log(f'使用CSS选择器失败: {css_error}')
                # 如果CSS选择器方法失败，回退到优化的原始方法
                pass
            
            # 如果CSS选择器方法没有找到任何元素，使用优化的原始方法
            if not matching_tables:
                # 优化：限制一次性获取的元素数量
                self._log('使用优化的原始方法进行检测...')
                
                # 先获取所有table元素的id属性（批处理）
                table_elements = await self.page.locator('table').all()
                self._log(f'找到 {len(table_elements)} 个table元素')
                
                import re
                pattern = r'^CPH_QGV_dxdt(\d+)_QDGV_\1_DXMainTable$'
                
                # 遍历table元素，使用更高效的方式
                for i, table in enumerate(table_elements):
                    try:
                        # 获取table元素的id
                        table_id = await table.get_attribute('id')
                        if table_id:
                            # 检查id是否符合格式
                            if re.match(pattern, table_id):
                                matching_tables.append(table_id)
                                self._log(f'找到符合条件的table元素: {table_id}')
                    except Exception as e:
                        # 单个元素处理失败，继续处理下一个
                        continue
            
            # 保存匹配的表格
            self.matching_tables = matching_tables
            
            # 计算耗时
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 输出结果
            self._log('\n检测完成！')
            self._log(f'检测耗时: {elapsed_time:.2f} 秒')
            self._log(f'共找到 {len(matching_tables)} 个满足条件的table元素')
            if matching_tables:
                self._log('符合条件的table元素id:')
                for table_id in matching_tables:
                    self._log(f'  - {table_id}')
            else:
                self._log('未找到符合条件的table元素')
                
        except Exception as e:
            self._log(f"检测table元素失败: {e}")
    
    def _cleanup(self):
        """清理资源（已禁用）"""
        self._log('清理资源功能已禁用，保持浏览器打开')
        # 不清理任何资源，保持浏览器完全打开状态
    
    def screenshot(self, file_path):
        """截图当前页面
        
        Args:
            file_path (str): 截图文件保存路径
            
        Returns:
            str: 截图文件路径，如果失败则返回None
        """
        try:
            if not self.page:
                self._log("错误: 页面未连接")
                return None
            
            self._log(f"正在截图，保存到: {file_path}")
            
            # 使用Playwright的screenshot方法
            self._run_async(self.page.screenshot(path=file_path, full_page=True))
            
            self._log(f"截图成功: {file_path}")
            return file_path
        except Exception as e:
            self._log(f"截图失败: {e}")
            return None
    
    def _run_async(self, coro):
        """运行异步函数
        
        如果事件循环不存在或已关闭，会重新创建事件循环
        """
        try:
            # 检查事件循环状态
            if self.loop is None or self.loop.is_closed():
                # 事件循环不存在或已关闭，重新创建
                print("事件循环不存在或已关闭，正在重新创建...")
                self._recreate_event_loop()
            
            # 使用保存的事件循环运行异步函数
            return self.loop.run_until_complete(coro)
        except Exception as e:
            print(f"运行异步函数失败: {e}")
            # 尝试重新创建事件循环并重试
            try:
                print("尝试重新创建事件循环并重试...")
                self._recreate_event_loop()
                return self.loop.run_until_complete(coro)
            except Exception as retry_error:
                print(f"重试失败: {retry_error}")
                raise
    
    def _recreate_event_loop(self):
        """重新创建事件循环"""
        try:
            # 关闭旧的事件循环（如果存在）
            if self.loop is not None and not self.loop.is_closed():
                self.loop.close()
                print("旧事件循环已关闭")
            
            # 创建新的事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            print("新事件循环已创建")
        except Exception as e:
            print(f"重新创建事件循环失败: {e}")
            raise
    
    def _find_element(self, element_identifier, row_index=0):
        """查找网页元素
        
        Args:
            element_identifier (dict): 元素标识符，包含id、class_name、text、table_column等字段
            row_index (int): 数据行索引
            
        Returns:
            Locator: 找到的网页元素定位器
        """
        if not self.page:
            raise Exception('浏览器未连接')
        
        try:
            # 按ID查找
            if 'id' in element_identifier:
                return self.page.locator(f"#{element_identifier['id']}")
            # 按class name查找
            elif 'class_name' in element_identifier:
                return self.page.locator(f".{element_identifier['class_name']}")
            # 按文本内容查找
            elif 'text' in element_identifier:
                return self.page.locator(f"text={element_identifier['text']}")
            # 按XPath查找
            elif 'xpath' in element_identifier:
                return self.page.locator(element_identifier['xpath'])
            # 按CSS选择器查找
            elif 'css_selector' in element_identifier:
                return self.page.locator(element_identifier['css_selector'])
            # 按表格列号查找
            elif 'table_column' in element_identifier:
                column = element_identifier['table_column']
                table_identifier = element_identifier.get('table_identifier', '')
                
                # 构建基础选择器
                base_selector = table_identifier if table_identifier else "//table"
                
                # 首先尝试使用ID直接定位（如果有）
                if 'id' in element_identifier:
                    try:
                        locator = self.page.locator(f"#{element_identifier['id']}")
                        # 直接尝试获取元素，不先调用count()
                        try:
                            first_element = locator.first
                            is_visible = self._run_async(first_element.is_visible())
                            if is_visible:
                                print(f"使用ID定位器: #{element_identifier['id']}")
                                return locator
                        except:
                            pass
                    except:
                        pass
                
                # 清理base_selector，确保它不会导致重复的//tr
                # 检查base_selector是否已经包含//tr
                if "//tr" in base_selector:
                    # 如果已经包含//tr，直接添加/td
                    # 例如：//table//tr[position()>=3] 变成 //table//tr[position()>=3]/td[7]
                    td_selector = f"{base_selector}/td[{column}]"
                else:
                    # 否则，添加//tr/td
                    td_selector = f"{base_selector}//tr/td[{column}]"
                
                # 打印构建的选择器，方便调试
                print(f"构建的选择器: {td_selector}")
                
                # 尝试多种定位策略（减少策略数量，提高速度）
                strategies = [
                    # 1. 优先定位有id属性的单元格
                    f"{td_selector}[@id]",
                    # 2. 通用定位
                    td_selector
                ]
                
                # 尝试每个策略
                for strategy in strategies:
                    try:
                        locator = self.page.locator(strategy)
                        # 直接尝试获取元素，不先调用count()
                        try:
                            # 尝试获取第一个元素
                            first_element = locator.first
                            # 检查元素是否存在
                            is_visible = self._run_async(first_element.is_visible())
                            if is_visible:
                                print(f"使用表格定位策略: {strategy}")
                                # 如果匹配到多个元素，根据row_index选择对应的元素
                                try:
                                    # 只在需要时才调用count()
                                    if row_index > 0:
                                        count = self._run_async(locator.count())
                                        if count > 1 and row_index < count:
                                            print(f"匹配到多个元素，使用第 {row_index + 1} 个元素")
                                            return locator.nth(row_index)
                                    # 默认返回第一个元素
                                    return locator.first
                                except:
                                    # 如果count()失败，直接返回第一个元素
                                    return locator.first
                        except Exception as e:
                            print(f"策略 {strategy} 获取元素失败: {e}")
                            continue
                    except Exception as e:
                        print(f"策略 {strategy} 失败: {e}")
                        continue
                
                # 不再使用硬编码的单元格ID，因为它可能不正确
                # 直接使用基于列号的定位器
                
                # 如果所有策略都失败，使用原始的定位器
                print("警告: 所有表格定位策略都失败，使用原始定位器")
                final_locator = self.page.locator(td_selector)
                return final_locator.first
            else:
                raise Exception('元素标识符格式错误')
        except Exception as e:
            raise Exception(f"无法找到元素: {element_identifier}, 错误: {e}")
    
    def fill_input(self, element_identifier, value, row_index=0):
        """填写输入框
        
        Args:
            element_identifier (dict): 元素标识符
            value (str): 要填写的值
            row_index (int): 数据行索引
        """
        try:
            locator = self._find_element(element_identifier, row_index)
            # 等待元素可见
            self._run_async(locator.wait_for(state='visible', timeout=1000))
            
            # 尝试找到内部的input元素
            input_locator = None
            try:
                # 尝试在找到的元素内查找input元素
                input_locator = locator.locator("input")
                # 直接尝试获取第一个input元素，不先调用count()
                try:
                    first_input = input_locator.first
                    is_visible = self._run_async(first_input.is_visible())
                    if is_visible:
                        print("找到内部input元素")
                        # 使用内部的input元素
                        locator = input_locator
                    else:
                        print("未找到内部input元素，使用原始locator")
                except:
                    print("未找到内部input元素，使用原始locator")
            except Exception as input_find_error:
                print(f"查找内部input元素失败: {input_find_error}")
            
            # 尝试直接填充值
            try:
                self._run_async(locator.fill(str(value)))
                print(f"已填写输入框: {element_identifier.get('id', element_identifier.get('class_name', 'unknown'))} = {value}")
            except Exception as fill_error:
                print(f"直接填充失败: {fill_error}")
                # 尝试点击元素，可能会弹出编辑框
                self._run_async(locator.click())
                # 减少等待时间，从1000ms减少到200ms
                self._run_async(self.page.wait_for_timeout(200))
                
                # 尝试找到当前聚焦的元素并输入
                try:
                    # 尝试在当前聚焦的元素上输入
                    self._run_async(self.page.keyboard.type(str(value)))
                    print(f"已点击并输入值: {element_identifier.get('id', element_identifier.get('class_name', 'unknown'))} = {value}")
                except Exception as keyboard_error:
                    print(f"键盘输入失败: {keyboard_error}")
                    # 尝试查找新生成的输入框
                    try:
                        # 查找可能新生成的输入框
                        input_locator = self.page.locator("input:focus")
                        count = self._run_async(input_locator.count())
                        if count > 0:
                            self._run_async(input_locator.fill(str(value)))
                            print(f"已找到并填写新生成的输入框: {value}")
                        else:
                            # 尝试查找所有可见的输入框
                            input_locator = self.page.locator("input:visible")
                            # 直接尝试获取第一个输入框，不先调用count()
                            try:
                                first_input = input_locator.first
                                is_visible = self._run_async(first_input.is_visible())
                                if is_visible:
                                    self._run_async(first_input.fill(str(value)))
                                    print(f"已找到并填写第一个可见的输入框: {value}")
                                else:
                                    print("无法找到可填写的输入框")
                            except Exception as visible_input_error:
                                print(f"查找可见输入框失败: {visible_input_error}")
                                print("无法找到可填写的输入框")
                    except Exception as input_error:
                        print(f"查找输入框失败: {input_error}")
        except Exception as e:
            print(f"填写输入框时出错: {e}")
            # 出错时不关闭浏览器，继续执行
    
    def select_option(self, element_identifier, value, row_index=0):
        """选择下拉框选项
        
        Args:
            element_identifier (dict): 元素标识符
            value (str): 要选择的值
            row_index (int): 数据行索引
        """
        try:
            locator = self._find_element(element_identifier, row_index)
            # 等待元素可见
            self._run_async(locator.wait_for(state='visible', timeout=100))
            
            # 尝试找到内部的select元素
            select_locator = None
            try:
                # 尝试在找到的元素内查找select元素
                select_locator = locator.locator("select")
                # 直接尝试获取第一个select元素，不先调用count()
                try:
                    first_select = select_locator.first
                    is_visible = self._run_async(first_select.is_visible())
                    if is_visible:
                        print("找到内部select元素")
                        # 使用内部的select元素
                        locator = select_locator
                    else:
                        print("未找到内部select元素，使用原始locator")
                except:
                    print("未找到内部select元素，使用原始locator")
            except Exception as select_find_error:
                print(f"查找内部select元素失败: {select_find_error}")
            
            # 尝试选择选项
            # 首先尝试按值选择（从错误信息看这个成功率更高）
            try:
                self._run_async(locator.select_option(value=str(value)))
                print(f"成功选择选项（按值）: {value}")
                return
            except Exception as value_error:
                print(f"按值选择失败: {value_error}")
                
                # 尝试按可见文本选择
                try:
                    self._run_async(locator.select_option(label=str(value)))
                    print(f"成功选择选项（按文本）: {value}")
                    return
                except Exception as label_error:
                    print(f"按文本选择失败: {label_error}")
                    
                    # 尝试按索引选择
                    try:
                        index = int(value)
                        self._run_async(locator.select_option(index=index))
                        print(f"成功选择选项（按索引）: {value}")
                        return
                    except Exception as index_error:
                        print(f"按索引选择失败: {index_error}")
                        
                        # 如果所有标准方法都失败，使用点击方式
                        print("尝试使用点击方式选择选项...")
                        try:
                            # 点击下拉框展开
                            self._run_async(locator.click())
                            print("已点击下拉框")
                            
                            # 减少等待时间，从1500ms减少到500ms
                            self._run_async(self.page.wait_for_timeout(500))
                            
                            # 尝试查找包含目标文本的选项
                            option_selectors = [
                                f"option:has-text('{value}')",
                                f"li:has-text('{value}')",
                                f"div:has-text('{value}')",
                                f"span:has-text('{value}')",
                                f"[role='option']:has-text('{value}')",
                            ]
                            
                            option_found = False
                            for option_selector in option_selectors:
                                try:
                                    option_locator = self.page.locator(option_selector)
                                    # 直接尝试获取第一个选项，不先调用count()
                                    try:
                                        first_option = option_locator.first
                                        # 等待选项可见
                                        self._run_async(first_option.wait_for(state='visible', timeout=3000))
                                        print(f"找到匹配的选项: {option_selector}")
                                        # 点击第一个匹配的选项
                                        self._run_async(first_option.click())
                                        print(f"成功点击选项: {value}")
                                        option_found = True
                                        break
                                    except Exception as option_error:
                                        print(f"使用选择器 {option_selector} 查找选项失败: {option_error}")
                                        continue
                                except Exception as option_error:
                                    print(f"使用选择器 {option_selector} 查找选项失败: {option_error}")
                                    continue
                            
                            if not option_found:
                                # 如果找不到选项，尝试使用键盘导航
                                print("未找到选项，尝试使用键盘导航...")
                                # 按下箭头键展开下拉列表
                                self._run_async(self.page.keyboard.press("ArrowDown"))
                                self._run_async(self.page.wait_for_timeout(500))
                                
                                # 尝试输入部分文本来过滤选项
                                self._run_async(self.page.keyboard.type(str(value)))
                                self._run_async(self.page.wait_for_timeout(800))
                            
                            # 按Enter确认
                            self._run_async(self.page.keyboard.press("Enter"))
                            print(f"已使用键盘输入选项: {value}")
                            
                        except Exception as click_error:
                            print(f"点击方式选择选项失败: {click_error}")
                            raise
        except Exception as e:
            print(f"选择下拉框选项时出错: {e}")
            # 出错时不关闭浏览器，继续执行
    
    def fill_textarea(self, element_identifier, value, row_index=0):
        """填写文本区域
        
        Args:
            element_identifier (dict): 元素标识符
            value (str): 要填写的值
            row_index (int): 数据行索引
        """
        try:
            locator = self._find_element(element_identifier, row_index)
            # 等待元素可见
            self._run_async(locator.wait_for(state='visible', timeout=10000))
            
            # 尝试直接填充值
            try:
                self._run_async(locator.fill(str(value)))
                print(f"已填写文本区域: {element_identifier.get('id', element_identifier.get('class_name', 'unknown'))} = {value}")
            except Exception as fill_error:
                print(f"直接填充失败: {fill_error}")
                # 尝试点击元素
                self._run_async(locator.click())
                self._run_async(self.page.wait_for_timeout(200))
                
                # 尝试使用键盘输入
                try:
                    self._run_async(self.page.keyboard.type(str(value)))
                    print(f"已点击并输入值: {element_identifier.get('id', element_identifier.get('class_name', 'unknown'))} = {value}")
                except Exception as keyboard_error:
                    print(f"键盘输入失败: {keyboard_error}")
        except Exception as e:
            print(f"填写文本区域时出错: {e}")
            # 出错时不关闭浏览器，继续执行
    
    def close(self):
        """关闭浏览器（已禁用）"""
        print('关闭浏览器功能已禁用，保持浏览器打开')
        # 不关闭浏览器，保持打开状态
