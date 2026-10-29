"""HanShift 基础用法示例。

运行方式::

    python examples/basic_usage.py
"""

from hanshift import Converter, convert, detect, detect_detail

SECTION = "-" * 60


def main():
    print(SECTION)
    print("1. 一行式转换")
    print(SECTION)
    print("s2t  我的头发很长        ->", convert("我的头发很长", "s2t"))
    print("t2s  我的頭髮很長        ->", convert("我的頭髮很長", "t2s"))
    print("s2tw 鼠标和打印机        ->", convert("鼠标和打印机", "s2tw"))
    print("s2hk 软件工程师          ->", convert("软件工程师", "s2hk"))
    print("tw2s 滑鼠和印表機        ->", convert("滑鼠和印表機", "tw2s"))

    print()
    print(SECTION)
    print("2. 歧义消解（本项目的核心能力）")
    print(SECTION)
    samples = [
        "我的头发很长",        # 发 -> 髮
        "经济发展迅速",        # 发 -> 發
        "这是一个干燥的饼干",  # 干 -> 乾
        "他干活很卖力",        # 干 -> 幹
        "房间里有一只猫",      # 只 -> 隻
        "这只是开始",          # 只 -> 只（指示代词，保持不变）
    ]
    for sample in samples:
        print("  %-12s -> %s" % (sample, convert(sample, "s2t")))

    print()
    print(SECTION)
    print("3. 转换器对象与统计信息")
    print(SECTION)
    converter = Converter("s2t")
    result, stats = converter.convert_with_stats("中华人民共和国")
    print("  转换结果:", result)
    print("  统计信息:", stats)

    print()
    print(SECTION)
    print("4. 简繁体检测")
    print(SECTION)
    for text in ["这是简体中文", "這是繁體中文", "这是简体和繁體混排", "Hello, world!"]:
        label, confidence = detect(text)
        print("  %-16s -> %-12s (置信度 %.2f)" % (text, label, confidence))
    print()
    print("  详细报告:", detect_detail("中华人民共和国"))


if __name__ == "__main__":
    main()
