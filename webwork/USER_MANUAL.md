# Excel数据自动填入网页工具 - 使用手册

## 目录

1. [简介](#简介)
2. [系统要求](#系统要求)
3. [安装指南](#安装指南)
4. [快速开始](#快速开始)
5. [功能详解](#功能详解)
6. [配置说明](#配置说明)
7. [Excel文件格式](#excel文件格式)
8. [使用步骤](#使用步骤)
9. [常见问题](#常见问题)
10. [故障排除](#故障排除)
11. [附录](#附录)

---

## 简介

Excel数据自动填入网页工具是一个自动化工具，可以将Excel文件中的数据自动填入到网页表单中。该工具支持多种网页元素类型和元素定位方式，提供直观的GUI界面和命令行两种使用方式。

### 主要功能

- Excel数据自动读取和验证
- 网页自动化操作
- 支持多种网页元素类型（输入框、下拉选择框、文本域）
- 支持多种元素定位方式（ID、class name、文本内容、XPath、CSS选择器）
- 自动检测和填入多个表格
- 从Excel中自动提取Discount值
- 页面截图功能
- 日志记录功能

### 适用场景

- 批量数据录入
- 表单自动填写
- 网页数据导入
- 自动化测试

---

## 系统要求

### 软件要求

- **操作系统**：Windows 7/8/10/11
- **Python版本**：Python 3.7 或更高版本（推荐 3.13）
- **浏览器**：Chrome浏览器（推荐最新版本）

### 硬件要求

- **内存**：至少 2GB RAM（推荐 4GB 或更高）
- **磁盘空间**：至少 500MB 可用空间
- **网络**：需要网络连接（用于下载浏览器驱动）

---

## 安装指南

### 方法一：使用可执行文件（推荐）

1. **下载可执行文件**
   - 从项目发布页面下载 `excel_web_filler.exe`
   - 或使用打包脚本自行编译

2. **准备目录结构**
   ```
   excel_web_filler/
   ├── excel_web_filler.exe    # 主程序
   ├── cfg/                     # 配置文件目录
   │   └── default.json         # 默认配置文件
   ├── logs/                    # 日志文件目录（自动创建）
   └── img/                     # 截图文件目录（自动创建）
   ```

3. **配置默认配置文件**
   - 在 `cfg` 目录下创建 `default.json` 文件
   - 参考配置说明部分进行配置

4. **运行程序**
   - 双击 `excel_web_filler.exe` 启动程序

### 方法二：使用源代码

1. **克隆或下载项目**
   ```bash
   git clone <项目地址>
   cd webwork
   ```

2. **创建Python虚拟环境**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install playwright openpyxl pyinstaller
   playwright install
   ```

4. **运行程序**
   ```bash
   python gui.py
   ```

### 方法三：自行打包

1. **按照方法二安装依赖**
2. **运行打包脚本**
   ```bash
   python build.py
   ```
3. **打包完成后**，可执行文件位于 `dist` 目录

---

## 快速开始

### 第一次使用

1. **启动程序**
   - 双击 `excel_web_filler.exe` 或运行 `python gui.py`

2. **准备Excel文件**
   - 确保Excel文件格式符合要求（参见[Excel文件格式](#excel文件格式)）
   - 第16行必须是表头行

3. **配置文件**
   - 使用默认配置文件 `cfg/default.json`
   - 或点击"配置"按钮选择自定义配置文件

4. **选择Excel文件**
   - 点击"浏览"按钮选择Excel文件
   - 系统会自动验证文件格式

5. **连接网页**
   - 在"URL地址"输入框中输入网页地址（可选）
   - 点击"连接网页"按钮

6. **检测表格（可选）**
   - 点击"检测表格"按钮查看页面中的表格

7. **自动填表**
   - 点击"自动填表"按钮开始填表

8. **截图（可选）**
   - 点击"页面截图"按钮保存当前页面截图

### 最小配置示例

**Excel文件**：
- 第16行表头：No.、IMPA、Description、Remark、Q'ty、Unit、Unit Price   (USD)、Amount   (USD)、Brand
- 第17行开始数据

**配置文件**（`cfg/default.json`）：
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
            "excel_field": "No.",
            "web_element": {
                "id": "no"
            },
            "element_type": "input"
        }
    ]
}
```

---

## 功能详解

### 1. Excel文件格式验证

**功能说明**：
- 在导入Excel文件时立即进行格式验证
- 验证第16行的表头是否符合要求
- 验证成功显示读取的数据行数和Discount值
- 验证失败显示详细的错误信息

**验证规则**：
- 第16行必须是表头行
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
- 用户选择Excel文件后立即验证
- 执行填表操作时再次验证（防止配置不同导致的问题）

**错误处理**：
- 验证失败会显示详细的错误信息
- 错误信息会显示在GUI界面和日志文件中
- 关键错误会弹窗提示用户
- 验证失败会阻止后续操作

### 2. 连接网页

**功能说明**：
- 连接到指定的网页URL
- 启动浏览器（系统Chrome或Playwright默认）
- 自动检测满足条件的表格元素
- 显示浏览器启动日志

**操作步骤**：
1. 在"URL地址"输入框中输入网页地址（可选，优先级高于配置文件）
2. 点击"连接网页"按钮
3. 等待浏览器启动和页面加载
4. 查看日志输出确认连接成功

**注意事项**：
- 确保网络连接正常
- 确保URL地址正确
- 如果页面加载较慢，请耐心等待

### 3. 检测表格

**功能说明**：
- 检测页面中满足条件的表格元素
- 显示检测耗时
- 列出所有符合条件的表格

**表格格式**：
- 表格ID格式：`CPH_QGV_dxdt数字_QDGV_数字_DXMainTable`
- 两个数字必须保持一致
- 例如：`CPH_QGV_dxdt0_QDGV_0_DXMainTable`、`CPH_QGV_dxdt1_QDGV_1_DXMainTable`

**操作步骤**：
1. 先点击"连接网页"按钮连接到网页
2. 点击"检测表格"按钮
3. 查看检测结果和耗时

**输出示例**：
```
开始检测表格...
开始执行表格检测...
检测完成！
检测耗时: 0.21 秒
共找到 17 个满足条件的table元素
符合条件的table元素id:
  - CPH_QGV_dxdt0_QDGV_0_DXMainTable
  - CPH_QGV_dxdt1_QDGV_1_DXMainTable
  ...
```

### 4. 自动填表

**功能说明**：
- 读取Excel数据（已在导入时验证过）
- 按表格顺序处理数据
- 顺序填入数据
- 处理{{discount}}占位符
- 处理Brand字段特殊映射

**填表逻辑**：
- 使用单一的Excel行索引跨所有表格
- 按表格顺序（从0开始）处理数据
- 每个表格按行顺序填入数据
- 当一个表格填满后，自动切换到下一个表格

**值优先级**：
1. 默认值（default_value）
2. Excel值（excel_field）
3. Discount值（{{discount}}占位符）

**操作步骤**：
1. 确保Excel文件已验证通过
2. 确保已连接到网页
3. 点击"自动填表"按钮
4. 等待填表完成
5. 查看日志输出确认填表结果

### 5. 页面截图

**功能说明**：
- 保存当前页面截图
- 自动创建img目录
- 生成时间戳文件名
- 保存截图到img目录

**操作步骤**：
1. 确保已连接到网页
2. 点击"页面截图"按钮
3. 等待截图完成
4. 查看img目录下的截图文件

**文件命名**：
- 格式：`screenshot_YYYYMMDD_HHMMSS.png`
- 例如：`screenshot_20260216_123456.png`

---

## 配置说明

### 配置文件结构

配置文件使用JSON格式，包含以下主要部分：

```json
{
    "url": "网页URL",
    "excel_config": {
        "header_row": 16,
        "start_row": 17,
        "end_row": null,
        "discount": null,
        "oem_type": ["Compatible", "OEM", "Genuine"]
    },
    "field_mappings": [
        {
            "excel_field": "Excel字段名",
            "web_element": {
                "id": "元素ID"
            },
            "element_type": "input",
            "default_value": "默认值"
        }
    ]
}
```

### 配置参数详解

#### 1. url（网页URL）

**说明**：目标网页的URL地址

**示例**：
```json
"url": "https://example.com/form"
```

**优先级**：
- GUI界面的URL输入框 > 配置文件中的url

#### 2. excel_config（Excel配置）

**header_row（表头行）**
- **说明**：Excel文件中表头所在的行号
- **默认值**：16
- **示例**：
  ```json
  "header_row": 16
  ```

**start_row（数据开始行）**
- **说明**：Excel文件中数据开始的行号
- **默认值**：17
- **示例**：
  ```json
  "start_row": 17
  ```

**end_row（数据结束行）**
- **说明**：Excel文件中数据结束的行号
- **默认值**：null（自动计算）
- **自动计算规则**：从start_row开始，找到第一个第一列为空或非数字的行
- **示例**：
  ```json
  "end_row": null
  ```

**discount（折扣值）**
- **说明**：默认的折扣值
- **默认值**：null（从Excel中自动提取）
- **自动提取规则**：从表格末尾倒序查找，F列为"Discount  :"，H列为百分比值
- **示例**：
  ```json
  "discount": null
  ```

**oem_type（OEM类型列表）**
- **说明**：OEM类型的可选值列表
- **默认值**：["Compatible", "OEM", "Genuine"]
- **用途**：Brand字段映射到oem_type的索引
- **示例**：
  ```json
  "oem_type": ["Compatible", "OEM", "Genuine"]
  ```

#### 3. field_mappings（字段映射）

**excel_field（Excel字段名）**
- **说明**：Excel文件中的字段名
- **类型**：字符串或null
- **null表示**：使用默认值
- **示例**：
  ```json
  "excel_field": "No."
  ```

**web_element（网页元素标识符）**
- **说明**：网页元素的定位信息
- **支持的定位方式**：
  - `id`：元素ID
  - `class_name`：元素类名
  - `text`：元素文本内容
  - `xpath`：XPath表达式
  - `css_selector`：CSS选择器
  - `table_column`：表格列号（配合table_identifier使用）
- **示例**：
  ```json
  "web_element": {
      "id": "no"
  }
  ```

**element_type（元素类型）**
- **说明**：网页元素的类型
- **支持的类型**：
  - `input`：输入框
  - `select`：下拉选择框
  - `textarea`：文本域
- **示例**：
  ```json
  "element_type": "input"
  ```

**default_value（默认值）**
- **说明**：当excel_field为null或Excel中没有该值时使用的默认值
- **特殊值**：
  - `{{discount}}`：使用自动提取的Discount值
- **示例**：
  ```json
  "default_value": "{{discount}}"
  ```

### 配置文件示例

#### 示例1：简单表单

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
            "excel_field": "No.",
            "web_element": {
                "id": "no"
            },
            "element_type": "input"
        },
        {
            "excel_field": "IMPA",
            "web_element": {
                "id": "impa"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Description",
            "web_element": {
                "id": "description"
            },
            "element_type": "textarea"
        },
        {
            "excel_field": "Brand",
            "web_element": {
                "id": "brand"
            },
            "element_type": "select"
        }
    ]
}
```

#### 示例2：表格填入

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
            "excel_field": "No.",
            "web_element": {
                "table_column": 1,
                "table_identifier": "//table[@id='CPH_QGV_dxdt0_QDGV_0_DXMainTable']//tr[position()>=3]"
            },
            "element_type": "input"
        },
        {
            "excel_field": "IMPA",
            "web_element": {
                "table_column": 2,
                "table_identifier": "//table[@id='CPH_QGV_dxdt0_QDGV_0_DXMainTable']//tr[position()>=3]"
            },
            "element_type": "input"
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

---

## Excel文件格式

### 表头格式要求

**表头行**：第16行

**表头字段**（必须严格按照以下顺序和内容）：

| 列号 | 字段名 | 说明 |
|------|--------|------|
| 1 | No. | 序号 |
| 2 | IMPA | IMPA编码 |
| 3 | Description | 描述 |
| 4 | Remark | 备注 |
| 5 | Q'ty | 数量 |
| 6 | Unit | 单位 |
| 7 | Unit Price   (USD) | 单价（美元） |
| 8 | Amount   (USD) | 金额（美元） |
| 9 | Brand | 品牌 |

### 数据行格式

**数据开始行**：第17行

**数据格式**：
- 第1列（No.）：必须是数字，从1开始
- 其他列：根据实际情况填写

**数据结束行**：
- 如果配置文件中指定了`end_row`，则使用指定的行号
- 如果`end_row`为null，则自动计算：
  - 从第17行开始检查
  - 当某一行的第一列为空或不是数字时，上一行就是结束行

### Discount值格式

**位置**：表格的最后一部分

**格式**：
- F列：值为"Discount  :"
- H列：值为百分比的数字，例如"6.0%"或0.06

**自动提取规则**：
- 从表格的最后一行开始往上查找
- 查找F列值为"Discount  :"的行
- 提取该行H列的值
- 如果是字符串（如"16%"），提取数字部分
- 如果是小数（如0.16），乘以100转换为整数

### 示例Excel文件

```
第16行：No. | IMPA | Description | Remark | Q'ty | Unit | Unit Price   (USD) | Amount   (USD) | Brand
第17行：1   | 123  | Test Item   | Test  | 10   | PCS  | 100.00          | 1000.00        | OEM
第18行：2   | 456  | Test Item 2 | Test2 | 20   | PCS  | 200.00          | 4000.00        | Compatible
...
第100行：    |      |             |       |      |      |                 |                |
第101行：    |      |             |       |      |      |                 |                |
第102行：    |      |             |       |      | Discount  :     |                | 16%
```

---

## 使用步骤

### 完整使用流程

#### 第一步：准备工作

1. **准备Excel文件**
   - 确保Excel文件格式符合要求
   - 第16行必须是表头行
   - 表头字段必须严格按照指定格式

2. **准备配置文件**
   - 在`cfg`目录下创建`default.json`文件
   - 根据实际需求配置参数

3. **准备网页**
   - 确保网页可以正常访问
   - 了解网页的元素定位方式

#### 第二步：启动程序

1. **启动程序**
   - 双击`excel_web_filler.exe`或运行`python gui.py`
   - 等待程序界面加载完成

2. **查看日志**
   - 确认日志文件已创建
   - 查看程序启动日志

#### 第三步：选择Excel文件

1. **选择文件**
   - 点击"浏览"按钮
   - 选择Excel文件

2. **查看验证结果**
   - 系统会自动验证Excel文件格式
   - 查看验证结果：
     - 验证成功：显示读取的数据行数和Discount值
     - 验证失败：显示详细的错误信息

3. **处理验证失败**
   - 检查Excel文件格式
   - 修改Excel文件
   - 重新选择文件

#### 第四步：配置参数

1. **配置URL**
   - 在"URL地址"输入框中输入网页地址（可选）
   - 或在配置文件中设置url参数

2. **配置文件**
   - 点击"配置"按钮
   - 选择或修改配置文件
   - 查看配置内容
   - 点击"加载配置"按钮

3. **查看配置**
   - 确认配置参数正确
   - 确认字段映射正确

#### 第五步：连接网页

1. **连接网页**
   - 点击"连接网页"按钮
   - 等待浏览器启动
   - 等待页面加载

2. **查看日志**
   - 查看浏览器启动日志
   - 确认连接成功

3. **处理连接失败**
   - 检查网络连接
   - 检查URL地址
   - 检查浏览器是否已安装

#### 第六步：检测表格（可选）

1. **检测表格**
   - 点击"检测表格"按钮
   - 等待检测完成

2. **查看检测结果**
   - 查看检测耗时
   - 查看找到的表格列表
   - 确认表格格式正确

3. **处理检测失败**
   - 检查页面是否完全加载
   - 检查表格ID格式
   - 检查配置文件中的table_identifier

#### 第七步：自动填表

1. **开始填表**
   - 点击"自动填表"按钮
   - 等待填表完成

2. **查看日志**
   - 查看填表进度
   - 查看填表结果
   - 查看错误信息（如果有）

3. **处理填表失败**
   - 查看错误信息
   - 检查配置文件
   - 检查Excel数据
   - 检查网页元素

#### 第八步：截图（可选）

1. **截图**
   - 点击"页面截图"按钮
   - 等待截图完成

2. **查看截图**
   - 打开`img`目录
   - 查看截图文件

3. **处理截图失败**
   - 检查`img`目录权限
   - 检查磁盘空间
   - 检查网页是否正常显示

#### 第九步：完成

1. **确认结果**
   - 查看网页中的填表结果
   - 查看日志文件
   - 确认所有数据已正确填入

2. **保存结果**
   - 保存网页截图
   - 保存日志文件
   - 记录填表结果

3. **关闭程序**
   - 关闭浏览器
   - 关闭程序

### 命令行使用

#### 基本用法

```bash
python main.py <excel_file> <config_file> [--url <url>]
```

#### 参数说明

- `excel_file`：Excel文件路径（必需）
- `config_file`：配置文件路径（必需）
- `--url`：网页URL（可选，优先级高于配置文件）

#### 示例

```bash
python main.py data.xlsx config.json
```

```bash
python main.py data.xlsx config.json --url https://example.com/form
```

---

## 常见问题

### Q1：Excel文件格式验证失败怎么办？

**A**：
1. 检查第16行的表头是否正确
2. 确保表头字段名称和顺序完全匹配
3. 查看详细的错误信息，定位具体哪一列不匹配
4. 修改Excel文件后重新选择

### Q2：无法连接到网页怎么办？

**A**：
1. 检查网络连接是否正常
2. 检查URL地址是否正确
3. 检查Chrome浏览器是否已安装
4. 检查Playwright浏览器驱动是否已安装
5. 查看日志文件了解详细错误信息

### Q3：元素未找到怎么办？

**A**：
1. 检查配置文件中的元素标识符是否正确
2. 确保网页已完全加载
3. 使用浏览器开发者工具检查元素
4. 尝试不同的元素定位方式
5. 查看日志文件了解详细错误信息

### Q4：数据填入失败怎么办？

**A**：
1. 检查Excel文件中的字段名是否与配置文件一致
2. 检查网页元素是否可编辑
3. 检查元素类型是否正确（input、select、textarea）
4. 查看日志文件了解详细错误信息

### Q5：表格检测失败怎么办？

**A**：
1. 检查页面是否完全加载
2. 检查表格ID格式是否正确
3. 检查配置文件中的table_identifier
4. 使用"检测表格"功能查看找到的表格
5. 查看日志文件了解详细错误信息

### Q6：Discount值提取失败怎么办？

**A**：
1. 检查Excel文件中是否有Discount行
2. 检查F列是否为"Discount  :"
3. 检查H列是否为百分比值
4. 在配置文件中手动设置discount值
5. 查看日志文件了解详细错误信息

### Q7：截图失败怎么办？

**A**：
1. 检查可执行文件所在目录是否有写权限
2. 手动创建`img`目录
3. 检查磁盘空间是否充足
4. 检查网页是否正常显示
5. 查看日志文件了解详细错误信息

### Q8：配置文件未找到怎么办？

**A**：
1. 检查`cfg`目录是否存在
2. 检查`default.json`文件是否存在
3. 检查配置文件路径是否正确
4. 使用"配置"按钮选择配置文件
5. 查看日志文件了解详细错误信息

### Q9：程序启动失败怎么办？

**A**：
1. 检查Python版本是否符合要求（3.7+）
2. 检查依赖包是否已安装
3. 检查可执行文件是否损坏
4. 查看日志文件了解详细错误信息
5. 尝试重新安装或重新打包

### Q10：填表速度慢怎么办？

**A**：
1. 检查网络连接速度
2. 检查网页加载速度
3. 减少Excel数据行数
4. 优化配置文件中的元素定位
5. 使用"检测表格"功能优化表格查找

---

## 故障排除

### 问题1：Excel文件格式验证失败

**症状**：
```
Excel文件格式验证失败: 表头第 1 列不匹配，预期: 'No.'，实际: 'No1.'
```

**原因**：
- Excel文件第16行的表头格式不正确
- 表头字段名称或顺序不匹配

**解决方案**：
1. 打开Excel文件
2. 定位到第16行
3. 检查表头字段是否正确：
   - 第1列：No.
   - 第2列：IMPA
   - 第3列：Description
   - 第4列：Remark
   - 第5列：Q'ty
   - 第6列：Unit
   - 第7列：Unit Price   (USD)
   - 第8列：Amount   (USD)
   - 第9列：Brand
4. 修改不正确的字段
5. 保存文件
6. 重新选择Excel文件

### 问题2：无法连接到网页

**症状**：
```
连接到网页时出错: TimeoutError: Navigation timeout of 30000 ms exceeded
```

**原因**：
- 网络连接问题
- URL地址错误
- 网页加载缓慢
- 浏览器未安装

**解决方案**：
1. 检查网络连接
2. 验证URL地址是否正确
3. 检查Chrome浏览器是否已安装
4. 检查Playwright浏览器驱动是否已安装：
   ```bash
   playwright install
   ```
5. 增加页面加载超时时间（修改代码）
6. 查看日志文件了解详细错误信息

### 问题3：元素未找到

**症状**：
```
填入数据时出错: TimeoutError: Locator.click: Timeout 30000ms exceeded
```

**原因**：
- 元素标识符不正确
- 网页未完全加载
- 元素不存在

**解决方案**：
1. 使用浏览器开发者工具检查元素
2. 验证元素标识符是否正确
3. 确保网页已完全加载
4. 尝试不同的元素定位方式：
   - ID
   - Class name
   - XPath
   - CSS选择器
5. 增加元素查找超时时间（修改代码）
6. 查看日志文件了解详细错误信息

### 问题4：数据填入失败

**症状**：
```
填入数据时出错: Error: Element is not visible
```

**原因**：
- 元素不可见
- 元素被遮挡
- 元素类型不正确

**解决方案**：
1. 检查元素是否可见
2. 检查元素类型是否正确
3. 滚动页面使元素可见
4. 检查元素是否被其他元素遮挡
5. 查看日志文件了解详细错误信息

### 问题5：表格检测失败

**症状**：
```
检测完成！
检测耗时: 0.21 秒
共找到 0 个满足条件的table元素
```

**原因**：
- 页面未完全加载
- 表格ID格式不正确
- 配置文件中的table_identifier不正确

**解决方案**：
1. 确保页面已完全加载
2. 使用"检测表格"功能查看找到的表格
3. 检查表格ID格式：
   - 格式：`CPH_QGV_dxdt数字_QDGV_数字_DXMainTable`
   - 两个数字必须保持一致
4. 检查配置文件中的table_identifier
5. 使用浏览器开发者工具检查表格元素
6. 查看日志文件了解详细错误信息

### 问题6：Discount值提取失败

**症状**：
```
找到Discount值: 0
```

**原因**：
- Excel文件中没有Discount行
- F列或H列格式不正确
- Discount值格式不正确

**解决方案**：
1. 检查Excel文件中是否有Discount行
2. 检查F列是否为"Discount  :"
3. 检查H列是否为百分比值：
   - 字符串格式：如"16%"
   - 数字格式：如0.16
4. 在配置文件中手动设置discount值：
   ```json
   "discount": 16
   ```
5. 查看日志文件了解详细错误信息

### 问题7：截图失败

**症状**：
```
截图时出错: PermissionError: [Errno 13] Permission denied: 'img'
```

**原因**：
- img目录没有写权限
- 磁盘空间不足
- img目录不存在

**解决方案**：
1. 检查img目录是否存在
2. 手动创建img目录
3. 检查img目录的写权限
4. 检查磁盘空间是否充足
5. 更改截图保存路径
6. 查看日志文件了解详细错误信息

### 问题8：配置文件未找到

**症状**：
```
错误: 未找到配置文件
```

**原因**：
- cfg目录不存在
- default.json文件不存在
- 配置文件路径不正确

**解决方案**：
1. 检查cfg目录是否存在
2. 检查default.json文件是否存在
3. 检查配置文件路径是否正确
4. 使用"配置"按钮选择配置文件
5. 手动创建cfg目录和default.json文件
6. 查看日志文件了解详细错误信息

### 问题9：程序启动失败

**症状**：
```
程序启动时出错: ModuleNotFoundError: No module named 'playwright'
```

**原因**：
- 依赖包未安装
- Python版本不符合要求
- 虚拟环境未激活

**解决方案**：
1. 检查Python版本（需要3.7+）
2. 激活虚拟环境：
   ```bash
   .venv\Scripts\activate
   ```
3. 安装依赖包：
   ```bash
   pip install playwright openpyxl
   ```
4. 安装Playwright浏览器：
   ```bash
   playwright install
   ```
5. 查看日志文件了解详细错误信息

### 问题10：填表速度慢

**症状**：
- 填表过程耗时过长
- 程序响应缓慢

**原因**：
- 网络连接速度慢
- 网页加载速度慢
- Excel数据行数过多
- 元素定位效率低

**解决方案**：
1. 检查网络连接速度
2. 检查网页加载速度
3. 减少Excel数据行数
4. 优化配置文件中的元素定位：
   - 使用更精确的定位方式
   - 避免使用通用的class name
   - 使用ID或XPath定位
5. 使用"检测表格"功能优化表格查找
6. 查看日志文件了解详细错误信息

---

## 附录

### A. 日志文件说明

**日志文件位置**：
- 可执行文件所在目录的`logs`子目录

**日志文件命名**：
- 格式：`excel_web_filler_YYYYMMDD_HHMMSS.log`
- 例如：`excel_web_filler_20260216_123456.log`

**日志文件内容**：
- 程序启动信息
- Excel文件验证结果
- 网页连接信息
- 表格检测结果
- 填表过程记录
- 错误信息

**日志文件示例**：
```
=== Excel Web Filler 日志文件 ===
创建时间: 2026-02-16 12:34:56
日志文件: D:\excel_web_filler\logs\excel_web_filler_20260216_123456.log
=================================

正在验证Excel文件格式: D:\test.xlsx
Excel表头验证通过！
✓ Excel文件格式验证通过
✓ 共读取 6 行数据
✓ 找到Discount值: 16

开始连接到网页...
使用URL: https://example.com/form
网页连接成功
现在可以点击'自动填表'按钮开始填表

开始执行填表任务...
读取Excel数据...
Excel数据读取成功，共 6 行
找到 17 个满足条件的表格

处理表格 1/17: CPH_QGV_dxdt0_QDGV_0_DXMainTable
填入第1行数据到表格1
填入第2行数据到表格1
...

填表完成！
```

### B. 截图文件说明

**截图文件位置**：
- 可执行文件所在目录的`img`子目录

**截图文件命名**：
- 格式：`screenshot_YYYYMMDD_HHMMSS.png`
- 例如：`screenshot_20260216_123456.png`

**截图文件格式**：
- PNG格式
- 全页面截图

### C. 配置文件模板

**默认配置文件模板**（`cfg/default.json`）：
```json
{
    "url": "",
    "excel_config": {
        "header_row": 16,
        "start_row": 17,
        "end_row": null,
        "discount": null,
        "oem_type": ["Compatible", "OEM", "Genuine"]
    },
    "field_mappings": []
}
```

**完整配置文件模板**：
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
            "excel_field": "No.",
            "web_element": {
                "id": "no"
            },
            "element_type": "input"
        },
        {
            "excel_field": "IMPA",
            "web_element": {
                "id": "impa"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Description",
            "web_element": {
                "id": "description"
            },
            "element_type": "textarea"
        },
        {
            "excel_field": "Remark",
            "web_element": {
                "id": "remark"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Q'ty",
            "web_element": {
                "id": "qty"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Unit",
            "web_element": {
                "id": "unit"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Unit Price   (USD)",
            "web_element": {
                "id": "price"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Amount   (USD)",
            "web_element": {
                "id": "amount"
            },
            "element_type": "input"
        },
        {
            "excel_field": "Brand",
            "web_element": {
                "id": "brand"
            },
            "element_type": "select"
        }
    ]
}
```

### D. Excel文件模板

**Excel文件结构**：

| 行号 | 列1 | 列2 | 列3 | 列4 | 列5 | 列6 | 列7 | 列8 | 列9 |
|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 16 | No. | IMPA | Description | Remark | Q'ty | Unit | Unit Price   (USD) | Amount   (USD) | Brand |
| 17 | 1 | 123 | Test Item | Test | 10 | PCS | 100.00 | 1000.00 | OEM |
| 18 | 2 | 456 | Test Item 2 | Test2 | 20 | PCS | 200.00 | 4000.00 | Compatible |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 100 | | | | | | | | | |
| 101 | | | | | | | | | |
| 102 | | | | | | Discount  : | | | 16% |

### E. 元素定位方式

#### 1. ID定位

**说明**：通过元素的ID属性定位

**示例**：
```json
{
    "web_element": {
        "id": "no"
    }
}
```

#### 2. Class name定位

**说明**：通过元素的class属性定位

**示例**：
```json
{
    "web_element": {
        "class_name": "input-field"
    }
}
```

#### 3. Text定位

**说明**：通过元素的文本内容定位

**示例**：
```json
{
    "web_element": {
        "text": "提交"
    }
}
```

#### 4. XPath定位

**说明**：通过XPath表达式定位

**示例**：
```json
{
    "web_element": {
        "xpath": "//input[@id='no']"
    }
}
```

#### 5. CSS选择器定位

**说明**：通过CSS选择器定位

**示例**：
```json
{
    "web_element": {
        "css_selector": "#no"
    }
}
```

#### 6. 表格列定位

**说明**：通过表格列号和表格标识符定位

**示例**：
```json
{
    "web_element": {
        "table_column": 1,
        "table_identifier": "//table[@id='CPH_QGV_dxdt0_QDGV_0_DXMainTable']//tr[position()>=3]"
    }
}
```

### F. 命令行参数

**基本用法**：
```bash
python main.py <excel_file> <config_file> [--url <url>]
```

**参数说明**：
- `excel_file`：Excel文件路径（必需）
- `config_file`：配置文件路径（必需）
- `--url`：网页URL（可选，优先级高于配置文件）

**示例**：
```bash
python main.py data.xlsx config.json
```

```bash
python main.py data.xlsx config.json --url https://example.com/form
```

### G. 技术支持

**联系方式**：
- 项目地址：[GitHub项目地址]
- 问题反馈：[Issues页面]
- 邮箱：[技术支持邮箱]

**常见问题**：
- 参见[常见问题](#常见问题)部分
- 参见[故障排除](#故障排除)部分

**版本信息**：
- 当前版本：1.0.0
- 更新日期：2026-02-16

---

**文档版本**：1.0.0  
**最后更新**：2026-02-16  
**作者**：Excel Web Filler Team
