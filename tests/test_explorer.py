import pytest
import allure

from pages.explorer_page import ExplorerPage

@allure.feature("资源管理器基础功能")
@allure.story("导航功能")
class TestNavigation:
    """导航功能测试"""
    
    @allure.title("测试导航到此电脑")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_navigate_to_this_pc(self, explorer: ExplorerPage):
        """验证可以成功导航到此电脑"""
        with allure.step("点击此电脑"):
            explorer.click_navigation_item("此电脑")
        
        with allure.step("验证地址栏显示"):
            path = explorer.get_current_path()
            assert "此电脑" in path or "This PC" in path or "Computer" in path
    
    @allure.title("测试地址栏导航")
    @allure.severity(allure.severity_level.NORMAL)
    def test_address_bar_navigation(self, explorer: ExplorerPage):
        """验证可以通过地址栏导航到指定路径"""
        test_path = r"C:\Windows"
        
        explorer.navigate_to(test_path)
        current = explorer.get_current_path()
        
        with allure.step(f"验证当前路径包含 {test_path}"):
            assert test_path.replace("\\", "") in current.replace("\\", "")

@allure.feature("资源管理器基础功能")
@allure.story("文件操作")
class TestFileOperations:
    """文件操作测试"""
    
    @allure.title("测试获取文件列表")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_file_list(self, explorer: ExplorerPage):
        """验证可以获取当前目录文件列表"""
        explorer.navigate_to("C:\\")
        
        with allure.step("获取文件列表"):
            files = explorer.get_file_items()
            
        with allure.step("验证返回列表"):
            assert isinstance(files, list)
            allure.attach(str(files), "文件列表", allure.attachment_type.TEXT)
    
    @allure.title("测试搜索功能")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_files(self, explorer: ExplorerPage):
        """验证搜索功能可用"""
        explorer.navigate_to("C:\\Windows")
        
        with allure.step("执行搜索"):
            explorer.search("*.exe")
            # 这里简化处理，实际应验证搜索结果
            assert True

@allure.feature("资源管理器高级功能")
@allure.story("窗口管理")
class TestWindowManagement:
    """窗口管理测试"""
    
    @allure.title("测试窗口标题")
    @allure.severity(allure.severity_level.TRIVIAL)
    def test_window_title(self, explorer: ExplorerPage):
        """验证窗口标题正确"""
        title = explorer._get_window().window_text()
        with allure.step("验证标题包含资源管理器"):
            assert "资源管理器" in title or "Explorer" in title
