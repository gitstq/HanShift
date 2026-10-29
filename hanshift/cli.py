"""HanShift 命令行界面。

用法示例::

    hanshift convert "我的头发很长"                 # 简体转繁体
    hanshift convert -t s2tw "鼠标和打印机"          # 转台湾正体
    hanshift convert -i README.md -o README.zh-TW.md
    hanshift convert -i docs/ -r --in-place         # 目录批量原地转换
    hanshift detect "軟體工程師"
    hanshift lookup 发
    cat a.txt | hanshift convert -t t2s
"""

import argparse
import json
import os
import sys

from . import __version__
from .core import Converter, get_converter
from .detect import detect_detail

#: 目录批量处理时的默认扩展名
DEFAULT_EXTS = (".txt", ".md", ".rst", ".csv", ".json", ".yaml", ".yml", ".html")


def _read_text(path):
    with open(path, "r", encoding="utf-8-sig", errors="replace") as handle:
        return handle.read()


def _write_text(path, text):
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _iter_files(root, recursive, exts):
    if recursive:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames.sort()
            for name in sorted(filenames):
                if name.lower().endswith(exts):
                    yield os.path.join(dirpath, name)
    else:
        for name in sorted(os.listdir(root)):
            full = os.path.join(root, name)
            if os.path.isfile(full) and name.lower().endswith(exts):
                yield full


def cmd_convert(args):
    """执行转换命令。"""
    converter = get_converter(args.target)

    # 1) 目录批量模式
    if args.input and os.path.isdir(args.input):
        exts = tuple(e.strip().lower() for e in args.ext.split(",") if e.strip())
        exts = exts or DEFAULT_EXTS
        if not args.in_place and not args.output:
            print("错误：目录批量转换需指定 --in-place 或 --output", file=sys.stderr)
            return 2
        files = list(_iter_files(args.input, args.recursive, exts))
        if not files:
            print("未找到匹配的文件（扩展名: %s）" % ", ".join(exts))
            return 0
        summary = []
        for path in files:
            original = _read_text(path)
            converted, stats = converter.convert_with_stats(original)
            if args.dry_run:
                summary.append({"file": path, "changed_chars": stats["changed_chars"]})
                continue
            if args.in_place:
                target = path
            else:
                rel = os.path.relpath(path, args.input)
                target = os.path.join(args.output, rel)
            _write_text(target, converted)
            summary.append(
                {
                    "file": path,
                    "output": target,
                    "changed_chars": stats["changed_chars"],
                }
            )
        if args.format == "json":
            print(json.dumps({"mode": args.target, "files": summary}, ensure_ascii=False, indent=2))
        else:
            print("已处理 %d 个文件（模式: %s）" % (len(summary), args.target))
            for item in summary:
                if args.dry_run:
                    print("  [预览] %s  变更字符 %d" % (item["file"], item["changed_chars"]))
                else:
                    print("  %s -> %s" % (item["file"], item["output"]))
        return 0

    # 2) 单文件或直接文本模式
    if args.input:
        text = _read_text(args.input)
    elif args.text:
        text = args.text
    else:
        # 从标准输入读取，支持管道
        text = sys.stdin.read()

    converted, stats = converter.convert_with_stats(text)

    if args.output:
        _write_text(args.output, converted)
        if args.format == "json":
            print(json.dumps(stats, ensure_ascii=False))
        else:
            print("已写入: %s" % args.output)
        return 0

    if args.format == "json":
        print(json.dumps({"result": converted, "stats": stats}, ensure_ascii=False, indent=2))
    else:
        print(converted)
        if args.stats:
            print(
                "\n[统计] 模式=%s 原文%d字符 变更%d字符"
                % (stats["mode"], stats["source_length"], stats["changed_chars"]),
                file=sys.stderr,
            )
    return 0


def cmd_detect(args):
    """执行检测命令。"""
    if args.input:
        text = _read_text(args.input)
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()
    info = detect_detail(text)
    if args.format == "json":
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        label_map = {
            "simplified": "简体",
            "traditional": "繁体",
            "mixed": "简繁混排",
            "neutral": "无明显特征",
        }
        print("判定: %s（置信度 %.2f）" % (label_map[info["label"]], info["confidence"]))
        print(
            "简体特征字 %d 个，繁体特征字 %d 个，总长度 %d"
            % (info["simplified_marks"], info["traditional_marks"], info["length"])
        )
    return 0


