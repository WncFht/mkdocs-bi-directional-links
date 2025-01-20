import os
import logging

class SearchIntegration:
    def __init__(self):
        self.docs_dir = ""

    def load_config(self, config):
        """
        加载 MkDocs 配置，初始化 Search 插件。
        """
        self.docs_dir = config["docs_dir"]

    def find_file(self, file_ref):
        """
        查找文件路径。
        """
        # 拼接文件路径
        file_path = os.path.join(self.docs_dir, file_ref)
        logging.info(f"查找文件路径：{file_path}")  # 添加调试日志
        if os.path.isfile(file_path):
            # 统一路径分隔符为正斜杠
            return file_path.replace("\\", "/")
        return None