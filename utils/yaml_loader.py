import yaml
import os
from pathlib import Path

class YamlLoader:
    """YAML配置加载器 - 单例模式"""
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self, filename="config.yaml"):
        """加载YAML配置"""
        if self._config is None:
            config_path = Path(__file__).parent.parent / "config" / filename
            print(f"Loading config from: {config_path}")
            if not config_path.exists():
                print(f"Config file not found: {config_path}")
                raise FileNotFoundError(f"Config file not found: {config_path}")
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
            print(f"Config loaded successfully: {self._config}")
        return self._config
    
    def get(self, key_path: str, default=None):
        """
        通过点号路径获取配置值
        例如: get("app.timeout") -> 10
        """
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value

# 全局配置实例
config = YamlLoader()
