# Excel数据自动填入网页工具

本工具可以将Excel文件中的数据自动填入到网页表单中，支持多种网页元素类型和元素定位方式，提供GUI界面和命令行两种使用方式。

## 功能特点

- 支持读取Excel文件中的数据
- 自动计算Excel数据结束行
- Excel文件格式自动验证（导入时立即验证表头格式）
- 支持连接到已打开的网页（如果未打开则启动新的浏览器）
- 支持多种网页元素类型：输入框、下拉选择框、文本域
- 支持多种元素定位方式：ID、class name、文本内容、XPath、CSS选择器
- 通过配置文件定义Excel字段与网页元素的映射关系
- 提供直观的GUI界面
- 支持URL输入框，可直接在界面中输入网页地址
- 自动检测满足条件的表格元素
- 动态生成表格标识符
- 顺序填表逻辑，确保数据按Excel顺序填入
- 日志文件输出功能
- 配置文件可选，默认使用cfg/default.json
- 页面截图功能
- 从Excel中自动提取Discount值
- 强制Chrome显示滚动条
- 表格检测功能（独立按钮，显示检测耗时）

## 依赖环境

- Python 3.7+
- 安装依赖包：
  ```
  pip install playwright openpyxl
  ```
  安装完playwright后，运行以下命令安装浏览器（可选，playwright会在运行时自动下载所需浏览器）：
  ```
  playwright install
  ```
- Chrome浏览器（Playwright会自动管理浏览器驱动）

## 项目结构
webwork/
├── gui.py              # GUI界面主程序
├── main.py             # 命令行主程序
├── excel_reader.py      # Excel数据读取模块
├── web_automator.py     # 网页自动化模块
├── build.py            # 打包脚本
├── simple_test.py       # 简单测试脚本
├── test_form.html       # 测试HTML文件
├── config_szq_template.json  # 配置文件模板
└── README.md           # 项目文档

## 使用方法

### 方法一：使用GUI界面（推荐）

1. **直接运行可执行文件**：
   - 双击 `excel_web_filler.exe` 运行
   - 或在命令行中运行：`python gui.py`

2. **使用步骤**：
   - 在"URL地址"输入框中输入网页地址（可选，优先级高于配置文件）
   - 点击"浏览"按钮选择Excel文件
     - 系统会立即验证Excel文件格式
     - 验证成功：显示读取的数据行数和Discount值
     - 验证失败：显示详细的错误信息并弹窗提示
   - 点击"配置"按钮打开配置文件管理对话框
   - 选择或修改配置文件
   - 点击"连接网页"按钮连接到目标网页
     - 启动浏览器（系统Chrome或Playwright默认）
     - 导航到URL
     - 自动检测满足条件的表格元素
     - 显示浏览器启动日志
   - 点击"检测表格"按钮检测页面中的表格
     - 显示检测耗时
     - 列出所有符合条件的表格
   - 点击"自动填表"按钮开始自动填表
     - 读取Excel数据（已在导入时验证过）
     - 按表格顺序处理数据
     - 顺序填入数据
   - 点击"页面截图"按钮保存当前页面截图

### 方法二：使用命令行

```bash
python main.py <excel_file> <config_file> [--url <url>]
```

参数说明：
- `excel_file`: Excel文件路径
- `config_file`: 配置文件路径
- `--url`: （可选）网页URL，优先级高于配置文件中的URL

## 配置文件说明

### Excel文件格式要求

**Excel表头验证规则**：
- Excel文件的第16行必须是表头行
- 表头必须严格按照以下顺序和内容：
  1. `No.`
  2. `IMPA`
  3. `Description`
  4. `Remark`
  5. `Q'ty`
  6. `Unit`
  7. `Unit Price   (USD)`
  8. `Amount   (USD)`
  9. `Brand`

**验证时机**：
- 导入Excel文件时立即进行验证
- 验证失败会显示详细的错误信息并弹窗提示
- 错误信息会显示在GUI界面和日志文件中

**示例错误信息**：
```
Excel文件格式验证失败: 表头第 1 列不匹配，预期: 'No.'，实际: 'No1.'
```

**验证成功示例**：
```
正在验证Excel文件格式: D:\test.xlsx
Excel表头验证通过！
✓ Excel文件格式验证通过
✓ 共读取 6 行数据
✓ 找到Discount值: 16
```

创建配置文件（如`config.json`），定义Excel字段与网页元素的映射关系：

