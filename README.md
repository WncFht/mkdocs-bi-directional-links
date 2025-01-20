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

## 搜索逻辑

以下是基于你提供的两个文件的 **搜索逻辑文档**，详细描述了插件的查找逻辑、路径解析、文件匹配规则以及生成链接的过程。文档旨在帮助开发者理解插件的核心功能和工作原理。

---

# 双向链接插件搜索逻辑文档

## 概述
该插件用于在 Markdown 文件中支持双向链接语法（如 `[[page]]` 或 `[[page|text]]`），并能够根据文件名或路径查找对应的文件。插件通过扫描指定目录下的文件，构建文件名和路径的映射表，并在解析 Markdown 时动态查找和生成链接。

---

## 核心功能
1. **支持双向链接语法**：
   - 解析 `[[page]]` 或 `[[page|text]]` 语法。
   - 支持图片、音频、视频和 Markdown 文件的链接。

2. **文件查找与路径解析**：
   - 根据文件名或路径查找对应的文件。
   - 支持相对路径和绝对路径模式。

3. **动态生成链接**：
   - 根据文件类型生成对应的 HTML 标签（如 `<a>`、`<img>`、`<audio>`、`<video>`）。

---

## 搜索逻辑

### 1. **初始化阶段**
在插件初始化时，会扫描指定目录下的文件，并构建两个映射表：

#### 1.1 文件扫描
- 使用 `globSync` 扫描指定目录（`rootDir`）下的文件。
- 支持的文件类型包括：
  - Markdown 文件（`*.md`）。
  - 图片文件（如 `.png`、`.jpg`、`.svg` 等）。
  - 音频文件（如 `.mp3`、`.wav` 等）。
  - 视频文件（如 `.mp4`、`.webm` 等）。

#### 1.2 构建映射表
- **`possibleBiDirectionalLinksInCleanBaseNameOfFilePaths`**：
  - 文件名（不含路径）到文件相对路径的映射。
  - 例如：`page3.md` -> `dir2/page3.md`。
- **`possibleBiDirectionalLinksInFullFilePaths`**：
  - 文件完整路径到文件相对路径的映射。
  - 例如：`docs/dir2/page3.md` -> `dir2/page3.md`。

#### 1.3 处理文件名冲突
- 如果多个文件具有相同的文件名，则将这些文件从 `possibleBiDirectionalLinksInCleanBaseNameOfFilePaths` 中移除，仅保留在 `possibleBiDirectionalLinksInFullFilePaths` 中。

---

### 2. **查找逻辑**
在 Markdown 解析过程中，插件会匹配双向链接语法，并尝试查找对应的文件路径。

#### 2.1 匹配双向链接语法
- 使用正则表达式 `biDirectionalLinkPattern` 匹配 `[[page]]` 或 `[[page|text]]` 语法。
- 提取 `href`（文件名或路径）和 `text`（显示的文本）。

#### 2.2 处理特殊链接
- 如果 `href` 以 `#` 或 `^` 开头，表示这是一个锚点链接（指向当前文件的某个部分），直接生成链接并返回。

#### 2.3 转换路径格式
- 将 `href` 转换为操作系统特定的路径格式（`osSpecificHref`）。
- 如果 `href` 没有文件扩展名，默认添加 `.md` 扩展名（假设目标文件是 Markdown 文件）。

#### 2.4 查找文件路径
- 调用 `findBiDirectionalLinks` 函数，在以下两个映射表中查找匹配的文件路径：
  1. **`possibleBiDirectionalLinksInCleanBaseNameOfFilePaths`**：基于文件名查找。
  2. **`possibleBiDirectionalLinksInFullFilePaths`**：基于完整路径查找。
- 如果找到多个匹配项，优先使用第一个匹配项，并输出警告日志。

#### 2.5 处理查找结果
- 如果未找到匹配的文件路径，输出警告日志并跳过该链接。
- 如果找到匹配的文件路径，根据文件类型生成对应的 HTML 标签。

---

### 3. **路径解析与生成**
#### 3.1 相对路径模式
- 如果启用了相对路径模式（`isRelativePath`），计算目标文件相对于当前文件的相对路径。
- 例如：
  - 当前文件：`dir1/index.md`。
  - 目标文件：`dir2/page3.md`。
  - 生成的相对路径：`../dir2/page3.md`。

#### 3.2 绝对路径模式
- 如果未启用相对路径模式，生成基于 `baseDir` 的绝对路径。
- 例如：
  - `baseDir`：`/docs`。
  - 目标文件：`dir2/page3.md`。
  - 生成的绝对路径：`/docs/dir2/page3.md`。

---

### 4. **生成链接**
根据文件类型生成对应的 HTML 标签：

#### 4.1 Markdown 文件
- 生成 `<a>` 标签。
- 示例：
  ```html
  <a href="/docs/dir2/page3.md">Page 3</a>
  ```

#### 4.2 图片文件
- 生成 `<img>` 标签。
- 示例：
  ```html
  <img src="/docs/dir2/image.png" alt="Image">
  ```

#### 4.3 音频文件
- 生成 `<audio>` 标签。
- 示例：
  ```html
  <audio controls preload="metadata" aria-label="Audio">
    <source src="/docs/dir2/audio.mp3">
  </audio>
  ```

#### 4.4 视频文件
- 生成 `<video>` 标签。
- 示例：
  ```html
  <video controls preload="metadata" aria-label="Video">
    <source src="/docs/dir2/video.mp4">
  </video>
  ```

---

### 5. **日志与警告**
插件在查找过程中会输出详细的日志和警告信息，帮助开发者调试问题：
- **未找到匹配文件**：输出警告日志，提示可能的原因（如文件不存在、路径错误等）。
- **文件名冲突**：输出警告日志，提示多个文件具有相同的文件名。
- **路径解析失败**：输出警告日志，提示路径解析失败的原因。

---

## 总结
该插件的搜索逻辑通过文件名和路径的映射表实现了高效的文件查找，并支持多种文件类型的链接生成。通过灵活的路径解析和详细的日志输出，插件能够满足复杂的 Markdown 文档需求。