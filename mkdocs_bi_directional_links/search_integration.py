import os
import logging
from typing import List, Optional

class SearchIntegration:
    def __init__(self):
        self.docs_dir = ""
        self.file_cache = {}

    def load_config(self, config):
        """
        加载 MkDocs 配置，初始化 Search 插件。
        """
        self.docs_dir = config["docs_dir"]

    def load_files(self, files):
        """
        加载文件列表，初始化文件缓存。
        """
        self._build_file_cache(files)

    def _build_file_cache(self, files):
        """
        构建文件缓存。
        """
        for file in files:
            file_path = file.src_path.replace("\\", "/")
            file_name = os.path.basename(file_path)

            # 缓存文件名到路径的映射
            if file_name not in self.file_cache:
                self.file_cache[file_name] = [file_path]
            else:
                self.file_cache[file_name].append(file_path)

        # self.print_cache()

    def find_file(self, from_file: str, file_ref: str) -> Optional[str]:
        """
        查找文件路径。
        """
        from_file = from_file.replace("\\", "/")
        # print(f"查找文件：from_file={from_file}, file_ref={file_ref}")  # 输出当前查找的文件

        file_name = os.path.basename(file_ref)
        # logging.debug(f"处理 EzLink：file_name={file_name}")  # 输出文件名

        # 快速文件缓存查找
        if file_name in self.file_cache:
            # logging.debug(f"快速文件缓存查找：file_name={file_name}, 缓存={self.file_cache[file_name]}")  # 输出缓存内容
            # 如果有多个匹配项，直接返回第一个
            return self.file_cache[file_name][0]

        return None

    def print_cache(self):
        """
        打印缓存内容。
        """
        logging.info("文件名到路径的映射：")
        for file_name, paths in self.file_cache.items():
            logging.info(f"{file_name}: {paths}")