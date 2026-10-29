<div align="center">

# 🔁 HanShift

**Zero-dependency · offline-first Simplified ⇄ Traditional Chinese converter**

Character mapping · phrase-level disambiguation · regional variants · automatic detection

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://github.com/gitstq/HanShift)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen)](./tests)
[![Offline](https://img.shields.io/badge/offline-first-orange)](https://github.com/gitstq/HanShift)

**🌐 Language / 語言：** [简体中文](./README.md) · [繁體中文](./README.zh-TW.md) · English

</div>

---

## 🎉 Introduction

Simplified Chinese merged many distinct traditional characters into one. **A single
simplified character often maps to several traditional ones.**

This is not trivia — it is *the* main source of errors when converting to traditional 👇

| Simplified | Possible traditional | Example |
|:---:|:---:|:---|
| 发 | **發** / **髮** | 经济**发**展 (develop, 發) · 我的头**发** (hair, 髮) |
| 干 | **乾** / **幹** | 天气**干**燥 (dry, 乾) · 埋头**干**活 (work, 幹) |
| 只 | **只** / **隻** | **只**是开始 (only, 只) · 一**只**猫 (classifier, 隻) |
| 面 | **面** / **麵** | 表**面**问题 (surface, 面) · 一碗**面**条 (noodles, 麵) |

Any tool that does naive character-by-character substitution will trip over this:
it turns "头发" (hair) into "頭**發**", and "干活" (to work) into "乾活".

**HanShift exists to fix exactly that.** It is not a lookup table — it is a three-stage
progressive pipeline:

> **Regional variants** → **Phrase-level disambiguation** → **Character-level fallback**

A phrase is matched first to lock in the context; only unmatched characters fall back to
the single-character map. Full coverage *and* high accuracy 🎯

### 🧭 Inspiration and positioning

OpenCC is an excellent prior art in this space, and its core idea — *phrases take priority
over single characters* — directly inspired this project. HanShift is, however,
**built entirely from scratch**: it uses none of OpenCC's source code or dictionaries,
and adds several targeted improvements:

- 🐍 **Pure Python, zero dependencies** — no compilation, no C++ library, works on PyPy and embedded runtimes
- 📦 **Compact** — all data is embedded as compact strings, no external dictionary files
- 🧩 **Phrases + context** — longest-match *plus* a **context-blocking** mechanism (see the "这只是开始" case below)
- 🔁 **Round-trip safe** — Simplified → Traditional → Simplified returns the original, covered by unit tests
- 🌏 **Three regions** — not just Taiwan, but Hong Kong usage as well (的士 / 巴士 / 軟件)

---

## ✨ Features

### 🎯 Phrase-level disambiguation (core capability)

**449 curated phrase rules** covering the one-to-many cases that break naive converters:

```python
convert("我的头发很长")        # -> 我的頭髮很長   ✅ 发 -> 髮  (hair)
convert("经济发展迅速")        # -> 經濟發展迅速   ✅ 发 -> 發  (develop)
convert("这是一个干燥的饼干")   # -> 這是一個乾燥的餅乾  ✅ 干 -> 乾  (dry)
convert("他干活很卖力")        # -> 他幹活很賣力   ✅ 干 -> 幹  (work)
```

### 🧠 Context awareness

Longest-match alone still has blind spots. Take 这只: it can be a classifier or a demonstrative pronoun:

```python
convert("房间里有一只猫")   # -> 房間裏有一隻貓   ✅ classifier -> 隻
convert("这只是开始")       # -> 這只是開始       ✅ pronoun -> stays 只
```

HanShift inspects the character **following** a matched phrase: if it is a predicate
particle or adverb (是 / 很 / 就 / 也 …), the match is rejected as a pronoun and skipped 💡

### 🌏 Regional variants (not just glyphs)

Swapping glyphs is not enough. Mainland China says 软件; Taiwan says **軟體**; Hong Kong
says **軟件**. One simplified word, three regional spellings.

```python
convert("软件工程师",  "s2t")   # -> 軟件工程師   glyphs only
convert("软件工程师",  "s2tw")  # -> 軟體工程師   Taiwan
convert("软件工程师",  "s2hk")  # -> 軟件工程師   Hong Kong
convert("出租车",      "s2hk")  # -> 的士         Hong Kong cab
convert("鼠标和打印机", "s2tw")  # -> 滑鼠和印表機  Taiwan IT terms
```

**235 Taiwanese** and **144 Hong Kong** variant entries ship out of the box, covering
IT, transport, food, and business vocabulary 🗺️

### 🔍 Automatic detection

```python
detect("中华人民共和国")      # -> ('simplified', 1.0)
detect("中華人民共和國")      # -> ('traditional', 1.0)
detect("这是简体和繁體混排")   # -> ('mixed', 0.75)
detect("Hello, world!")     # -> ('neutral', 0.0)
```

Feature-character scoring identifies mixed text and reports a confidence value 📊

### 📦 Genuinely dependency-free

**Zero third-party runtime dependencies** — only the standard library
(`argparse` / `re` / `json` / `os`). No network, no external dictionaries, no build
toolchain. Fully offline ✈️

### ⚡ Data at a glance

| Layer | Entries | Notes |
|:---|:---:|:---|
| Simplified → Traditional chars | **6,785** | CJK-wide simplified/traditional variants |
| Traditional → Simplified chars | **6,874** | Reverse mapping |
| Disambiguation phrases | **449** | One-to-many rules (hand curated) |
| Taiwanese variants | **235** | Mainland → Taiwan vocabulary |
| Hong Kong variants | **144** | Mainland → Hong Kong vocabulary |

---

## 🚀 Quick start

### 📋 Requirements

- **Python 3.8+** (CPython or PyPy)
- **No third-party dependencies**
- Windows / macOS / Linux

### 📥 Install

```bash
# Option 1: from PyPI (recommended)
pip install hanshift

# Option 2: from source
git clone https://github.com/gitstq/HanShift.git
cd HanShift
pip install .

# Option 3: no install at all, run straight from the clone
python -m hanshift convert "我的头发很长"
```

### ⚡ In three minutes

**Command line:**

```bash
# Simplified -> Traditional
hanshift convert "我的头发很长"
# -> 我的頭髮很長

# To Taiwanese standard (incl. regional vocabulary)
hanshift convert -t s2tw "鼠标和打印机"
# -> 滑鼠和印表機

# Traditional -> Simplified
hanshift convert -t t2s "軟體工程師在電腦上編寫程式碼"
# -> 软体工程师在电脑上编写程式码

# Detect which script a text uses
hanshift detect "中華人民共和國"

# Show every traditional candidate for a character
hanshift lookup 发
# -> 发 -> 發 髮

# List all conversion modes
hanshift modes
```

**Python API:**

```python
from hanshift import convert

convert("我的头发很长", "s2t")      # '我的頭髮很長'
convert("軟體工程師", "t2s")        # '软体工程师'
convert("鼠标和打印机", "s2tw")      # '滑鼠和印表機'
```

**Pipes:**

```bash
cat README.md | hanshift convert -t t2s > README.zh-CN.md
echo "房间里有一只猫" | hanshift convert
```

---

## 📖 Detailed guide

### 🔀 Conversion modes

| Mode | Meaning | Example |
|:---:|:---|:---|
| `s2t` | Simplified → Traditional (**glyphs only**) | 软件 → 軟件 |
| `t2s` | Traditional → Simplified (**glyphs only**) | 軟體 → 软体 |
| `s2tw` | Simplified → **Taiwan** (glyphs + Taiwan vocabulary) | 软件 → 軟體 |
| `s2twp` | Same as `s2tw` (alias) | 软件 → 軟體 |
| `s2hk` | Simplified → **Hong Kong** (glyphs + HK vocabulary) | 软件 → 軟件 |
| `tw2s` | Taiwan → Simplified (Taiwan vocabulary + glyphs) | 軟體 → 软件 |
| `hk2s` | Hong Kong → Simplified (HK vocabulary + glyphs) | 軟件 → 软件 |

> ⚠️ **Note:** `t2s` only restores glyphs — it will *not* turn 軟體 into 软件
> (that is a *vocabulary* difference). To localize Taiwanese copy for a mainland
> audience, use `tw2s`, not `t2s`.

### 🐍 Python API in depth

**One-liner:**

```python
from hanshift import convert

convert("中华人民共和国", "s2t")   # '中華人民共和國'
```

**Converter object** (recommended for batch work — reuse it):

```python
from hanshift import Converter

converter = Converter("s2tw")
converter.convert("鼠标和打印机")          # '滑鼠和印表機'
converter.convert("网络信息技术")          # '網路資訊技術'

# With statistics
result, stats = converter.convert_with_stats("中华人民共和国")
print(result)   # '中華人民共和國'
print(stats)    # {'mode': 's2t', 'source_length': 7, 'result_length': 7, 'changed_chars': 2}
```

**Cached instance** (fastest):

```python
from hanshift import get_converter

get_converter("s2t").convert("学习历史")
```

**Detection:**

```python
from hanshift import detect, detect_detail

detect("這是繁體中文")        # ('traditional', 1.0)
detect_detail("中华人民共和国")
# {'label': 'simplified', 'confidence': 1.0,
#  'simplified_marks': 2, 'traditional_marks': 0, 'length': 7}
```

**Candidate lookup** (great for debugging a conversion):

```python
from hanshift import candidates

candidates("发")   # ['發', '髮']
candidates("干")   # ['乾', '幹']
```

### 📁 Files and directories

```bash
# Single file
hanshift convert -i README.md -o README.zh-TW.md -t s2tw

# Whole directory, recursively, in place
hanshift convert -i docs/ -r --in-place -t s2tw

# Whole directory into a new tree
hanshift convert -i docs/ -o docs-zh-TW/ -r -t s2tw

# Restrict to specific extensions
hanshift convert -i src/ -r --in-place --ext .md,.txt,.rst

# Preview how much would change, without writing
hanshift convert -i docs/ -r --dry-run

# Show statistics
hanshift convert "中华人民共和国" --stats
```

See [`examples/batch_convert.py`](./examples/batch_convert.py) for the Python equivalent.

### 🖨️ JSON output (for scripts and CI)

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

### 🔧 CLI reference

| Command | Flag | Description |
|:---|:---|:---|
| `convert` | `-t, --target` | Conversion mode, defaults to `s2t` |
| | `-i, --input` | Input file or directory |
| | `-o, --output` | Output file or directory |
| | `--in-place` | Overwrite files in place |
| | `-r, --recursive` | Recurse into subdirectories |
| | `--ext` | Extension filter (comma separated) |
| | `--dry-run` | Preview only, do not write |
| | `--stats` | Print conversion statistics |
| | `--format` | `text` or `json` |
| `detect` | `-i, --input` | Input file |
| `lookup` | (positional) | One or more characters to look up |
| `modes` | — | List all modes |

> 💡 When `convert` gets neither text nor `-i`, it reads from **stdin**, which makes
> it easy to compose in pipelines.

---

## 💡 Design and roadmap

### 🏗️ Architecture

HanShift is a **three-stage progressive pipeline**; each stage has one job and is testable on its own:

```
input text
   │
   ▼
┌──────────────────────────────────────┐
│ Stage 1  Regional variants            │  软件 -> 軟體 / 軟件
│          longest match (optional)     │
├──────────────────────────────────────┤
│ Stage 2  Phrase disambiguation        │  头发 -> 頭髮、干活 -> 幹活
│          longest match + context block│
├──────────────────────────────────────┤
│ Stage 3  Rule-based extras            │  "3只" -> "3隻"
│          regex for open-ended patterns│
├──────────────────────────────────────┤
│ Stage 4  Character fallback           │  国 -> 國
└──────────────────────────────────────┘
   │
   ▼
output text
```

**Why this order?** Regional vocabulary must be replaced *before* glyph conversion.
Convert glyphs first and 软件 becomes 軟件, at which point the vocabulary entry for
软件 can never match again.

### 🔬 Where the data comes from

Character maps are not typed by hand. They are produced by a **custom generation pipeline**:

1. **Source** — parse `kTraditionalVariant` / `kSimplifiedVariant` from the official **Unicode Unihan Database**
2. **Drop self-references** — Unihan often lists the character itself as its own variant
   (e.g. 数 → 数 / 數); keeping it would silently skip conversion
3. **Prefer bidirectional agreement** — favour candidates whose reverse entry points back,
   which filters out a large amount of variant noise
4. **Conservative handling of ambiguous characters** — for 了 / 家 / 合 / 采 / 斗 / 曲 / 丑,
   the default is to **leave the glyph unchanged** and let phrase rules decide
5. **Manual correction of defaults** — fix cases where Unihan's first candidate is a
   variant rather than the modern standard form (e.g. 启 → 啓 corrected to 啟, 线 → 綫 corrected to 線)

Phrase rules and regional vocabulary tables are **hand curated**, focused on
high-frequency real-world usage.

### ⚖️ Trade-offs

| Decision | Choice | Rationale |
|:---|:---|:---|
| Dependencies | none | Embeddable anywhere, no supply-chain risk, small install |
| Data layout | compact string, parsed at import | Smaller and faster to import than dict literals |
| Matching | longest match | Keeps compound words intact instead of fragmenting them |
| Ambiguity default | keep original glyph | A missed conversion is far less damaging than a wrong one |
| Algorithm | per-position backtracking | O(n×L) is fast enough here; Aho-Corasick would be over-engineering |

### 🗺️ Roadmap

- [ ] 📈 Grow phrase rules to 1,000+, covering more specialist domains
- [ ] 🈶 Japanese kanji support (shinjitai / kyūjitai)
- [ ] 🔌 Optional Aho-Corasick matcher for very large corpora
- [ ] 🧪 Accuracy regression benchmark against parallel corpora, with a visual report
- [ ] 🌐 Optional WebAssembly build for browser integration
- [ ] 📝 User-supplied dictionaries (TOML/JSON overrides)

---

## 📦 Packaging and deployment

HanShift is a **library / CLI project**, so there are no binary artifacts to publish —
it is distributed through standard Python packaging.

### 🛠️ Build locally

A one-command build script is included:

```bash
# Linux / macOS / Git Bash
bash scripts/build.sh

# or use the standard tooling directly
python -m build
```

Artifacts land in `dist/`:

- `hanshift-1.0.0-py3-none-any.whl` — universal wheel, installable with `pip`
- `hanshift-1.0.0.tar.gz` — source distribution

### 🧪 Run the tests

```bash
bash scripts/run_tests.sh

# or directly
python -m unittest discover -s tests
```

**34 test cases** cover basic conversion, disambiguation, regional variants,
round-trip stability, and CLI end-to-end behaviour.

### 🚀 Publish to PyPI

```bash
python -m build
python -m twine upload dist/*
```

### 🐳 Containers and CI

```dockerfile
FROM python:3.11-slim
RUN pip install --no-cache-dir hanshift
ENTRYPOINT ["hanshift"]
```

```yaml
# GitHub Actions example
- name: Generate traditional docs
  run: |
    pip install hanshift
    hanshift convert -i docs/ -o docs-zh-TW/ -r -t s2tw
```

### 📌 Compatibility

| Environment | Status |
|:---|:---|
| Python 3.8 / 3.9 / 3.10 / 3.11 / 3.12 | ✅ Fully supported |
| CPython | ✅ Fully supported |
| PyPy | ✅ Supported (pure Python) |
| Windows / macOS / Linux | ✅ All platforms |
| Air-gapped / offline | ✅ Fully supported |

> ⚠️ **Caveats**
> - Files are read and written as **UTF-8**. Convert GBK / Big5 sources to UTF-8 first, otherwise you will get mojibake
> - Directory mode processes `.txt .md .rst .csv .json .yaml .yml .html` by default; override with `--ext`
> - `--in-place` **overwrites** your files — keep them under version control (Git), or run `--dry-run` first

---

## 🤝 Contributing

Contributions of any kind are welcome 🌟 — extra phrases, corrected mappings, or a better algorithm.

### 🔀 Commit convention

Please follow the **Angular commit convention**:

```
feat: new feature
fix: bug fix
docs: documentation
refactor: refactoring
test: tests
perf: performance
chore: tooling
```

Examples:

```
feat: add 50 IT-domain Taiwanese terms
fix: convert 线 to 線 instead of the variant 綫
docs: refresh quick-start examples
```

### 📋 PR checklist

- [ ] Code follows PEP 8 with clear comments
- [ ] New or changed behaviour is covered by unit tests
- [ ] `python -m unittest discover -s tests` passes
- [ ] Data-layer changes keep the "Data at a glance" table in READMEs up to date
- [ ] Commit message follows the Angular convention

### 🐛 Reporting issues

When reporting a wrong conversion, please include:

1. **Input text**
2. **Mode used** (e.g. `s2tw`)
3. **Actual output** and **expected output**
4. **HanShift version** (`hanshift --version`)
5. **Python version**

```
input:    我的头发很长
mode:     s2t
actual:   我的頭發很長
expected: 我的頭髮很長
version:  1.0.0
```

### 🧩 Contributing vocabulary data

If you know cross-strait or Hong Kong usage well, please contribute directly:

| File | Contents |
|:---|:---|
| `hanshift/data/s2t_phrases.py` | Disambiguation phrases (simplified → traditional) |
| `hanshift/data/variants_tw.py` | Mainland → Taiwan vocabulary |
| `hanshift/data/variants_hk.py` | Mainland → Hong Kong vocabulary |

The format is a uniform `{"simplified": "traditional"}` dict; place entries under the
grouping comment that matches them.

---

## 📄 License

Released under the **MIT License** — see [LICENSE](./LICENSE).

### 🙏 Credits and data sources

- **Mapping data** — single-character mappings are derived from the
  **Unicode Unihan Database** (`kTraditionalVariant` / `kSimplifiedVariant`), parsed,
  cross-checked and manually corrected by this project's own pipeline. Unicode data is
  used under the Unicode license; thanks to the Unicode Consortium.
- **Design inspiration** — OpenCC established the "phrases before characters" paradigm
  and was an important reference. HanShift uses **no OpenCC source code or dictionary
  files**; all code and word lists here were written independently.
- **Word lists** — disambiguation phrases and regional vocabulary were curated by hand
  around high-frequency everyday usage.

### ⚖️ Terms

- ✅ Commercial use, modification, distribution and private deployment allowed
- ✅ You are not required to open-source your own project
- ⚠️ Provided "as is", without warranty of any kind

---

<div align="center">

**If HanShift helped you, consider leaving a ⭐ Star!**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
