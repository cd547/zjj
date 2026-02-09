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
        self._connect()
    
    def _connect(self):
        """连接到网页"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 在事件循环中运行异步连接
            loop.run_until_complete(self._connect_async())
            
        except Exception as e:
            print(f"连接到网页失败: {e}")
            self.is_connected = False
            # 不清理资源，保持浏览器打开
            print('保持浏览器打开状态，不清理资源')
    
    async def _connect_async(self):
        """异步连接到网页"""
        try:
            # 启动Playwright
            self.playwright = await async_playwright().start()
            # 启动浏览器（默认使用Chrome）
            print('正在启动浏览器...')
            
            # 尝试使用系统已安装的Chrome浏览器
            chrome_paths = [
                "C:\Program Files\Google\Chrome\Application\chrome.exe",
                "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            
            browser_launched = False
            for chrome_path in chrome_paths:
                try:
                    print(f'尝试使用Chrome路径: {chrome_path}')
                    self.browser = await self.playwright.chromium.launch(
                        headless=False,  # 显示浏览器窗口
                        slow_mo=50,  # 减慢操作速度，便于观察（从100ms减少到50ms）
                        executable_path=chrome_path  # 系统Chrome路径
                    )
                    browser_launched = True
                    break
                except Exception as e:
                    print(f'使用路径 {chrome_path} 失败: {e}')
            
            # 如果所有路径都失败，使用Playwright默认的浏览器
            if not browser_launched:
                print('使用系统Chrome失败，尝试使用Playwright默认浏览器...')
                self.browser = await self.playwright.chromium.launch(
                    headless=False,  # 显示浏览器窗口
                    slow_mo=100  # 减慢操作速度，便于观察
                )
            # 创建新页面
            self.page = await self.browser.new_page()
            # 导航到目标URL
            print(f'正在导航到: {self.url}')
            # 减少页面加载等待时间，从'networkidle'改为'load'，这样页面加载完成后就开始操作
            await self.page.goto(self.url, wait_until='load')
            self.is_connected = True
            print('连接成功！')
                
        except Exception as e:
            print(f"连接到网页失败: {e}")
            self.is_connected = False
            # 不清理资源，保持浏览器打开
            print('保持浏览器打开状态，不清理资源')
    
    def _cleanup(self):
        """清理资源（已禁用）"""
        print('清理资源功能已禁用，保持浏览器打开')
        # 不清理任何资源，保持浏览器完全打开状态
    
    def _run_async(self, coro):
        """运行异步函数"""
        try:
            # 创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # 运行异步函数
            return loop.run_until_complete(coro)
        except Exception as e:
            print(f"运行异步函数失败: {e}")
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
                        count = self._run_async(locator.count())
                        if count > 0:
                            print(f"使用ID定位器: #{element_identifier['id']}")
                            return locator
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
                
                # 尝试多种定位策略
                strategies = [
                    # 1. 优先定位有id属性的单元格，并考虑row_index
                    f"{td_selector}[@id]",
                    # 2. 排除表头行，并考虑row_index
                    f"{base_selector}//tr[not(contains(@class, 'header')) and not(contains(@class, 'dxgvHeader'))][position()={row_index + 1}]/td[{column}]",
                    # 3. 基于row_index的精确行定位
                    f"{base_selector}//tr[position()={row_index + 3}]/td[{column}]",  # 假设从第3行开始是数据
                    # 4. 排除可能的空单元格（包含文本或有class的）
                    f"{td_selector}[text() or @class]",
                    # 5. 通用定位
                    td_selector
                ]
                
                # 尝试每个策略
                for strategy in strategies:
                    try:
                        locator = self.page.locator(strategy)
                        count = self._run_async(locator.count())
                        if count > 0:
                            print(f"使用表格定位策略: {strategy} (匹配到 {count} 个元素)")
                            # 打印匹配到的元素信息
                            print("匹配到的元素信息:")
                            for i in range(min(count, 5)):  # 最多打印前5个元素
                                try:
                                    element = locator.nth(i)
                                    # 获取元素的基本信息
                                    element_info = {
                                        "index": i,
                                        "is_visible": self._run_async(element.is_visible()),
                                        "is_enabled": self._run_async(element.is_enabled()),
                                        "is_editable": self._run_async(element.is_editable()),
                                        "bounding_box": self._run_async(element.bounding_box())
                                    }
                                    print(f"  元素 {i}: {element_info}")
                                    
                                    # 获取元素的HTML结构
                                    html = self._run_async(element.inner_html())
                                    outer_html = self._run_async(element.outer_html())
                                    print(f"  元素 {i} 完整HTML: {outer_html}")
                                    print(f"  元素 {i} 内部HTML: {html}")
                                    
                                    # 获取元素的属性
                                    attrs = self._run_async(element.get_attribute_names())
                                    attr_info = {}
                                    for attr in attrs[:10]:  # 最多获取10个属性
                                        try:
                                            attr_info[attr] = self._run_async(element.get_attribute(attr))
                                        except:
                                            pass
                                    print(f"  元素 {i} 属性: {attr_info}")
                                except Exception as e:
                                    print(f"  元素 {i}: 获取信息失败 - {e}")
                            # 如果匹配到多个元素，根据row_index选择对应的元素
                            if count > 1:
                                if row_index < count:
                                    print(f"匹配到多个元素，使用第 {row_index + 1} 个元素")
                                    return locator.nth(row_index)
                                else:
                                    print(f"row_index {row_index} 超出元素数量 {count}，使用第一个元素")
                                    return locator.first
                            return locator
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
            self._run_async(locator.wait_for(state='visible', timeout=10000))
            
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
                            count = self._run_async(input_locator.count())
                            if count > 0:
                                self._run_async(input_locator.first.fill(str(value)))
                                print(f"已找到并填写第一个可见的输入框: {value}")
                            else:
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
            self._run_async(locator.wait_for(state='visible', timeout=10000))
            
            # 尝试选择选项
            try:
                # 按可见文本选择
                self._run_async(locator.select_option(label=str(value)))
            except:
                try:
                    # 按值选择
                    self._run_async(locator.select_option(value=str(value)))
                except:
                    try:
                        # 按索引选择
                        index = int(value)
                        self._run_async(locator.select_option(index=index))
                    except Exception as select_error:
                        print(f"直接选择失败: {select_error}")
                        # 尝试点击下拉框，然后输入选项
                        try:
                            self._run_async(locator.click())
                            self._run_async(self.page.wait_for_timeout(500))
                            # 输入选项
                            self._run_async(self.page.keyboard.type(str(value)))
                            # 按Enter确认
                            self._run_async(self.page.keyboard.press("Enter"))
                            print(f"已点击并输入选项: {value}")
                        except Exception as click_error:
                            print(f"点击并输入选项失败: {click_error}")
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
