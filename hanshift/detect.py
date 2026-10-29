"""简繁体检测：判断一段文本是简体、繁体还是混排。

原理：分别统计文本中「简体特征字」与「繁体特征字」的命中数量。
特征字指那些在简繁之间存在字形差异的字，例如「们」只可能是简体，
「們」只可能是繁体。二者比例决定判定结果与置信度。
"""

from .data import S2T_CHAR, T2S_CHAR

# 简体特征字：存在对应繁体字形的简体字
_SIMP_MARKS = frozenset(ch for ch, trad in S2T_CHAR.items() if trad != ch)
# 繁体特征字：存在对应简体字形的繁体字
_TRAD_MARKS = frozenset(ch for ch, simp in T2S_CHAR.items() if simp != ch)

#: 判定结果标签
SIMPLIFIED = "simplified"
TRADITIONAL = "traditional"
MIXED = "mixed"
NEUTRAL = "neutral"


def detect(text):
    """检测文本使用的字形体系。

    返回 ``(label, confidence)``：
    label 为 ``simplified`` / ``traditional`` / ``mixed`` / ``neutral``，
    confidence 为 0.0 ~ 1.0 的置信度。
    """
    if not text:
        return NEUTRAL, 0.0

    simp_hits = 0
    trad_hits = 0
    for ch in text:
        if ch in _SIMP_MARKS:
            simp_hits += 1
        if ch in _TRAD_MARKS:
            trad_hits += 1

    total = simp_hits + trad_hits
    if total == 0:
        return NEUTRAL, 0.0

    ratio = max(simp_hits, trad_hits) / total
    minority = min(simp_hits, trad_hits)

    # 少数派占比超过 15% 视为混排，避免个别字干扰整体判断
    if minority / total >= 0.15:
        return MIXED, ratio
    if simp_hits > trad_hits:
        return SIMPLIFIED, ratio
    return TRADITIONAL, ratio


def detect_detail(text):
    """返回更详细的检测信息（字典形式），便于程序生成 JSON 报告。"""
    simp_hits = sum(1 for ch in text if ch in _SIMP_MARKS)
    trad_hits = sum(1 for ch in text if ch in _TRAD_MARKS)
    label, confidence = detect(text)
    return {
        "label": label,
        "confidence": round(confidence, 4),
        "simplified_marks": simp_hits,
        "traditional_marks": trad_hits,
        "length": len(text),
    }
