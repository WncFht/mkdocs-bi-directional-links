### 项目架构文档：MkDocs 双向链接插件

---

#### 项目概述
该项目是一个 MkDocs 插件，旨在为 Markdown 文件提供双向链接功能。通过解析 Markdown 文件中的 `[[file]]` 和 `[[file|text]]` 语法，插件能够自动生成相应的 HTML 标签（如链接、图片、视频、音频等），并支持文件路径的查找和解析。

---

### 项目文件结构

1. **`link_processor.py`**
2. **`plugin.py`**
3. **`search_integration.py`**
4. **`utils.py`**

---

### 文件详细说明

#### 1. **`link_processor.py`**
   - **功能**: 负责处理 Markdown 文件中的双向链接语法，将其转换为相应的 HTML 标签。
   - **类**:
     - **`LinkProcessor`**
       - **属性**:
         - `includes`: 支持的文件扩展名列表（如 `.md`, `.png`, `.jpg`, `.mp4`, `.mp3`）。
       - **方法**:
         - **`process_markdown(self, markdown, page, config, files, search_integration)`**
           - **功能**: 处理 Markdown 内容，替换双向链接语法为 HTML 标签。
           - **参数**:
             - `markdown`: 输入的 Markdown 内容。
             - `page`: 当前处理的页面对象。
             - `config`: MkDocs 配置对象。
             - `files`: 所有文件的列表。
             - `search_integration`: `SearchIntegration` 实例，用于查找文件路径。
           - **返回值**: 处理后的 Markdown 内容。
         - **`replace_bi_directional_link(match)`**（内部函数）
           - **功能**: 替换双向链接语法为 HTML 标签。
           - **参数**:
             - `match`: 正则表达式匹配对象。
           - **返回值**: 替换后的 HTML 标签或原始文本（如果文件未找到）。

---

#### 2. **`plugin.py`**
   - **功能**: 插件的核心入口，负责初始化插件、加载配置，并在 MkDocs 的生命周期中调用相应的处理方法。
   - **类**:
     - **`BiDirectionalLinksPlugin`**
       - **属性**:
         - `debug`: 是否启用调试模式。
         - `search_integration`: `SearchIntegration` 实例，用于文件路径查找。
         - `link_processor`: `LinkProcessor` 实例，用于处理 Markdown 内容。
       - **方法**:
         - **`__init__(self)`**
           - **功能**: 初始化插件，设置默认配置。
         - **`on_config(self, config)`**
           - **功能**: 在 MkDocs 加载配置时调用，初始化插件配置。
           - **参数**:
             - `config`: MkDocs 配置对象。
           - **返回值**: 更新后的配置对象。
         - **`on_page_markdown(self, markdown, page, config, files)`**
           - **功能**: 在解析 Markdown 文件时调用，处理双向链接语法。
           - **参数**:
             - `markdown`: 输入的 Markdown 内容。
             - `page`: 当前处理的页面对象。
             - `config`: MkDocs 配置对象。
             - `files`: 所有文件的列表。
           - **返回值**: 处理后的 Markdown 内容。

---

#### 3. **`search_integration.py`**
   - **功能**: 负责文件路径的查找和解析。
   - **类**:
     - **`SearchIntegration`**
       - **属性**:
         - `docs_dir`: MkDocs 文档目录路径。
       - **方法**:
         - **`__init__(self)`**
           - **功能**: 初始化 `SearchIntegration` 实例。
         - **`load_config(self, config)`**
           - **功能**: 加载 MkDocs 配置，初始化 `docs_dir`。
           - **参数**:
             - `config`: MkDocs 配置对象。
         - **`find_file(self, file_ref)`**
           - **功能**: 查找文件路径。
           - **参数**:
             - `file_ref`: 文件引用（如 `page1.md`）。
           - **返回值**: 文件路径（如果找到），否则返回 `None`。

---

#### 4. **`utils.py`**
   - **功能**: 提供工具函数，支持文件路径的解析。
   - **函数**:
     - **`resolve_file_path(file_ref, current_file_path, base_dir)`**
       - **功能**: 解析文件路径，支持相对路径和绝对路径。
       - **参数**:
         - `file_ref`: 文件引用（如 `page1.md`）。
         - `current_file_path`: 当前文件的路径。
         - `base_dir`: 基础目录路径。
       - **返回值**: 解析后的文件路径（如果找到），否则返回 `None`。

---

### 数据流图

1. **初始化阶段**:
   - MkDocs 加载配置，调用 `BiDirectionalLinksPlugin.on_config`，初始化 `SearchIntegration` 和 `LinkProcessor`。
2. **Markdown 处理阶段**:
   - MkDocs 解析 Markdown 文件，调用 `BiDirectionalLinksPlugin.on_page_markdown`。
   - `LinkProcessor.process_markdown` 处理 Markdown 内容，调用 `SearchIntegration.find_file` 查找文件路径。
   - 根据文件类型生成相应的 HTML 标签，返回处理后的 Markdown 内容。

---

### 依赖关系

- **`plugin.py`** 依赖于：
  - `search_integration.py` 中的 `SearchIntegration` 类。
  - `link_processor.py` 中的 `LinkProcessor` 类。
- **`link_processor.py`** 依赖于：
  - `search_integration.py` 中的 `SearchIntegration` 类。
- **`search_integration.py`** 依赖于：
  - `utils.py` 中的 `resolve_file_path` 函数（如果使用）。

---

### 调试与测试建议

1. **调试模式**:
   - 在 `mkdocs.yml` 中启用 `debug` 选项，查看插件加载和配置是否正确。
2. **文件路径测试**:
   - 确保 `docs_dir` 配置正确，并在 `find_file` 方法中添加调试日志，输出拼接后的路径。
3. **正则表达式测试**:
   - 使用在线工具（如 regex101.com）测试正则表达式，确保能够正确匹配 `[[file]]` 和 `[[file|text]]` 语法。
4. **单元测试**:
   - 为 `LinkProcessor` 和 `SearchIntegration` 编写单元测试，覆盖各种文件类型和路径情况。

---

### 总结

该插件通过 `LinkProcessor` 处理 Markdown 中的双向链接语法，`SearchIntegration` 负责查找文件路径，`BiDirectionalLinksPlugin` 作为核心入口，管理插件的生命周期和配置。通过合理的模块划分和接口设计，插件能够高效地处理双向链接，并支持多种文件类型。