```json
{
    "url": "https://example.com/form",
    "excel_config": {
        "header_row": 16,
        "start_row": 17,
        "end_row": null,
        "discount": null,
        "oem_type": ["Compatible", "OEM", "Genuine"]
    },
    "field_mappings": [
        {
            "excel_field": "姓名",
            "web_element": {
                "id": "name"
            },
            "element_type": "input"
        },
        {
            "excel_field": "性别",
            "web_element": {
                "id": "gender"
            },
            "element_type": "select"
        },
        {
            "excel_field": null,
            "web_element": {
                "table_column": 9,
                "table_identifier": "//table[@id='CPH_QGV_dxdt0_QDGV_0_DXMainTable']//tr[position()>=3]"
            },
            "element_type": "input",
            "default_value": "{{discount}}"
        }
    ]
}
```

配置说明：
- `url`: 网页URL
- `excel_config`: Excel配置
  - `header_row`: 表头所在行
  - `start_row`: 数据开始行
  - `end_row`: 数据结束行（null表示自动计算）
  - `discount`: 折扣值（null表示从Excel中自动提取）
  - `oem_type`: OEM类型列表
- `field_mappings`: 字段映射列表
  - `excel_field`: Excel中的字段名（null表示使用默认值）
  - `web_element`: 网页元素标识符（支持id、class_name、text、xpath、css_selector、table_column、table_identifier）
  - `element_type`: 元素类型（input、select、textarea）
  - `default_value`: 默认值（"{{discount}}"表示使用自动提取的Discount值）

## 示例

### Excel文件格式

| 姓名 | 年龄 | 性别 | 邮箱 | 地址 |
|------|------|------|------|------|
| 张三 | 25   | 男   | zhangsan@example.com | 北京市朝阳区 |
| 李四 | 30   | 女   | lisi@example.com | 上海市浦东新区 |

### 运行命令

```bash
python main.py data.xlsx config.json
```

## 注意事项

1. **Excel文件格式要求**：
   - 第16行必须是表头行，内容必须严格按照指定格式
   - 表头字段：No.、IMPA、Description、Remark、Q'ty、Unit、Unit Price   (USD)、Amount   (USD)、Brand
   - 导入Excel文件时会立即进行格式验证
   - 验证失败会显示详细的错误信息并弹窗提示

2. **错误处理机制**：
   - 所有错误信息会显示在GUI界面的输出窗口
   - 所有错误信息会写入日志文件（logs目录）
   - 关键错误会弹窗提示用户
   - Excel验证失败会阻止后续操作

3. 确保Excel文件中的字段名与配置文件中的`excel_field`一致
4. 确保网页元素标识符（如ID、class name等）正确无误
5. 对于下拉选择框，工具会尝试按可见文本、值或索引进行选择
6. 如果网页加载较慢，可能需要调整代码中的等待时间
7. 本工具仅用于自动化数据填入，不支持复杂的网页交互操作
8. 截图文件会保存在可执行文件所在目录的`img`子目录下
9. 日志文件会保存在可执行文件所在目录的`logs`子目录下

## 故障排除

- **Excel文件格式验证失败**：
  - 检查第16行的表头是否正确
  - 确保表头字段名称和顺序完全匹配
  - 查看详细的错误信息，定位具体哪一列不匹配

- **无法连接到网页**：请确保Chrome浏览器已安装，Playwright会自动下载和管理浏览器驱动
- **元素未找到**：请检查配置文件中的元素标识符是否正确，确保网页已完全加载
- **数据填入失败**：请检查Excel文件中的字段名是否与配置文件一致
- **Playwright浏览器下载失败**：请确保网络连接正常，或手动运行 `playwright install` 命令安装浏览器
- **配置文件未找到**：请在可执行文件所在目录的`cfg`文件夹中放置`default.json`文件
- **截图失败**：请确保可执行文件所在目录有写权限，或手动创建`img`目录

## 项目架构

### 项目结构

```
webwork/
├── gui.py              # GUI界面主程序
├── main.py             # 命令行主程序
├── excel_reader.py      # Excel数据读取模块
├── web_automator.py     # 网页自动化模块
├── build.py            # 打包脚本
├── simple_test.py       # 简单测试脚本
├── test_form.html       # 测试HTML文件
├── config_szq_template.json  # 配置文件模板
└── README.md           # 项目文档
```

### 核心模块

#### 1. Excel数据读取模块 (excel_reader.py)

**主要功能**：
- 读取Excel文件中的数据
- 自动计算数据结束行
- 自动提取Discount值

**关键方法**：
- `__init__(excel_file, header_row, start_row, end_row)`: 初始化读取器
- `read_data()`: 读取数据并返回(data, discount_value)

