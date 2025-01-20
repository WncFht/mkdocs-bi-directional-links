### 测试设计文档：MkDocs 双向链接插件

---

#### 测试目标
本测试设计文档旨在为 MkDocs 双向链接插件的各个模块提供详细的测试方案，确保插件功能正确、稳定。测试覆盖以下模块：
1. **`LinkProcessor`**: 负责处理 Markdown 中的双向链接语法。
2. **`BiDirectionalLinksPlugin`**: 插件的核心入口，负责初始化和配置。
3. **`SearchIntegration`**: 负责文件路径的查找和解析。

---

### 测试范围

1. **`LinkProcessor` 测试**:
   - 测试双向链接语法的解析和替换。
   - 测试不同文件类型（Markdown、图片、视频、音频）的处理。
   - 测试自定义文本的双向链接。
   - 测试文件未找到时的处理逻辑。

2. **`BiDirectionalLinksPlugin` 测试**:
   - 测试插件初始化。
   - 测试配置加载（如调试模式）。
   - 测试插件在 MkDocs 生命周期中的行为。

3. **`SearchIntegration` 测试**:
   - 测试文件路径的查找功能。
   - 测试路径拼接和文件存在性检查。
   - 测试相对路径和绝对路径的解析。

---

### 测试用例设计

#### 1. **`LinkProcessor` 测试用例**

| 测试用例编号 | 描述 | 输入 | 预期输出 |
|--------------|------|------|----------|
| LP-01 | 测试普通双向链接 | `[[page1.md]]` | `<a href="tests/test_data/page1.md">page1.md</a>` |
| LP-02 | 测试带自定义文本的双向链接 | `[[page1.md\|第一页]]` | `<a href="tests/test_data/page1.md">第一页</a>` |
| LP-03 | 测试图片链接 | `![[image.png]]` | `<img src="tests/test_data/image.png" alt="image.png">` |
| LP-04 | 测试视频链接 | `![[video.mp4]]` | `<video controls><source src="tests/test_data/video.mp4"></video>` |
| LP-05 | 测试音频链接 | `![[audio.mp3]]` | `<audio controls><source src="tests/test_data/audio.mp3"></audio>` |
| LP-06 | 测试文件未找到时的处理 | `[[nonexistent.md]]` | 返回原始文本 `[[nonexistent.md]]` |

#### 2. **`BiDirectionalLinksPlugin` 测试用例**

| 测试用例编号 | 描述 | 输入 | 预期输出 |
|--------------|------|------|----------|
| BP-01 | 测试插件初始化 | 无 | `debug` 默认为 `False` |
| BP-02 | 测试配置加载（启用调试模式） | `{"debug": True}` | `debug` 为 `True` |
| BP-03 | 测试配置加载（未启用调试模式） | `{"debug": False}` | `debug` 为 `False` |

#### 3. **`SearchIntegration` 测试用例**

| 测试用例编号 | 描述 | 输入 | 预期输出 |
|--------------|------|------|----------|
| SI-01 | 测试文件查找功能 | `page1.md` | 返回 `docs/page1.md` |
| SI-02 | 测试文件未找到时的处理 | `nonexistent.md` | 返回 `None` |
| SI-03 | 测试路径拼接 | `subdir/page2.md` | 返回 `docs/subdir/page2.md` |

