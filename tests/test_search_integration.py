import unittest
from mkdocs_bi_directional_links.search_integration import SearchIntegration

class TestSearchIntegration(unittest.TestCase):
    def test_find_file(self):
        """
        测试 Search 插件的文件查找功能。
        """
        search_integration = SearchIntegration()
        # 模拟 MkDocs 配置
        config = {"docs_dir": "docs", "plugins": {"search": {}}}
        search_integration.load_config(config)

        # 模拟查找文件
        file_ref = "page1.md"
        result = search_integration.find_file(file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "docs/page1.md")  # 确保路径正确