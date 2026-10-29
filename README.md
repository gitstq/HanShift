<div align="center">

# 🔁 HanShift

**零依赖 · 离线优先的简繁中文转换引擎**

单字映射 · 词组级歧义消解 · 两岸港台用语差异 · 简繁自动检测

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://github.com/gitstq/HanShift)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen)](./tests)
[![Offline](https://img.shields.io/badge/offline-first-orange)](https://github.com/gitstq/HanShift)

**🌐 语言 / Language：** 简体中文 · [繁體中文](./README.zh-TW.md) · [English](./README.en.md)

</div>

---

## 🎉 项目介绍

简体字在历史上合并了大量繁体字：**一个简体字，往往对应多个繁体字**。

这不是冷知识，而是简转繁时最大的坑 👇

| 简体字 | 可能的繁体 | 例子 |
|:---:|:---:|:---|
| 发 | **發** / **髮** | 经济**发**展（發）· 我的头**发**（髮） |
| 干 | **乾** / **幹** | 天气**干**燥（乾）· 埋头**干**活（幹） |
| 只 | **只** / **隻** | **只**是开始（只）· 一**只**猫（隻） |
| 面 | **面** / **麵** | 表**面**问题（面）· 一碗**面**条（麵） |

只做「逐字替换」的工具会无一例外地翻车：把「头发」变成「頭**發**」，把「干活」变成「乾活」。

**HanShift 就是为解决这个痛点而生的。** 它不是简单的查表工具，而是一套三层递进的转换管线：

> **地区用语差异** → **歧义词组消解** → **单字默认映射**

先用词组锁定语境，再回退到单字映射，从而在保证覆盖率的同时把准确率拉满 🎯

### 🧭 灵感来源与设计定位

市面上已有优秀的 OpenCC 项目，它的设计思路（词组优先于单字）给了本项目直接的启发。HanShift **完全独立自研**，未使用 OpenCC 的任何代码，并在以下方面做了针对性优化：

- 🐍 **纯 Python 零依赖**：不编译、不装 C++ 库，`pip install` 即用，可跑在 PyPy / 嵌入式环境中
- 📦 **体积可控**：全部数据以紧凑字符串内嵌，无外部词典文件，单包即可运行
- 🧩 **词组 + 上下文双保险**：除最长匹配外，额外引入**上下文阻断**机制（见下文「这只是开始」案例）
- 🔁 **双向往返一致**：简 → 繁 → 简 可稳定回到原文，已纳入单元测试保障
- 🌏 **两岸暨港台三地差异化**：不仅分台湾，也区分香港用词（的士 / 巴士 / 軟件）

---

## ✨ 核心特性

### 🎯 词组级歧义消解（核心能力）

内置 **449 条**歧义词组规则，覆盖日常生活中最容易出错的一对多场景：

```python
convert("我的头发很长")        # -> 我的頭髮很長   ✅ 发 -> 髮
convert("经济发展迅速")        # -> 經濟發展迅速   ✅ 发 -> 發
convert("这是一个干燥的饼干")   # -> 這是一個乾燥的餅乾  ✅ 干 -> 乾
convert("他干活很卖力")        # -> 他幹活很賣力   ✅ 干 -> 幹
```

### 🧠 上下文感知阻断

纯最长匹配仍有边界情况。比如「这只」既可能是量词，也可能是指示代词：

```python
convert("房间里有一只猫")   # -> 房間裏有一隻貓   ✅ 量词，取「隻」
convert("这只是开始")       # -> 這只是開始       ✅ 代词，保持「只」
```

HanShift 会检查命中词组的**后继字符**：若紧跟谓语类虚词（是 / 很 / 就 / 也……），则判定为指示代词用法并放弃替换 💡

### 🌏 地区用语差异（不只是换字形）

简体转繁体，只换字形是不够的。大陆说「软件」，台湾说「**軟體**」，香港说「**軟件**」——同一个简体词，在不同地区有不同译法。

```python
convert("软件工程师",  "s2t")   # -> 軟件工程師   仅字形转换
convert("软件工程师",  "s2tw")  # -> 軟體工程師   台湾正体
convert("软件工程师",  "s2hk")  # -> 軟件工程師   香港繁体
convert("出租车",      "s2hk")  # -> 的士         香港用语
convert("鼠标和打印机", "s2tw")  # -> 滑鼠和印表機  台湾用语
```

内置 **228 条**台湾用语 + **144 条**香港用语差异词表，覆盖 IT、交通、饮食、商业等高频领域 🗺️

### 🔍 简繁体自动检测

```python
detect("中华人民共和国")      # -> ('simplified', 1.0)
detect("中華人民共和國")      # -> ('traditional', 1.0)
detect("这是简体和繁體混排")   # -> ('mixed', 0.75)
detect("Hello, world!")     # -> ('neutral', 0.0)
```

基于特征字统计打分，可识别混排文本并给出置信度 📊

### 📦 真正的零依赖

**运行期 0 个第三方依赖**，仅使用 Python 标准库（`argparse` / `re` / `json` / `os`）。
不联网、不读外部词典、不需要编译工具链，完全离线运行 ✈️

### ⚡ 数据规模一览

| 数据层 | 条目数 | 说明 |
|:---|:---:|:---|
| 简体 → 繁体单字 | **6,785** | 覆盖 CJK 全字集的简繁异体字 |
| 繁体 → 简体单字 | **6,874** | 反向映射 |
| 歧义词组 | **449** | 一对多消歧规则（人工编纂） |
| 台湾用语 | **228** | 大陆 → 台湾用词差异 |
| 香港用语 | **144** | 大陆 → 香港用词差异 |

---

## 🚀 快速开始

### 📋 环境要求

- **Python 3.8 及以上**（CPython / PyPy 均可）
- **无需任何第三方依赖**
- 支持 Windows / macOS / Linux 全平台

### 📥 安装

```bash
# 方式一：从 PyPI 安装（推荐）
pip install hanshift

# 方式二：从源码安装
git clone https://github.com/gitstq/HanShift.git
cd HanShift
pip install .

# 方式三：免安装，直接运行（克隆后即可用）
python -m hanshift convert "我的头发很长"
```

### ⚡ 三分钟上手

**命令行：**

```bash
# 简体转繁体
hanshift convert "我的头发很长"
# 输出: 我的頭髮很長

# 转台湾正体（含地区用语）
hanshift convert -t s2tw "鼠标和打印机"
# 输出: 滑鼠和印表機

# 繁体转简体
hanshift convert -t t2s "軟體工程師在電腦上編寫程式碼"
# 输出: 软体工程师在电脑上编写程式码

# 检测文本类型
hanshift detect "中華人民共和國"

# 查询某个字的所有繁体候选
hanshift lookup 发
# 输出: 发 -> 發 髮

# 查看所有转换模式
hanshift modes
```

**Python API：**

```python
from hanshift import convert

convert("我的头发很长", "s2t")      # '我的頭髮很長'
convert("軟體工程師", "t2s")        # '软体工程师'
convert("鼠标和打印机", "s2tw")      # '滑鼠和印表機'
```

**管道调用：**

```bash
cat README.md | hanshift convert -t t2s > README.zh-CN.md
echo "房间里有一只猫" | hanshift convert
```

---

## 📖 详细使用指南

### 🔀 转换模式全表

| 模式 | 说明 | 示例 |
|:---:|:---|:---|
| `s2t` | 简体 → 繁体（**仅字形**） | 软件 → 軟件 |
| `t2s` | 繁体 → 简体（**仅字形**） | 軟體 → 软体 |
| `s2tw` | 简体 → **台湾**正体（字形 + 台湾用语） | 软件 → 軟體 |
| `s2twp` | 同 `s2tw`（别名，兼容常见命名习惯） | 软件 → 軟體 |
| `s2hk` | 简体 → **香港**繁体（字形 + 香港用语） | 软件 → 軟件 |
| `tw2s` | 台湾正体 → 简体（台湾用语 + 字形） | 軟體 → 软件 |
| `hk2s` | 香港繁体 → 简体（香港用语 + 字形） | 軟件 → 软件 |

> ⚠️ **注意**：`t2s` 只做字形还原，不会把「軟體」改成「软件」（那是**用词**层面的事）。
> 如果你要把台湾文案转成大陆文案，请用 `tw2s` 而不是 `t2s`。

### 🐍 Python API 详解

**一行式快捷函数：**

```python
from hanshift import convert

convert("中华人民共和国", "s2t")   # '中華人民共和國'
```

**转换器对象（推荐用于批量场景，复用实例避免重复构建）：**

```python
from hanshift import Converter

converter = Converter("s2tw")
converter.convert("鼠标和打印机")          # '滑鼠和印表機'
converter.convert("网络信息技术")          # '網路資訊技術'

# 带统计信息
result, stats = converter.convert_with_stats("中华人民共和国")
print(result)   # '中華人民共和國'
print(stats)    # {'mode': 's2t', 'source_length': 7, 'result_length': 7, 'changed_chars': 2}
```

**获取缓存实例（最高效）：**

```python
from hanshift import get_converter

get_converter("s2t").convert("学习历史")
```

**简繁检测：**

```python
from hanshift import detect, detect_detail

detect("這是繁體中文")        # ('traditional', 1.0)
detect_detail("中华人民共和国")
# {'label': 'simplified', 'confidence': 1.0,
#  'simplified_marks': 2, 'traditional_marks': 0, 'length': 7}
```

**查询候选字形（排查利器）：**

```python
from hanshift import candidates

candidates("发")   # ['發', '髮']
candidates("干")   # ['乾', '幹']
```

### 📁 文件与目录批量转换

```bash
# 单个文件
hanshift convert -i README.md -o README.zh-TW.md -t s2tw

# 整个目录递归转换（原地覆盖）
hanshift convert -i docs/ -r --in-place -t s2tw

# 整个目录转换到新目录
hanshift convert -i docs/ -o docs-zh-TW/ -r -t s2tw

# 只处理指定扩展名
hanshift convert -i src/ -r --in-place --ext .md,.txt,.rst

# 先预览会改动多少，不实际写入
hanshift convert -i docs/ -r --dry-run

# 输出统计信息
hanshift convert "中华人民共和国" --stats
```

Python 侧批量处理可参考 [`examples/batch_convert.py`](./examples/batch_convert.py)。

### 🖨️ JSON 输出（便于集成到脚本 / CI）

```bash
hanshift convert --format json "中华人民共和国"
```

```json
{
  "result": "中華人民共和國",
  "stats": {
    "mode": "s2t",
    "source_length": 7,
    "result_length": 7,
    "changed_chars": 2
  }
}
```

```bash
hanshift detect --format json "中華人民共和國"
```

```json
{
  "label": "traditional",
  "confidence": 1.0,
  "simplified_marks": 0,
  "traditional_marks": 3,
  "length": 7
}
```

### 🔧 命令行参数速查

| 命令 | 参数 | 说明 |
|:---|:---|:---|
| `convert` | `-t, --target` | 转换模式，默认 `s2t` |
| | `-i, --input` | 输入文件或目录 |
| | `-o, --output` | 输出文件或目录 |
| | `--in-place` | 原地覆盖写入 |
| | `-r, --recursive` | 递归处理子目录 |
| | `--ext` | 扩展名过滤（逗号分隔） |
| | `--dry-run` | 只预览不写入 |
| | `--stats` | 输出转换统计 |
| | `--format` | `text` 或 `json` |
| `detect` | `-i, --input` | 输入文件 |
| `lookup` | （位置参数） | 待查询的汉字，可多个 |
| `modes` | — | 列出所有模式 |

> 💡 `convert` 命令省略文本且未指定 `-i` 时，会自动从**标准输入**读取，方便管道组合。

---

## 💡 设计思路与迭代规划

### 🏗️ 架构设计

HanShift 采用**三层递进管线**，每一层职责单一、可独立测试：

```
输入文本
   │
   ▼
┌──────────────────────────────────────┐
│ 第一层  地区用语差异                    │  软件 -> 軟體 / 軟件
│        最长匹配替换（可关闭）           │
├──────────────────────────────────────┤
│ 第二层  歧义词组消解                    │  头发 -> 頭髮、干活 -> 幹活
│        最长匹配 + 上下文阻断            │
├──────────────────────────────────────┤
│ 第三层  规则补充                        │  「3只」->「3隻」
│        正则处理无法穷举的模式            │
├──────────────────────────────────────┤
│ 第四层  单字默认映射                    │  国 -> 國
└──────────────────────────────────────┘
   │
   ▼
输出文本
```

**为什么是这个顺序？** 因为地区用语必须先于字形转换执行。
若先做字形转换，「软件」会变成「軟件」，此时再用语表去匹配「软件」就永远匹配不上了。

### 🔬 数据是怎么来的

单字映射表并非手工录入，而是通过一条**自研生成管线**产出：

1. **数据源**：解析 Unicode 官方 Unihan 数据库的 `kTraditionalVariant` / `kSimplifiedVariant` 字段
2. **排除自身候选**：Unihan 常把本字自身也列为变体（如「数 → 数 / 數」），必须剔除，否则会漏转换
3. **双向互证优先**：优先选择「繁体字的简体候选反向也包含该简体字」的候选，过滤掉大量异体字噪声
4. **高频歧义字保守保留**：对「了 / 家 / 合 / 采 / 斗 / 曲 / 丑」这类字，默认**不改变字形**，交给词组层精确处理
5. **人工校正默认字形**：修正 Unihan 首选候选为异体字的情况（如「启 → 啓」修正为「啟」、「线 → 綫」修正为「線」）

歧义词组与地区用语表则为**人工编纂**，聚焦高频真实场景。

### ⚖️ 设计权衡

| 决策 | 选择 | 理由 |
|:---|:---|:---|
| 依赖策略 | 零依赖 | 可嵌入任何环境，无供应链风险，安装体积可控 |
| 数据结构 | 紧凑字符串 + 运行时解析 | 比字典字面量体积更小，启动更快 |
| 匹配策略 | 最长匹配 | 保证复合词整体替换，避免碎片化 |
| 歧义默认 | 保守保留原形 | 宁可少转，不可错转（错转比漏转更伤可读性） |
| 匹配算法 | 逐位置回溯 | 数据量下 O(n×L) 足够快，无需引入 Aho-Corasick 复杂度 |

### 🗺️ 后续迭代规划

- [ ] 📈 扩充歧义词组至 1000+ 条，覆盖更多专业领域
- [ ] 🈶 支持日语汉字（新字体 / 旧字体）转换
- [ ] 🔌 提供 Aho-Corasick 多模式匹配加速（大文本 / 百万级吞吐场景）
- [ ] 🧪 增加基于平行语料的准确率回归基准（可视化报告）
- [ ] 🌐 提供可选的 WebAssembly 版本，用于浏览器端集成
- [ ] 📝 用户自定义词典加载能力（支持外部 TOML/JSON 覆盖）

---

## 📦 打包与部署指南

HanShift 属于**工具库 / CLI 类项目**，无需上传 Release 二进制产物，通过标准 Python 打包分发即可。

### 🛠️ 本地构建

项目提供了一键构建脚本：

```bash
# Linux / macOS / Git Bash
bash scripts/build.sh

# 或直接使用标准工具
python -m build
```

构建产物位于 `dist/`，包含：

- `hanshift-1.0.0-py3-none-any.whl` — 通用 wheel，可直接 `pip install`
- `hanshift-1.0.0.tar.gz` — 源码包

### 🧪 运行测试

```bash
bash scripts/run_tests.sh

# 或直接
python -m unittest discover -s tests
```

当前测试覆盖 **34 个用例**，包含基础转换、歧义消解、地区用语、往返一致性、CLI 端到端。

### 🚀 发布到 PyPI

```bash
python -m build
python -m twine upload dist/*
```

### 🐳 在容器 / CI 中使用

```dockerfile
FROM python:3.11-slim
RUN pip install --no-cache-dir hanshift
ENTRYPOINT ["hanshift"]
```

```yaml
# GitHub Actions 示例
- name: 生成繁体版文档
  run: |
    pip install hanshift
    hanshift convert -i docs/ -o docs-zh-TW/ -r -t s2tw
```

### 📌 兼容环境说明

| 环境 | 支持情况 |
|:---|:---|
| Python 3.8 / 3.9 / 3.10 / 3.11 / 3.12 | ✅ 完全支持 |
| CPython | ✅ 完全支持 |
| PyPy | ✅ 支持（纯 Python 实现） |
| Windows / macOS / Linux | ✅ 全平台支持 |
| 离线环境（无网络） | ✅ 完全支持 |

> ⚠️ **注意事项**
> - 所有文本文件按 **UTF-8** 读写；若源文件是 GBK / Big5 编码，请先转换为 UTF-8，否则会出现乱码
> - 目录批量转换默认只处理 `.txt .md .rst .csv .json .yaml .yml .html`，可用 `--ext` 自定义
> - 使用 `--in-place` 会**直接覆盖原文件**，建议提前做好版本控制（Git）或先跑 `--dry-run` 预览

---

## 🤝 贡献指南

欢迎任何形式的贡献 🌟 无论是补充词组、修正映射，还是改进算法。

### 🔀 PR 提交规范

提交信息请遵循 **Angular 提交规范**：

```
feat: 新增功能
fix: 修复问题
docs: 文档更新
refactor: 代码重构
test: 测试相关
perf: 性能优化
chore: 构建/工具相关
```

示例：

```
feat: 补充 50 条 IT 领域台湾用语
fix: 修正「线」被转换为异体字「綫」的问题
docs: 更新快速开始示例
```

### 📋 PR 检查清单

- [ ] 代码符合 PEP 8 规范，注释清晰
- [ ] 新增 / 修改的功能配有对应单元测试
- [ ] `python -m unittest discover -s tests` 全部通过
- [ ] 若修改了数据层，同步更新 README 中的「数据规模一览」
- [ ] 提交信息遵循 Angular 规范

### 🐛 Issue 反馈规则

提交转换错误的 Issue 时，请务必包含以下信息，以便快速定位：

1. **输入文本**（原文）
2. **使用的模式**（如 `s2tw`）
3. **实际输出**与**期望输出**
4. **HanShift 版本**（`hanshift --version`）
5. **Python 版本**

```
输入: 我的头发很长
模式: s2t
实际输出: 我的頭發很長
期望输出: 我的頭髮很長
版本: 1.0.0
```

### 🧩 贡献词表数据

如果你熟悉两岸暨港台用语差异，欢迎直接补充：

| 文件 | 内容 |
|:---|:---|
| `hanshift/data/s2t_phrases.py` | 歧义词组（简 → 繁） |
| `hanshift/data/variants_tw.py` | 大陆 → 台湾用语 |
| `hanshift/data/variants_hk.py` | 大陆 → 香港用语 |

数据格式统一为 `{"简体词": "繁体词"}`，请按注释中的分组归类放置。

---

## 📄 开源协议说明

本项目基于 **MIT License** 开源，详见 [LICENSE](./LICENSE)。

### 🙏 致谢与数据来源说明

- **映射数据来源**：单字简繁映射关系由 **Unicode Unihan Database** 的 `kTraditionalVariant` / `kSimplifiedVariant` 字段，经本项目自研管线解析、校验与人工校正后生成。Unicode 数据遵循 Unicode 许可协议，特此致谢 Unicode Consortium。
- **设计思路启发**：OpenCC 项目在简繁转换领域树立了「词组优先于单字」的范式，为本项目提供了重要参考。HanShift **未使用 OpenCC 的任何源代码或词典文件**，全部代码与词表均为独立编写。
- **词表编纂**：歧义词组与地区用语差异表由人工编纂，聚焦日常高频场景。

### ⚖️ 使用须知

- ✅ 允许商业使用、修改、分发、私有化部署
- ✅ 无需开放你的项目源码
- ⚠️ 软件按「现状」提供，不作任何明示或暗示的担保

---

<div align="center">

**如果 HanShift 帮到了你，欢迎点个 ⭐ Star 支持一下！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
