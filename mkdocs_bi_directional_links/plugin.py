import logging
from mkdocs.plugins import BasePlugin
from .search_integration import SearchIntegration
from .link_processor import LinkProcessor

class BiDirectionalLinksPlugin(BasePlugin):
    def __init__(self):
        self.debug = False  # 是否启用调试模式
        self.search_integration = SearchIntegration()  # Search 插件集成模块
        self.link_processor = LinkProcessor()  # 双向链接处理模块

    def on_config(self, config):
        """
        在 MkDocs 加载配置时调用，初始化插件配置。
        """
        self.debug = self.config.get("debug", False)  # 从配置中读取调试模式
        self.search_integration.load_config(config)  # 加载 Search 插件配置
        if self.debug:
            logging.info("BiDirectionalLinksPlugin: 调试模式已启用。")
        return config

    def on_page_markdown(self, markdown, page, config, files):
        """
        在解析 Markdown 文件时调用，处理双向链接语法。
        """
        return self.link_processor.process_markdown(markdown, page, config, files, self.search_integration)