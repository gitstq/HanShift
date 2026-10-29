<div align="center">

# 🔁 HanShift

**零依賴 · 離線優先的簡繁中文轉換引擎**

單字映射 · 詞組級歧義消解 · 兩岸港台用語差異 · 簡繁自動檢測

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://github.com/gitstq/HanShift)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Tests](https://img.shields.io/badge/tests-34%20passed-brightgreen)](./tests)
[![Offline](https://img.shields.io/badge/offline-first-orange)](https://github.com/gitstq/HanShift)

**🌐 語言 / Language：** 簡體中文 · [繁體中文](./README.zh-TW.md) · [English](./README.en.md)

</div>

---

## 🎉 專案介紹

簡體字在歷史上合併了大量繁體字：**一個簡體字，往往對應多個繁體字**。

這不是冷知識，而是簡轉繁時最大的坑 👇

| 簡體字 | 可能的繁體 | 例子 |
|:---:|:---:|:---|
| 发 | **發** / **髮** | 經濟**发**展（發）· 我的頭**发**（髮） |
| 干 | **乾** / **幹** | 天氣**干**燥（乾）· 埋頭**干**活（幹） |
| 只 | **只** / **隻** | **只**是開始（只）· 一**只**貓（隻） |
| 面 | **面** / **麵** | 表**面**問題（面）· 一碗**面**條（麵） |

只做「逐字替換」的工具會無一例外地翻車：把「头发」變成「頭**發**」，把「干活」變成「乾活」。

**HanShift 就是為解決這個痛點而生的。** 它不是簡單的查表工具，而是一套三層遞進的轉換管線：

> **地區用語差異** → **歧義詞組消解** → **單字預設映射**

先用詞組鎖定語境，再回退到單字映射，從而在保證覆蓋率的同時把準確率拉滿 🎯

### 🧭 靈感來源與設計定位

市面上已有優秀的 OpenCC 專案，它的設計思路（詞組優先於單字）給了本專案直接的啟發。HanShift **完全獨立自研**，未使用 OpenCC 的任何程式碼，並在以下方面做了針對性最佳化：

- 🐍 **純 Python 零依賴**：不編譯、不裝 C++ 庫，`pip install` 即用，可跑在 PyPy / 嵌入式環境中
- 📦 **體積可控**：全部資料以緊湊字串內嵌，無外部詞典檔案，單包即可運行
- 🧩 **詞組 + 上下文雙保險**：除最長匹配外，額外引入**上下文阻斷**機制（見下文「这只是开始」案例）
- 🔁 **雙向往返一致**：簡 → 繁 → 簡 可穩定回到原文，已納入單元測試保障
- 🌏 **兩岸暨港台三地差異化**：不僅分台灣，也區分香港用詞（的士 / 巴士 / 軟件）

---

## ✨ 核心特性

### 🎯 詞組級歧義消解（核心能力）

內置 **449 條**歧義詞組規則，覆蓋日常生活中最容易出錯的一對多場景：

```python
convert("我的头发很长")        # -> 我的頭髮很長   ✅ 发 -> 髮
convert("经济发展迅速")        # -> 經濟發展迅速   ✅ 发 -> 發
convert("这是一个干燥的饼干")   # -> 這是一個乾燥的餅乾  ✅ 干 -> 乾
convert("他干活很卖力")        # -> 他幹活很賣力   ✅ 干 -> 幹
```

### 🧠 上下文感知阻斷

純最長匹配仍有邊界情況。比如「這隻」既可能是量詞，也可能是指示代詞：

```python
convert("房间里有一只猫")   # -> 房間裏有一隻貓   ✅ 量词，取「隻」
convert("这只是开始")       # -> 這只是開始       ✅ 代词，保持「只」
```

HanShift 會檢查命中詞組的**後繼字符**：若緊跟謂語類虛詞（是 / 很 / 就 / 也……），則判定為指示代詞用法並放棄替換 💡

### 🌏 地區用語差異（不只是換字形）

簡體轉繁體，只換字形是不夠的。大陸說「软件」，台灣說「**軟體**」，香港說「**軟件**」——同一個簡體詞，在不同地區有不同譯法。

```python
convert("软件工程师",  "s2t")   # -> 軟件工程師   仅字形转换
convert("软件工程师",  "s2tw")  # -> 軟體工程師   台湾正体
convert("软件工程师",  "s2hk")  # -> 軟件工程師   香港繁体
convert("出租车",      "s2hk")  # -> 的士         香港用语
convert("鼠标和打印机", "s2tw")  # -> 滑鼠和印表機  台湾用语
```

內置 **235 條**台灣用語 + **144 條**香港用語差異詞表，覆蓋 IT、交通、飲食、商業等高頻領域 🗺️

### 🔍 簡繁體自動檢測

```python
detect("中华人民共和国")      # -> ('simplified', 1.0)
detect("中華人民共和國")      # -> ('traditional', 1.0)
detect("这是简体和繁體混排")   # -> ('mixed', 0.75)
detect("Hello, world!")     # -> ('neutral', 0.0)
```

基於特徵字統計打分，可識別混排文本並給出置信度 📊

### 📦 真正的零依賴

**運行期 0 個第三方依賴**，僅使用 Python 標準庫（`argparse` / `re` / `json` / `os`）。
不聯網、不讀外部詞典、不需要編譯工具鏈，完全離線運行 ✈️

### ⚡ 資料規模一覽

| 資料層 | 條目數 | 說明 |
|:---|:---:|:---|
| 簡體 → 繁體單字 | **6,785** | 覆蓋 CJK 全字集的簡繁異體字 |
| 繁體 → 簡體單字 | **6,874** | 反向映射 |
| 歧義詞組 | **449** | 一對多消歧規則（人工編纂） |
| 台灣用語 | **235** | 大陸 → 台灣用詞差異 |
| 香港用語 | **144** | 大陸 → 香港用詞差異 |

---

## 🚀 快速開始

### 📋 環境要求

- **Python 3.8 及以上**（CPython / PyPy 均可）
- **無需任何第三方依賴**
- 支援 Windows / macOS / Linux 全平臺

### 📥 安裝

```bash
# 方式一：從 PyPI 安裝（推薦）
pip install hanshift

# 方式二：從源碼安裝
git clone https://github.com/gitstq/HanShift.git
cd HanShift
pip install .

# 方式三：免安裝，直接運行（複製後即可用）
python -m hanshift convert "我的头发很长"
```

### ⚡ 三分鐘上手

**命令行：**

```bash
# 簡體轉繁體
hanshift convert "我的头发很长"
# 輸出: 我的頭髮很長

# 轉台灣正體（含地區用語）
hanshift convert -t s2tw "鼠标和打印机"
# 輸出: 滑鼠和印表機

# 繁體轉簡體
hanshift convert -t t2s "軟體工程師在電腦上編寫程式碼"
# 輸出: 软体工程師在電腦上編寫程式碼

# 檢測文本類型
hanshift detect "中華人民共和國"

# 查詢某個字的所有繁體候選
hanshift lookup 发
# 輸出: 發 -> 發 髮

# 查看所有轉換模式
hanshift modes
```

**Python API：**

```python
from hanshift import convert

convert("我的头发很长", "s2t")      # '我的頭髮很長'
convert("軟體工程師", "t2s")        # '软体工程师'
convert("鼠标和打印机", "s2tw")      # '滑鼠和印表機'
```

**管道調用：**

```bash
cat README.md | hanshift convert -t t2s > README.zh-CN.md
echo "房间里有一只猫" | hanshift convert
```

---

## 📖 詳細使用指南

### 🔀 轉換模式全表

| 模式 | 說明 | 示例 |
|:---:|:---|:---|
| `s2t` | 簡體 → 繁體（**僅字形**） | 软件 → 軟件 |
| `t2s` | 繁體 → 簡體（**僅字形**） | 軟體 → 软体 |
| `s2tw` | 簡體 → **台灣**正體（字形 + 台灣用語） | 软件 → 軟體 |
| `s2twp` | 同 `s2tw`（別名，相容常見命名習慣） | 软件 → 軟體 |
| `s2hk` | 簡體 → **香港**繁體（字形 + 香港用語） | 软件 → 軟件 |
| `tw2s` | 台灣正體 → 簡體（台灣用語 + 字形） | 軟體 → 软件 |
| `hk2s` | 香港繁體 → 簡體（香港用語 + 字形） | 軟件 → 软件 |

> ⚠️ **註意**：`t2s` 只做字形還原，不會把「軟體」改成「软件」（那是**用詞**層面的事）。
> 如果你要把台灣文案轉成大陸文案，請用 `tw2s` 而不是 `t2s`。

### 🐍 Python API 詳解

**一行式快捷函數：**

```python
from hanshift import convert

convert("中华人民共和国", "s2t")   # '中華人民共和國'
```

**轉換器物件（推薦用於批量場景，復用實體避免重複構建）：**

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

**獲取快取實體（最高效）：**

```python
from hanshift import get_converter

get_converter("s2t").convert("学习历史")
```

**簡繁檢測：**

```python
from hanshift import detect, detect_detail

detect("這是繁體中文")        # ('traditional', 1.0)
detect_detail("中华人民共和国")
# {'label': 'simplified', 'confidence': 1.0,
#  'simplified_marks': 2, 'traditional_marks': 0, 'length': 7}
```

**查詢候選字形（排查利器）：**

```python
from hanshift import candidates

candidates("发")   # ['發', '髮']
candidates("干")   # ['乾', '幹']
```

### 📁 檔案與目錄批量轉換

```bash
# 單個檔案
hanshift convert -i README.md -o README.zh-TW.md -t s2tw

# 整個目錄遞迴轉換（原地覆蓋）
hanshift convert -i docs/ -r --in-place -t s2tw

# 整個目錄轉換到新目錄
hanshift convert -i docs/ -o docs-zh-TW/ -r -t s2tw

# 只處理指定副檔名
hanshift convert -i src/ -r --in-place --ext .md,.txt,.rst

# 先預覽會改動多少，不實際寫入
hanshift convert -i docs/ -r --dry-run

# 輸出統計資訊
hanshift convert "中华人民共和国" --stats
```

Python 側批量處理可參考 [`examples/batch_convert.py`](./examples/batch_convert.py)。

### 🖨️ JSON 輸出（便於集成到腳本 / CI）

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

### 🔧 命令行參數速查

| 命令 | 參數 | 說明 |
|:---|:---|:---|
| `convert` | `-t, --target` | 轉換模式，預設 `s2t` |
| | `-i, --input` | 輸入檔案或目錄 |
| | `-o, --output` | 輸出檔案或目錄 |
| | `--in-place` | 原地覆蓋寫入 |
| | `-r, --recursive` | 遞迴處理子目錄 |
| | `--ext` | 副檔名過濾（逗號分隔） |
| | `--dry-run` | 只預覽不寫入 |
| | `--stats` | 輸出轉換統計 |
| | `--format` | `text` 或 `json` |
| `detect` | `-i, --input` | 輸入檔案 |
| `lookup` | （位置參數） | 待查詢的漢字，可多個 |
| `modes` | — | 列出所有模式 |

> 💡 `convert` 命令省略文本且未指定 `-i` 時，會自動從**標準輸入**讀取，方便管道組合。

---

## 💡 設計思路與疊代規劃

### 🏗️ 架構設計

HanShift 採用**三層遞進管線**，每一層職責單一、可獨立測試：

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

**為什麼是這個順序？** 因為地區用語必須先於字形轉換執行。
若先做字形轉換，「软件」會變成「軟件」，此時再用語表去匹配「软件」就永遠匹配不上了。

### 🔬 資料是怎麼來的

單字映射表並非手工録入，而是通過一條**自研生成管線**產出：

1. **資料源**：解析 Unicode 官方 Unihan 資料庫的 `kTraditionalVariant` / `kSimplifiedVariant` 字段
2. **排除自身候選**：Unihan 常把本字自身也列為變體（如「數 → 數 / 數」），必須剔除，否則會漏轉換
3. **雙向互證優先**：優先選擇「繁體字的簡體候選反向也包含該簡體字」的候選，過濾掉大量異體字噪聲
4. **高頻歧義字保守保留**：對「了 / 家 / 合 / 采 / 斗 / 曲 / 丑」這類字，預設**不改變字形**，交給詞組層精確處理
5. **人工校正預設字形**：修正 Unihan 首選候選為異體字的情況（如「啟 → 啓」修正為「啟」、「線 → 綫」修正為「線」）

歧義詞組與地區用語表則為**人工編纂**，聚焦高頻真實場景。

### ⚖️ 設計權衡

| 決策 | 選擇 | 理由 |
|:---|:---|:---|
| 依賴策略 | 零依賴 | 可嵌入任何環境，無供應鏈風險，安裝體積可控 |
| 資料結構 | 緊湊字串 + 運行時解析 | 比字典字面量體積更小，啟動更快 |
| 匹配策略 | 最長匹配 | 保證復合詞整體替換，避免碎片化 |
| 歧義預設 | 保守保留原形 | 寧可少轉，不可錯轉（錯轉比漏轉更傷可讀性） |
| 匹配演算法 | 逐位置回溯 | 資料量下 O(n×L) 足夠快，無需引入 Aho-Corasick 複雜度 |

### 🗺️ 後續疊代規劃

- [ ] 📈 擴充歧義詞組至 1000+ 條，覆蓋更多專業領域
- [ ] 🈶 支援日語漢字（新字體 / 舊字體）轉換
- [ ] 🔌 提供 Aho-Corasick 多模式匹配加速（大文本 / 百萬級吞吐場景）
- [ ] 🧪 增加基於平行語料的準確率回歸基準（可視化報告）
- [ ] 🌐 提供可選的 WebAssembly 版本，用於瀏覽器端集成
- [ ] 📝 用戶自定義詞典加載能力（支援外部 TOML/JSON 覆蓋）

---

## 📦 打包與部署指南

HanShift 屬於**工具庫 / CLI 類專案**，無需上傳 Release 二進制產物，通過標準 Python 打包分發即可。

### 🛠️ 本地構建

專案提供了一鍵構建腳本：

```bash
# Linux / macOS / Git Bash
bash scripts/build.sh

# 或直接使用標準工具
python -m build
```

構建產物位於 `dist/`，包含：

- `hanshift-1.0.0-py3-none-any.whl` — 通用 wheel，可直接 `pip install`
- `hanshift-1.0.0.tar.gz` — 源碼包

### 🧪 運行測試

```bash
bash scripts/run_tests.sh

# 或直接
python -m unittest discover -s tests
```

當前測試覆蓋 **34 個用例**，包含基礎轉換、歧義消解、地區用語、往返一致性、CLI 端到端。

### 🚀 發布到 PyPI

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

### 📌 相容環境說明

| 環境 | 支援情況 |
|:---|:---|
| Python 3.8 / 3.9 / 3.10 / 3.11 / 3.12 | ✅ 完全支援 |
| CPython | ✅ 完全支援 |
| PyPy | ✅ 支援（純 Python 實現） |
| Windows / macOS / Linux | ✅ 全平臺支援 |
| 離線環境（無網路） | ✅ 完全支援 |

> ⚠️ **註意事項**
> - 所有文本檔案按 **UTF-8** 讀寫；若來源檔案是 GBK / Big5 編碼，請先轉換為 UTF-8，否則會出現亂碼
> - 目錄批量轉換預設只處理 `.txt .md .rst .csv .json .yaml .yml .html`，可用 `--ext` 自定義
> - 使用 `--in-place` 會**直接覆蓋原檔案**，建議提前做好版本控制（Git）或先跑 `--dry-run` 預覽

---

## 🤝 貢獻指南

歡迎任何形式的貢獻 🌟 無論是補充詞組、修正映射，還是改進演算法。

### 🔀 PR 提交規範

提交資訊請遵循 **Angular 提交規範**：

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

### 📋 PR 檢查清單

- [ ] 程式碼符合 PEP 8 規範，註解清晰
- [ ] 新增 / 修改的功能配有對應單元測試
- [ ] `python -m unittest discover -s tests` 全部通過
- [ ] 若修改了資料層，同步更新 README 中的「資料規模一覽」
- [ ] 提交資訊遵循 Angular 規範

### 🐛 Issue 反饋規則

提交轉換錯誤的 Issue 時，請務必包含以下資訊，以便快速定位：

1. **輸入文本**（原文）
2. **使用的模式**（如 `s2tw`）
3. **實際輸出**与**期望輸出**
4. **HanShift 版本**（`hanshift --version`）
5. **Python 版本**

```
输入: 我的头发很长
模式: s2t
实际输出: 我的頭發很長
期望输出: 我的頭髮很長
版本: 1.0.0
```

### 🧩 貢獻詞表資料

如果你熟悉兩岸暨港台用語差異，歡迎直接補充：

| 檔案 | 內容 |
|:---|:---|
| `hanshift/data/s2t_phrases.py` | 歧義詞組（簡 → 繁） |
| `hanshift/data/variants_tw.py` | 大陸 → 台灣用語 |
| `hanshift/data/variants_hk.py` | 大陸 → 香港用語 |

資料格式統一為 `{"简体词": "繁体词"}`，請按註解中的分組歸類放置。

---

## 📄 開源協議說明

本專案基於 **MIT License** 開源，詳見 [LICENSE](./LICENSE)。

### 🙏 致謝與資料來源說明

- **映射資料來源**：單字簡繁映射關係由 **Unicode Unihan Database** 的 `kTraditionalVariant` / `kSimplifiedVariant` 字段，經本專案自研管線解析、校驗與人工校正後生成。Unicode 資料遵循 Unicode 許可協議，特此致謝 Unicode Consortium。
- **設計思路啟發**：OpenCC 專案在簡繁轉換領域樹立了「詞組優先於單字」的范式，為本專案提供了重要參考。HanShift **未使用 OpenCC 的任何原始碼或詞典檔案**，全部程式碼與詞表均為獨立編寫。
- **詞表編纂**：歧義詞組與地區用語差異表由人工編纂，聚焦日常高頻場景。

### ⚖️ 使用須知

- ✅ 允許商業使用、修改、分發、私有化部署
- ✅ 無需開放你的專案源碼
- ⚠️ 软件按「現狀」提供，不作任何明示或暗示的擔保

---

<div align="center">

**如果 HanShift 幫到了你，歡迎點個 ⭐ Star 支援一下！**

Made with ❤️ by [gitstq](https://github.com/gitstq)

</div>
