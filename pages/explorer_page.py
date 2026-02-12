import allure
from .base_page import BasePage
from utils.yaml_loader import config


class ExplorerPage(BasePage):
    """Windows资源管理器页面对象"""

    # 页面标识
    WINDOW_TITLE_RE = ".*资源管理器|.*Explorer"

    def __init__(self):
        super().__init__()
        # 确保config已加载
        config.load()
        self.selectors = config.get("selectors", {})

    # ==================== 元素定位 ====================

    def _get_selector(self, key):
        """从YAML获取选择器配置"""
        if self.selectors is None:
            return {}
        return self.selectors.get(key, {})

    @property
    def address_bar(self):
        """地址栏"""
        return self.find_element(**self._get_selector("address_bar"))

    @property
    def navigation_pane(self):
        """导航面板"""
        return self.find_element(**self._get_selector("navigation_pane"))

    @property
    def file_list(self):
        """文件列表区域"""
        return self.find_element(**self._get_selector("file_list"))

    @property
    def search_box(self):
        """搜索框"""
        return self.find_element(**self._get_selector("search_box"))

    # ==================== 页面操作 ====================

    @allure.step("打开资源管理器")
    def open(self):
        """打开资源管理器"""
        self.window = self.driver.get_window(title_re=self.WINDOW_TITLE_RE)
        self.screenshot("explorer_opened")
        return self

    @allure.step("导航到路径: {path}")
    def navigate_to(self, path: str):
        """通过地址栏导航"""
        # 点击地址栏
        addr_bar = self.address_bar
        self.click(addr_bar, "地址栏")

        # 输入路径并回车
        self.input_text(addr_bar, path)
        addr_bar.type_keys("{ENTER}")

        # 等待加载
        import time

        time.sleep(0.5)

        self.screenshot(f"navigated_to_{path.replace('/', '_')}")
        return self

    @allure.step("点击导航项: {item_name}")
    def click_navigation_item(self, item_name: str):
        """点击左侧导航项"""
        nav_pane = self.navigation_pane
        item = nav_pane.child_window(title=item_name, control_type="TreeItem")
        self.click(item, item_name)
        return self

    @allure.step("搜索文件: {keyword}")
    def search(self, keyword: str):
        """执行搜索"""
        search = self.search_box
        self.click(search, "搜索框")
        self.input_text(search, keyword)
        search.type_keys("{ENTER}")
        return self

    @allure.step("获取当前路径")
    def get_current_path(self) -> str:
        """获取当前地址栏路径"""
        return self.get_text(self.address_bar)

    @allure.step("获取文件列表")
    def get_file_items(self) -> list:
        """获取当前目录下的文件/文件夹列表"""
        file_list = self.file_list
        items = file_list.children(control_type="ListItem")
        return [item.window_text() for item in items]

    @allure.step("新建文件夹: {name}")
    def create_folder(self, name: str):
        """新建文件夹"""
        # 右键点击空白处
        self.file_list.click_input(button="right")

        # 查找"新建"菜单
        desktop = self.driver.get_app().window(title="上下文菜单")
        new_menu = desktop.child_window(title="新建(N)", control_type="MenuItem")
        self.click(new_menu, "新建菜单")

        # 点击"文件夹"
        folder_item = desktop.child_window(title="文件夹(F)", control_type="MenuItem")
        self.click(folder_item, "文件夹选项")

        # 输入名称
        import time

        time.sleep(0.3)
        self.file_list.type_keys(name + "{ENTER}")

        return self
