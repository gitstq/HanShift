"""HanShift 批量文件转换示例。

演示如何把一个目录下的 Markdown 文档批量转换为繁体版本。

运行方式::

    python examples/batch_convert.py <源目录> <输出目录>
"""

import os
import sys

from hanshift import get_converter


def convert_tree(src_dir, out_dir, mode="s2t", exts=(".md", ".txt")):
    """递归转换目录中的文本文件。"""
    converter = get_converter(mode)
    total = 0
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames.sort()
        for name in sorted(filenames):
            if not name.lower().endswith(exts):
                continue
            source = os.path.join(dirpath, name)
            rel = os.path.relpath(source, src_dir)
            target = os.path.join(out_dir, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(source, "r", encoding="utf-8") as handle:
                original = handle.read()
            converted, stats = converter.convert_with_stats(original)
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(converted)
            total += 1
            print("  %s -> %s（变更 %d 字符）" % (source, target, stats["changed_chars"]))
    return total


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src, out = sys.argv[1], sys.argv[2]
    if not os.path.isdir(src):
        print("源目录不存在: %s" % src)
        return 1
    print("开始批量转换（模式 s2t）:")
    count = convert_tree(src, out)
    print("完成，共处理 %d 个文件。" % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
