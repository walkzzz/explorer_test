import pytest
import allure
from utils.driver_factory import DriverFactory
from pages.explorer_page import ExplorerPage

@pytest.fixture(scope="session")
def driver():
    """全局驱动fixture"""
    DriverFactory.get_app()
    yield DriverFactory
    DriverFactory.close_app()

@pytest.fixture(scope="function")
def explorer(driver):
    """资源管理器页面fixture - 每个测试用例独立"""
    page = ExplorerPage()
    page.open()
    yield page
    # 测试结束后回到安全状态
    try:
        page.navigate_to("此电脑")
    except:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试失败自动截图"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            DriverFactory.take_screenshot(f"failed_{item.name}")
        except:
            pass

def pytest_configure(config):
    """配置allure环境信息"""
    config._metadata = {
        "测试框架": "pytest+allure+pywinauto",
        "测试对象": "Windows资源管理器",
        "后端": "UI Automation"
    }
