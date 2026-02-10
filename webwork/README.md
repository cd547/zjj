# Excel数据自动填入网页工具

本工具可以将Excel文件中的数据自动填入到网页表单中，支持多种网页元素类型和元素定位方式，提供GUI界面和命令行两种使用方式。

## 功能特点

- 支持读取Excel文件中的数据
- 自动计算Excel数据结束行
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

## 使用方法

### 方法一：使用GUI界面（推荐）

1. **直接运行可执行文件**：
   - 双击 `excel_web_filler.exe` 运行
   - 或在命令行中运行：`python gui.py`

2. **使用步骤**：
   - 在"URL地址"输入框中输入网页地址（可选，优先级高于配置文件）
   - 点击"浏览"按钮选择Excel文件
   - 点击"配置"按钮打开配置文件管理对话框
   - 选择或修改配置文件
   - 点击"连接网页"按钮连接到目标网页
   - 点击"自动填表"按钮开始自动填表
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

1. 确保Excel文件中的字段名与配置文件中的`excel_field`一致
2. 确保网页元素标识符（如ID、class name等）正确无误
3. 对于下拉选择框，工具会尝试按可见文本、值或索引进行选择
4. 如果网页加载较慢，可能需要调整代码中的等待时间
5. 本工具仅用于自动化数据填入，不支持复杂的网页交互操作
6. 截图文件会保存在可执行文件所在目录的`img`子目录下
7. 日志文件会保存在可执行文件所在目录的`logs`子目录下

## 故障排除

- **无法连接到网页**：请确保Chrome浏览器已安装，Playwright会自动下载和管理浏览器驱动
- **元素未找到**：请检查配置文件中的元素标识符是否正确，确保网页已完全加载
- **数据填入失败**：请检查Excel文件中的字段名是否与配置文件一致
- **Playwright浏览器下载失败**：请确保网络连接正常，或手动运行 `playwright install` 命令安装浏览器
- **配置文件未找到**：请在可执行文件所在目录的`cfg`文件夹中放置`default.json`文件
- **截图失败**：请确保可执行文件所在目录有写权限，或手动创建`img`目录

## 许可证

本项目采用MIT许可证。