**技术实现**：
- 使用openpyxl库读取Excel文件
- 从指定行开始读取数据
- 自动检测第一列为空或非数字的行作为结束行
- 从表格末尾倒序查找Discount值（F列"Discount  :"，H列百分比值）
- 支持字符串和数字两种Discount格式（如"16%"或0.16）

#### 2. 网页自动化模块 (web_automator.py)

**主要功能**：
- 启动和管理浏览器
- 连接到指定URL
- 检测满足条件的表格元素
- 填入各种类型的网页元素
- 截图功能
- 日志记录

**关键方法**：
- `__init__(url)`: 初始化并连接到网页
- `_connect()`: 创建事件循环并运行异步连接
- `_connect_async()`: 异步连接到网页，启动浏览器
- `_detect_tables()`: 检测符合格式的表格元素
- `_find_element(element_identifier, row_index)`: 查找网页元素
- `fill_input(element_identifier, value, row_index)`: 填入输入框
- `select_option(element_identifier, value, row_index)`: 选择下拉框选项
- `fill_textarea(element_identifier, value, row_index)`: 填入文本域
- `screenshot(file_path)`: 截图当前页面
- `_log(message)`: 记录日志信息
- `_run_async(coro)`: 运行异步函数

**技术实现**：
- 使用Playwright库进行网页自动化
- 支持Chromium浏览器（Chrome）
- 异步编程模型（async/await）
- 多种元素定位方式：ID、class name、text、xpath、css_selector、table_column
- 支持表格列定位（table_column + table_identifier）
- 日志记录机制（logs列表存储）
- 强制显示滚动条（CSS注入 + Chrome启动参数）
- 支持全页面截图

#### 3. GUI界面模块 (gui.py)

**主要功能**：
- 提供图形用户界面
- 文件选择和配置管理
- Excel文件格式自动验证
- 连接网页和自动填表
- 表格检测功能
- 页面截图
- 日志文件输出
- 错误处理和用户提示

**关键方法**：
- `__init__(root)`: 初始化GUI界面
- `_init_log_file()`: 初始化日志文件
- `create_file_selection()`: 创建文件选择区域
- `create_start_button()`: 创建按钮区域（四个按钮）
- `create_output_window()`: 创建输出窗口
- `browse_excel()`: 浏览选择Excel文件（自动验证格式）
- `validate_excel_format(excel_file)`: 验证Excel文件格式
- `open_config_dialog()`: 打开配置文件管理对话框
- `connect_to_webpage()`: 连接到网页
- `execute_connect()`: 执行连接操作
- `detect_tables()`: 执行表格检测操作
- `execute_detect_tables()`: 执行表格检测的具体逻辑
- `fill_table()`: 执行填表操作
- `execute_fill()`: 执行填表命令
- `take_screenshot()`: 执行页面截图
- `append_output(text)`: 向输出窗口添加文本并写入日志文件
- `set_button_states()`: 统一设置按钮状态

**四个按钮功能**：
1. **连接网页**（蓝色）：
   - 连接到目标网页
   - 启动浏览器（系统Chrome或Playwright默认）
   - 导航到URL
   - 自动检测满足条件的表格元素
   - 显示浏览器启动日志

2. **自动填表**（绿色）：
   - 读取Excel数据（已在导入时验证过）
   - 按表格顺序处理数据
   - 顺序填入数据
   - 处理{{discount}}占位符
   - 处理Brand字段特殊映射

3. **检测表格**（紫色）：
   - 检测页面中的表格元素
   - 显示检测耗时
   - 列出所有符合条件的表格
   - 表格ID格式：CPH_QGV_dxdt数字_QDGV_数字_DXMainTable

4. **页面截图**（橙色）：
   - 保存当前页面截图
   - 创建img目录
   - 生成时间戳文件名
   - 保存截图到img目录

**技术实现**：
- 使用Tkinter库构建GUI
- 支持URL输入框（优先级高于配置文件）
- 配置文件可选（默认使用cfg/default.json）
- 自动创建logs和img目录
- 日志文件自动命名（基于时间戳）
- 截图文件自动命名（基于时间戳）
- 配置文件弹出框（模态窗口）
- 实时日志显示和文件记录
- Excel文件格式自动验证
- 错误处理和用户提示
- 按钮状态统一管理

#### 4. 命令行主程序 (main.py)

**主要功能**：
- 命令行参数解析
- 配置文件加载
- Excel数据读取
- 网页连接和数据填入

**关键方法**：
- `load_config(config_file)`: 加载配置文件
- `main()`: 主函数，处理命令行参数和执行流程

