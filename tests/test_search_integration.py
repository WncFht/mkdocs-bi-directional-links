import unittest
from mkdocs_bi_directional_links.search_integration import SearchIntegration

class TestSearchIntegration(unittest.TestCase):
    def test_find_file(self):
        """
        测试 Search 插件的文件查找功能。
        """
        search_integration = SearchIntegration()
        # 模拟 MkDocs 配置
        config = {"docs_dir": "tests/test_data", "plugins": {"search": {}}}
        search_integration.load_config(config)

        # 模拟查找文件
        file_ref = "page1.md"
        result = search_integration.find_file(file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "tests/test_data/page1.md")  # 确保路径正确

    def test_find_file_not_found(self):
        """
        测试文件未找到时的处理逻辑。
        """
        search_integration = SearchIntegration()
        config = {"docs_dir": "tests/test_data", "plugins": {"search": {}}}
        search_integration.load_config(config)

        # 模拟查找不存在的文件
        file_ref = "nonexistent.md"
        result = search_integration.find_file(file_ref)
        self.assertIsNone(result)  # 确保返回 None

    def test_find_file_with_subdir(self):
        """
        测试子目录中的文件查找。
        """
        search_integration = SearchIntegration()
        config = {"docs_dir": "tests/test_data", "plugins": {"search": {}}}
        search_integration.load_config(config)

        # 模拟查找子目录中的文件
        file_ref = "subdir/page2.md"
        result = search_integration.find_file(file_ref)
        self.assertIsNotNone(result)  # 确保找到文件
        self.assertEqual(result, "tests/test_data/subdir/page2.md")  # 确保路径正确