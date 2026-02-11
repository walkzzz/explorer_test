# Windows应用自动化测试框架

## 项目简介

本框架基于Python + pytest + allure + pywinauto + yaml，用于Windows应用的自动化测试。采用Page Object模式设计，支持Windows GUI元素的定位、操作和验证。

## 技术栈

- Python 3.12+
- pytest 7.0+
- allure-pytest 2.13+
- pywinauto 0.6.8+
- PyYAML 6.0+
- Pillow (用于截图)

## 目录结构

```
explorer_test/
├── config/               # 配置文件目录
│   └── config.yaml       # 框架配置文件
├── utils/                # 工具类目录
│   ├── yaml_loader.py    # YAML配置加载器
│   └── driver_factory.py # Windows应用驱动工厂
├── pages/                # 页面对象目录
│   ├── base_page.py      # 页面对象基类
│   └── explorer_page.py  # 资源管理器页面对象
├── tests/                # 测试用例目录
│   └── test_explorer.py  # 资源管理器测试用例
├── conftest.py           # pytest配置和fixture
├── pytest.ini            # pytest配置文件
├── requirements.txt      # 依赖项文件
├── allure-results/       # Allure报告结果目录
└── allure-report/        # Allure报告生成目录
```

## 安装步骤

1. **创建虚拟环境**
   ```bash
   python -m venv .venv
   ```

2. **激活虚拟环境**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

3. **安装依赖项**
   ```bash
   pip install -r requirements.txt
   ```

4. **安装Allure命令行工具**
   参考：https://docs.qameta.io/allure/#_installing_a_commandline

## 运行测试

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_explorer.py -v
```

### 运行特定测试类

```bash
pytest tests/test_explorer.py::TestNavigation -v
```

### 运行特定测试方法

```bash
pytest tests/test_explorer.py::TestNavigation::test_navigate_to_this_pc -v
```

## 生成Allure报告

1. **运行测试生成结果**
   ```bash
   pytest --alluredir=allure-results
   ```

2. **生成报告**
   ```bash
   allure generate allure-results -o allure-report --clean
   ```

3. **打开报告**
   ```bash
   allure open allure-report
   ```

## 配置说明

配置文件位于 `config/config.yaml`，包含以下部分：

- **app**: 应用程序配置（路径、超时等）
- **selectors**: UI元素选择器配置
- **waits**: 等待时间配置

## 框架特性

1. **Page Object模式**：将页面元素和操作封装在页面对象中，提高代码可维护性
2. **配置驱动**：使用YAML配置文件管理元素定位器和测试配置
3. **智能等待**：内置显式等待机制，提高测试稳定性
4. **截图功能**：测试失败时自动截图，便于问题定位
5. **Allure报告**：生成美观、详细的测试报告
6. **多元素定位**：支持多种元素定位方式（control_type、class_name、name、auto_id等）
7. **异常处理**：完善的异常处理机制，提高测试可靠性

## 扩展指南

### 添加新的页面对象

1. 在 `pages/` 目录下创建新的页面对象文件
2. 继承 `BasePage` 类
3. 实现页面元素和操作方法

### 添加新的测试用例

1. 在 `tests/` 目录下创建新的测试文件
2. 使用 pytest 测试类和方法命名规范
3. 使用 `@allure.step` 装饰器添加测试步骤

### 自定义配置

1. 修改 `config/config.yaml` 文件中的配置项
2. 在代码中通过 `config.get()` 方法获取配置值

## 示例测试

框架包含以下示例测试：

- **导航测试**：测试资源管理器导航功能
- **文件操作测试**：测试文件列表获取和搜索功能
- **窗口管理测试**：测试窗口标题获取功能

## 注意事项

1. **运行环境**：需要在Windows操作系统上运行
2. **权限要求**：某些操作可能需要管理员权限
3. **稳定性**：Windows GUI自动化测试受系统环境影响较大，建议在稳定的测试环境中运行
4. **性能**：GUI操作相对较慢，测试执行时间可能较长

## 故障排查

### 常见问题及解决方案

1. **元素未找到**：检查元素定位器配置是否正确，增加等待时间
2. **窗口未找到**：检查窗口标题是否正确，确保应用已启动
3. **截图失败**：确保Pillow库已安装，检查临时目录权限
4. **测试超时**：增加配置文件中的超时时间，检查系统性能

## 贡献

欢迎提交问题和代码改进建议！

## 许可证

MIT License
