import allure
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.timings import TimeoutError as PwaTimeoutError
from utils.driver_factory import DriverFactory
from utils.yaml_loader import config

class BasePage:
    """所有页面对象的基类"""
    
    def __init__(self):
        self.driver = DriverFactory
        self.window = None
        self.timeout = config.get("waits.explicit_wait", 10)
    
    def _get_window(self):
        """延迟加载窗口"""
        if self.window is None:
            self.window = self.driver.get_window()
        return self.window
    
    def find_element(self, **kwargs):
        """
        查找单个元素
        支持: control_type, class_name, name, automation_id, title
        """
        window = self._get_window()
        try:
            # 检查window类型，使用不同的方法查找元素
            if hasattr(window, 'child_window'):
                # WindowSpecification对象
                # 处理automation_id参数
                if 'automation_id' in kwargs:
                    kwargs['auto_id'] = kwargs.pop('automation_id')
                element = window.child_window(**kwargs, found_index=0)
                element.wait('visible', timeout=self.timeout)
                return element
            else:
                # UIAWrapper对象
                from pywinauto import Desktop
                # 使用Desktop对象重新查找元素
                desktop = Desktop(backend="uia")
                # 为当前窗口创建一个WindowSpecification
                window_spec = desktop.window(handle=window.handle)
                # 处理automation_id参数
                if 'automation_id' in kwargs:
                    kwargs['auto_id'] = kwargs.pop('automation_id')
                element = window_spec.child_window(**kwargs, found_index=0)
                element.wait('visible', timeout=self.timeout)
                return element
        except PwaTimeoutError:
            raise Exception(f"元素未找到: {kwargs}")
    
    def find_elements(self, **kwargs):
        """查找多个元素"""
        window = self._get_window()
        if hasattr(window, 'children'):
            return window.children(**kwargs)
        else:
            # UIAWrapper对象
            from pywinauto import Desktop
            desktop = Desktop(backend="uia")
            window_spec = desktop.window(handle=window.handle)
            return window_spec.children(**kwargs)
    
    @allure.step("点击元素: {name}")
    def click(self, element, name="未知"):
        """安全点击元素"""
        element.click_input()
        return self
    
    @allure.step("输入文本: {text}")
    def input_text(self, element, text: str, clear_first=True):
        """输入文本"""
        if clear_first:
            element.type_keys("^a")  # Ctrl+A 全选
        element.type_keys(text, with_spaces=True)
        return self
    
    @allure.step("获取元素文本")
    def get_text(self, element) -> str:
        """获取元素文本"""
        return element.window_text()
    
    def wait_for_element(self, **kwargs):
        """显式等待元素出现"""
        window = self._get_window()
        if hasattr(window, 'child_window'):
            element = window.child_window(**kwargs)
            element.wait('visible', timeout=self.timeout)
            return element
        else:
            # UIAWrapper对象
            from pywinauto import Desktop
            desktop = Desktop(backend="uia")
            window_spec = desktop.window(handle=window.handle)
            element = window_spec.child_window(**kwargs)
            element.wait('visible', timeout=self.timeout)
            return element
    
    @allure.step("截图: {name}")
    def screenshot(self, name="page_state"):
        """页面截图"""
        self.driver.take_screenshot(name)
        return self
