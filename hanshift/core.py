"""HanShift 转换引擎核心。

采用三层管线，逐级精细化处理：

    第一层  地区用语差异（软件 -> 軟體 / 軟件）
    第二层  歧义词组消歧（头发 -> 頭髮，解决「发 -> 發/髮」一对多难题）
    第三层  单字默认映射（国 -> 國）

每一层均使用「最长匹配优先」策略，保证复合词整体替换，
避免逐字转换导致的碎片化错误。
"""

import re
from .data import (
    S2T_CHAR,
    T2S_CHAR,
    S2T_PHRASES,
    TW_VARIANTS,
    HK_VARIANTS,
)


def _reverse_mapping(table):
    """反转映射表，冲突时保留首次出现的条目（保持结果稳定可预期）。"""
    out = {}
    for key, value in table.items():
        if value not in out:
            out[value] = key
    return out


# 反向词组表：繁体词组 -> 简体词组（由简转繁词组表反转而来）
T2S_PHRASES = _reverse_mapping(S2T_PHRASES)

# 反向地区用语表：台湾/香港用词 -> 大陆用词
TW2S_VARIANTS = _reverse_mapping(TW_VARIANTS)
HK2S_VARIANTS = _reverse_mapping(HK_VARIANTS)

# 规则型补充：无法用静态词组穷举的模式，例如「3只」「12只」这类数量短语
S2T_RULES = [
    (re.compile(r"(\d+)只"), r"\1隻"),
]

# 上下文阻断：某些词组若后接特定字符，说明是另一用法，不应替换。
# 典型场景：「这只是开始」中的「这只」是指代词，而「这只猫」中的「这只」才是量词。
# 后接谓语类虚词/副词时判定为指示代词，保持原形。
_PREDICATE_HINTS = set("是就很也才却并又让使在会能要说做叫被都还只太真可已经还")

PHRASE_BLOCK_NEXT = {
    "这只": _PREDICATE_HINTS,
    "那只": _PREDICATE_HINTS,
    "哪只": _PREDICATE_HINTS,
}


def _max_key_len(table):
    return max((len(k) for k in table), default=1)


def _replace_longest(text, table, maxlen, block_next=None):
    """最长匹配替换：优先命中更长的词组，未命中则原样保留单字。

    ``block_next`` 提供上下文阻断能力：命中词组但下一字符属于阻断集合时，
    放弃该匹配并回退尝试更短的匹配，从而降低「同形异用」带来的误转。
    """
    if not table:
        return text
    out = []
    i = 0
    n = len(text)
    while i < n:
        matched = None
        used = 1
        upper = min(maxlen, n - i)
        for length in range(upper, 0, -1):
            segment = text[i:i + length]
            if segment not in table:
                continue
            if block_next:
                block = block_next.get(segment)
                if block and i + length < n and text[i + length] in block:
                    continue  # 上下文不符，尝试更短匹配
            matched = table[segment]
            used = length
            break
        out.append(matched if matched is not None else text[i])
        i += used
    return "".join(out)


class Converter:
    """简繁转换器。

    支持的转换模式：

    ==========  ==========================================
    模式        说明
    ==========  ==========================================
    s2t         简体 -> 繁体（仅字形）
    t2s         繁体 -> 简体（仅字形）
    s2tw        简体 -> 台湾正体（字形 + 台湾用语）
    s2twp       同 s2tw（兼容常见命名的别名）
    s2hk        简体 -> 香港繁体（字形 + 香港用语）
    tw2s        台湾正体 -> 简体（用语 + 字形）
    hk2s        香港繁体 -> 简体（用语 + 字形）
    ==========  ==========================================
    """

    #: 所有可用模式
    MODES = ("s2t", "t2s", "s2tw", "s2twp", "s2hk", "tw2s", "hk2s")

    #: 每个模式的管线配置：(地区用语表, 词组表, 单字表, 规则表)
    _PIPELINES = {
        "s2t": (None, S2T_PHRASES, S2T_CHAR, S2T_RULES),
        "s2tw": (TW_VARIANTS, S2T_PHRASES, S2T_CHAR, S2T_RULES),
        "s2twp": (TW_VARIANTS, S2T_PHRASES, S2T_CHAR, S2T_RULES),
        "s2hk": (HK_VARIANTS, S2T_PHRASES, S2T_CHAR, S2T_RULES),
        "t2s": (None, T2S_PHRASES, T2S_CHAR, None),
        "tw2s": (TW2S_VARIANTS, T2S_PHRASES, T2S_CHAR, None),
        "hk2s": (HK2S_VARIANTS, T2S_PHRASES, T2S_CHAR, None),
    }

    def __init__(self, mode="s2t"):
        if mode not in self._PIPELINES:
            raise ValueError(
                "不支持的转换模式: %s，可选: %s" % (mode, ", ".join(self.MODES))
            )
        self.mode = mode
        variants, phrases, chars, rules = self._PIPELINES[mode]
        self.variants = variants or {}
        self.phrases = phrases or {}
        self.chars = chars or {}
        self.rules = rules or []
        self._variants_max = _max_key_len(self.variants)
        self._phrases_max = _max_key_len(self.phrases)

    def convert(self, text):
        """转换文本。"""
        if not text:
            return text
        result = text
        # 第一层：地区用语差异
        if self.variants:
            result = _replace_longest(result, self.variants, self._variants_max)
        # 第二层：歧义词组消歧
        if self.phrases:
            block = PHRASE_BLOCK_NEXT if self.chars is S2T_CHAR else None
            result = _replace_longest(result, self.phrases, self._phrases_max, block)
        # 第三层：规则补充（如「3只」->「3隻」）
        for pattern, replacement in self.rules:
            result = pattern.sub(replacement, result)
        # 第四层：单字默认映射
        if self.chars:
            chars = self.chars
            result = "".join(chars.get(ch, ch) for ch in result)
        return result

    def convert_with_stats(self, text):
        """转换文本并返回统计信息。

        返回 ``(converted, stats)``，stats 包含原文/译文长度与变更字符数。
        """
        converted = self.convert(text)
        changed = sum(1 for a, b in zip(text, converted) if a != b)
        stats = {
            "mode": self.mode,
            "source_length": len(text),
            "result_length": len(converted),
            "changed_chars": changed + abs(len(text) - len(converted)),
        }
        return converted, stats


#: 模式 -> 转换器实例的缓存，避免重复构建
_CACHE = {}


def get_converter(mode="s2t"):
    """获取指定模式的转换器（带缓存）。"""
    converter = _CACHE.get(mode)
    if converter is None:
        converter = Converter(mode)
        _CACHE[mode] = converter
    return converter


def convert(text, mode="s2t"):
    """一行式转换快捷函数。

    >>> convert("我的头发很长", "s2t")
    '我的頭髮很長'
    """
    return get_converter(mode).convert(text)


def candidates(char):
    """查询某个字在简繁转换中可能对应的所有字形。

    用于排查转换结果，例如 ``candidates("发")`` 会返回 ``發`` 与 ``髮``。
    """
    result = []
    if char in S2T_CHAR:
        result.append(S2T_CHAR[char])
    # 反向：找出所有映射到该字的繁体字形
    for trad, simp in T2S_CHAR.items():
        if simp == char and trad not in result:
            result.append(trad)
    # 词组表中出现的相关字形
    for simp, trad in S2T_PHRASES.items():
        if char in simp:
            for idx, ch in enumerate(simp):
                if ch == char and idx < len(trad) and trad[idx] not in result:
                    result.append(trad[idx])
    return result
