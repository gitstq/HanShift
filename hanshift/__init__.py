"""HanShift — 零依赖、离线优先的简繁中文转换引擎。

核心能力：

* 简体 ⇄ 繁体双向转换
* 词组级「一对多」歧义消解（如 头发 -> 頭髮、干活 -> 幹活）
* 两岸 / 港台地区用语差异（如 软件 -> 軟體 / 軟件）
* 简繁体自动检测

快速上手::

    from hanshift import convert

    convert("我的头发很长", "s2t")      # '我的頭髮很長'
    convert("軟體工程師", "t2s")         # '软件工程师'
    convert("鼠标和打印机", "s2tw")      # '滑鼠和印表機'
"""

from .core import Converter, convert, get_converter, candidates
from .detect import detect, detect_detail

__version__ = "1.0.0"
__all__ = [
    "Converter",
    "convert",
    "get_converter",
    "candidates",
    "detect",
    "detect_detail",
    "__version__",
]