**技术实现**：
- 使用argparse解析命令行参数
- 支持Excel文件、配置文件、URL参数
- 顺序处理Excel数据行
- 支持Brand字段特殊映射（到oem_type索引）
- 支持默认值和discount值
- 错误处理和继续执行机制

#### 5. 打包脚本 (build.py)

**主要功能**：
- 检查必要文件
- 构建PyInstaller命令
- 执行打包操作

**技术实现**：
- 使用PyInstaller打包为单文件exe
- 只打包必要的Python模块（gui.py、main.py、excel_reader.py、web_automator.py）
- 不打包配置文件（使用cfg/default.json）
- 支持hidden-import选项

### 核心功能流程

#### GUI模式流程
```
1. 用户启动程序（gui.py）
2. 选择Excel文件
   - 系统立即验证Excel文件格式
   - 验证第16行表头是否符合要求
   - 验证成功：显示读取的数据行数和Discount值
   - 验证失败：显示详细的错误信息并弹窗提示
3. 选择或使用默认配置文件
4. 输入URL（可选）
5. 点击"连接网页"按钮
   - 创建WebAutomator实例
   - 启动浏览器（系统Chrome或Playwright默认）
   - 导航到URL
   - 注入CSS强制显示滚动条
   - 检测满足条件的表格元素
   - 显示浏览器启动日志
6. 点击"检测表格"按钮（可选）
   - 检测页面中的表格元素
   - 显示检测耗时
   - 列出所有符合条件的表格
7. 点击"自动填表"按钮
   - 读取Excel数据（已在导入时验证过）
   - 按表格顺序处理数据
   - 动态生成table_identifier
   - 顺序填入数据（单Excel行索引跨所有表格）
   - 处理{{discount}}占位符
   - 处理Brand字段特殊映射
7. 点击"页面截图"按钮（可选）
   - 创建img目录
   - 生成时间戳文件名
   - 保存截图
```

#### 命令行模式流程
```
1. 用户运行命令（main.py）
2. 解析命令行参数
3. 加载配置文件
4. 读取Excel数据
5. 连接到网页
6. 顺序处理每个数据行
   - 处理每个字段映射
   - 确定使用的值（默认值 > Excel值 > discount值）
   - 填入网页元素
7. 完成并保持浏览器打开
```

### 关键技术特性

#### 1. Excel数据处理
- 自动计算数据结束行（检测第一列为空或非数字）
- 支持灵活的表头和数据行配置
- 自动提取Discount值（从表格末尾倒序查找）
- 支持百分比和数字两种Discount格式

#### 2. 网页自动化
- 异步编程模型（提高性能）
- 多种元素定位方式（ID、class、text、xpath、css_selector、table_column）
- 智能元素查找（尝试多种策略）
- 动态表格标识符生成（支持多个表格）
- 强制显示滚动条（CSS注入 + Chrome参数）

#### 3. 数据填入逻辑
- 顺序填表（单Excel行索引跨所有表格）
- 值优先级：默认值 > Excel值 > discount值
- 支持占位符（{{discount}}）
- 支持特殊字段映射（Brand → oem_type索引）
- 错误处理和继续执行

#### 4. 配置管理
- 配置文件可选（默认使用cfg/default.json）
- 支持弹出框配置管理
- 支持URL输入框（优先级高于配置文件）
- 灵活的字段映射配置

#### 5. 日志和截图
- 实时日志显示（GUI输出窗口）
- 日志文件输出（logs目录）
- 页面截图功能（img目录）
- 自动文件命名（基于时间戳）

### 依赖库

- **Playwright**: 网页自动化
- **openpyxl**: Excel文件读取
- **Tkinter**: GUI界面（Python标准库）
- **asyncio**: 异步编程（Python标准库）
- **json**: JSON配置文件（Python标准库）
- **argparse**: 命令行参数（Python标准库）
- **datetime**: 时间戳生成（Python标准库）
- **re**: 正则表达式（Python标准库）

### 性能优化

1. **异步编程**: 使用async/await提高网页操作效率
2. **智能等待**: 使用Playwright的内置等待机制
3. **CSS注入**: 强制显示滚动条，避免重复操作
4. **批量处理**: 顺序处理数据行，减少浏览器操作

### 错误处理

1. **Excel读取错误**: 捕获异常并返回空数据
2. **网页连接错误**: 保持浏览器打开，不清理资源
3. **元素定位错误**: 尝试多种策略，继续处理
4. **数据填入错误**: 记录错误，继续处理下一个字段
5. **目录创建错误**: 使用备用目录（临时目录）

## 许可证

本项目采用MIT许可证。
