import allure
from pywinauto import Application, Desktop
from pywinauto.timings import Timings
from .yaml_loader import config

class DriverFactory:
    """Windows应用驱动工厂"""
    
    _app = None
    _window = None
    
    @classmethod
    def get_app(cls, force_new=False):
        """获取或创建应用实例"""
        if cls._app is None or force_new:
            # 确保配置已加载
            config.load()
            app_path = config.get("app.path")
            timeout = config.get("app.timeout", 10)
            
            print(f"App path: {app_path}")
            print(f"Timeout: {timeout}")
            
            if not app_path:
                raise ValueError("App path not found in config")
            
            with allure.step(f"启动应用: {app_path}"):
                # 强制启动一个新的资源管理器实例，打开C盘
                print("Starting new instance of Explorer with path C:")
                try:
                    # 使用 explorer.exe 命令启动资源管理器并打开C盘
                    cls._app = Application(backend="uia").start("explorer.exe C:")
                    print("Started new instance with explorer.exe C:")
                except Exception as e:
                    print(f"Failed to start explorer: {e}")
                    # 尝试直接启动
                    cls._app = Application(backend="uia").start(app_path)
                    print("Started new instance with direct path")
                
                # 设置全局超时
                Timings.window_find_timeout = timeout
                Timings.window_find_retry = 0.5
                
                # 等待几秒钟让应用完全启动
                import time
                time.sleep(3)  # 增加等待时间
                
        return cls._app
    
    @classmethod
    def get_window(cls, title_re=".*", class_name=None):
        """获取应用主窗口"""
        app = cls.get_app()
        
        print(f"Getting window with title_re: {title_re}, class_name: {class_name}")
        
        # 尝试获取所有窗口
        try:
            windows = app.windows()
            print(f"Found windows: {[w.window_text() for w in windows]}")
        except Exception as e:
            print(f"Error getting windows: {e}")
        
        # 尝试使用不同的方法查找窗口
        try:
            # 方法1: 使用应用对象查找
            if class_name:
                cls._window = app.window(class_name=class_name)
            else:
                cls._window = app.window(title_re=title_re)
            
            print(f"Window found: {cls._window}")
            
            # 等待窗口就绪并置顶
            timeout = config.get("waits.explicit_wait", 10)
            print(f"Waiting for window to be visible with timeout: {timeout}")
            cls._window.wait('visible', timeout=timeout)
            print("Window is visible")
        except Exception as e:
            print(f"Error waiting for window: {e}")
            
            # 方法2: 使用Desktop对象查找所有窗口
            try:
                from pywinauto import Desktop
                desktop = Desktop(backend="uia")
                all_windows = desktop.windows()
                print(f"All windows on desktop: {[w.window_text() for w in all_windows]}")
                
                # 筛选出可能的资源管理器窗口
                explorer_windows = []
                for w in all_windows:
                    text = w.window_text()
                    print(f"Checking window: '{text}'")
                    if text and ("资源管理器" in text or "Explorer" in text or "文件资源管理器" in text):
                        explorer_windows.append(w)
                    elif text == "C:":
                        explorer_windows.append(w)
                
                if explorer_windows:
                    cls._window = explorer_windows[0]
                    print(f"Found explorer window: {cls._window.window_text()}")
                    # 对于Desktop返回的窗口对象，使用time.sleep替代wait方法
                    import time
                    time.sleep(2)
                else:
                    # 尝试获取最前面的窗口
                    cls._window = desktop.window(active_only=True)
                    print(f"Using active window: {cls._window.window_text()}")
                    import time
                    time.sleep(2)
            except Exception as e2:
                print(f"Error getting window from Desktop: {e2}")
                raise
        
        cls._window.set_focus()
        print("Window focused")
        
        return cls._window
    
    @classmethod
    def close_app(cls):
        """关闭应用"""
        if cls._app:
            with allure.step("关闭应用"):
                try:
                    cls._app.kill()
                except:
                    pass
            cls._app = None
            cls._window = None

    @classmethod
    def take_screenshot(cls, name="screenshot"):
        """截取当前窗口截图"""
        if cls._window:
            import os
            # 使用Windows临时目录
            screenshot_path = os.path.join(os.getenv('TEMP'), f"{name}.png")
            cls._window.capture_as_image().save(screenshot_path)
            allure.attach.file(screenshot_path, name=name, attachment_type=allure.attachment_type.PNG)
