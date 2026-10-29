"""数据层：单字映射、歧义词组、地区用语差异。"""

from .s2t_chars import S2T_CHAR
from .t2s_chars import T2S_CHAR
from .s2t_phrases import S2T_PHRASES
from .variants_tw import TW_VARIANTS
from .variants_hk import HK_VARIANTS

__all__ = [
    "S2T_CHAR",
    "T2S_CHAR",
    "S2T_PHRASES",
    "TW_VARIANTS",
    "HK_VARIANTS",
]