def cmd_lookup(args):
    """查询某个字的候选字形。"""
    from .core import candidates

    rows = []
    for char in args.chars:
        rows.append({"char": char, "candidates": candidates(char)})
    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            cands = row["candidates"]
            print("%s -> %s" % (row["char"], " ".join(cands) if cands else "(无差异)"))
    return 0


def cmd_modes(args):
    """列出所有支持的转换模式。"""
    descriptions = {
        "s2t": "简体 -> 繁体（仅字形）",
        "t2s": "繁体 -> 简体（仅字形）",
        "s2tw": "简体 -> 台湾正体（字形 + 台湾用语）",
        "s2twp": "同 s2tw（别名）",
        "s2hk": "简体 -> 香港繁体（字形 + 香港用语）",
        "tw2s": "台湾正体 -> 简体（用语 + 字形）",
        "hk2s": "香港繁体 -> 简体（用语 + 字形）",
    }
    if args.format == "json":
        print(json.dumps(descriptions, ensure_ascii=False, indent=2))
    else:
        for mode in Converter.MODES:
            print("  %-6s %s" % (mode, descriptions[mode]))
    return 0


def build_parser():
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(
        prog="hanshift",
        description="HanShift — 零依赖、离线优先的简繁中文转换引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            '  hanshift convert "我的头发很长"\n'
            '  hanshift convert -t s2tw "鼠标和打印机"\n'
            "  hanshift convert -i README.md -o README.zh-TW.md\n"
            "  hanshift convert -i docs/ -r --in-place\n"
            '  hanshift detect "軟體工程師"\n'
            "  hanshift lookup 发\n"
        ),
    )
    parser.add_argument("--version", action="version", version="HanShift %s" % __version__)
    subparsers = parser.add_subparsers(dest="command")

    # convert
    p_convert = subparsers.add_parser("convert", help="转换文本或文件", aliases=["c"])
    p_convert.add_argument("text", nargs="?", help="待转换的文本（省略则从标准输入读取）")
    p_convert.add_argument("-t", "--target", default="s2t", help="转换模式，默认 s2t")
    p_convert.add_argument("-i", "--input", help="输入文件或目录")
    p_convert.add_argument("-o", "--output", help="输出文件或目录")
    p_convert.add_argument("--in-place", action="store_true", help="原地覆盖写入")
    p_convert.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
    p_convert.add_argument("--ext", default="", help="目录模式下的扩展名过滤，逗号分隔")
    p_convert.add_argument("--dry-run", action="store_true", help="只预览不写入")
    p_convert.add_argument("--stats", action="store_true", help="输出转换统计")
    p_convert.add_argument("--format", choices=["text", "json"], default="text")
    p_convert.set_defaults(func=cmd_convert)

    # detect
    p_detect = subparsers.add_parser("detect", help="检测文本是简体还是繁体", aliases=["d"])
    p_detect.add_argument("text", nargs="?", help="待检测文本（省略则从标准输入读取）")
    p_detect.add_argument("-i", "--input", help="输入文件")
    p_detect.add_argument("--format", choices=["text", "json"], default="text")
    p_detect.set_defaults(func=cmd_detect)

    # lookup
    p_lookup = subparsers.add_parser("lookup", help="查询字的候选字形", aliases=["l"])
    p_lookup.add_argument("chars", nargs="+", help="待查询的汉字")
    p_lookup.add_argument("--format", choices=["text", "json"], default="text")
    p_lookup.set_defaults(func=cmd_lookup)

    # modes
    p_modes = subparsers.add_parser("modes", help="列出所有转换模式", aliases=["m"])
    p_modes.add_argument("--format", choices=["text", "json"], default="text")
    p_modes.set_defaults(func=cmd_modes)

    return parser


def main(argv=None):
    """命令行入口。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except ValueError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
