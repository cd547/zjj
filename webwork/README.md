# Excel数据自动填入网页工具

本工具可以将Excel文件中的数据自动填入到网页表单中，支持多种网页元素类型和元素定位方式。

## 功能特点

- 支持读取Excel文件中的数据
- 支持连接到已打开的网页（如果未打开则启动新的浏览器）
- 支持多种网页元素类型：输入框、下拉选择框、文本域
- 支持多种元素定位方式：ID、class name、文本内容、XPath、CSS选择器
- 通过配置文件定义Excel字段与网页元素的映射关系

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

### 1. 准备工作

1. 确保Chrome浏览器已安装（Playwright也支持Firefox和Safari）
2. 安装依赖包并（可选）预先安装浏览器：
   ```
   pip install playwright openpyxl
   playwright install  # 可选，预先安装浏览器
   ```

### 2. 配置文件

创建配置文件（如`config.json`），定义Excel字段与网页元素的映射关系：

```json
{
    "url": "https://example.com/form",
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
        }
    ]
}
```

配置说明：
- `url`: 网页URL
- `field_mappings`: 字段映射列表
  - `excel_field`: Excel中的字段名
  - `web_element`: 网页元素标识符（支持id、class_name、text、xpath、css_selector）
  - `element_type`: 元素类型（input、select、textarea）

### 3. 运行工具

```bash
python main.py <excel_file> <config_file> [--url <url>]
```

参数说明：
- `excel_file`: Excel文件路径
- `config_file`: 配置文件路径
- `--url`: （可选）网页URL，优先级高于配置文件中的URL

## 示例

### Excel文件格式

| 姓名 | 年龄 | 性别 | 邮箱 | 地址 |
|------|------|------|------|------|
| 张三 | 25   | 男   | zhangsan@example.com | 北京市朝阳区 |
| 李四 | 30   | 女   | lisi@example.com | 上海市浦东新区 |

### 配置文件

```json
{
    "url": "https://example.com/form",
    "field_mappings": [
        {
            "excel_field": "姓名",
            "web_element": {
                "id": "name"
            },
            "element_type": "input"
        },
        {
            "excel_field": "年龄",
            "web_element": {
                "id": "age"
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
            "excel_field": "邮箱",
            "web_element": {
                "class_name": "email-input"
            },
            "element_type": "input"
        },
        {
            "excel_field": "地址",
            "web_element": {
                "xpath": "//textarea[@name='address']"
            },
            "element_type": "textarea"
        }
    ]
}
```

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

## 故障排除

- **无法连接到网页**：请确保Chrome浏览器已安装，Playwright会自动下载和管理浏览器驱动
- **元素未找到**：请检查配置文件中的元素标识符是否正确，确保网页已完全加载
- **数据填入失败**：请检查Excel文件中的字段名是否与配置文件一致
- **Playwright浏览器下载失败**：请确保网络连接正常，或手动运行 `playwright install` 命令安装浏览器

## 许可证

本项目采用MIT许可证。
