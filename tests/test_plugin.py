import unittest
from mkdocs_bi_directional_links.plugin import BiDirectionalLinksPlugin

class TestPlugin(unittest.TestCase):
    def test_plugin_initialization(self):
        """
        测试插件初始化。
        """
        plugin = BiDirectionalLinksPlugin()
        self.assertFalse(plugin.debug)  # 确保调试模式默认关闭

    def test_on_config(self):
        """
        测试插件配置加载。
        """
        plugin = BiDirectionalLinksPlugin()
        config = {"docs_dir": "docs", "plugins": {"mkdocs_bi_directional_links": {"debug": True}}}
        plugin.on_config(config)
        self.assertTrue(plugin.debug)  # 确保调试模式已启用