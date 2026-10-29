#!/usr/bin/env bash
# HanShift 一键构建脚本：测试 -> 构建 sdist/wheel -> 产物校验。
# 跨平台：Linux / macOS 可直接执行；Windows 可用 Git Bash 或 WSL 运行。
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"
DIST_DIR="dist"

echo "==> [1/4] 清理历史构建产物"
rm -rf build "$DIST_DIR" ./*.egg-info

echo "==> [2/4] 运行单元测试"
"$PYTHON" -m unittest discover -s tests 2>&1 | tail -5

echo "==> [3/4] 构建发行包"
if "$PYTHON" -m pip --version >/dev/null 2>&1; then
    "$PYTHON" -m pip install --quiet --upgrade build 2>/dev/null || true
fi
if "$PYTHON" -m build --help >/dev/null 2>&1; then
    "$PYTHON" -m build --sdist --wheel --outdir "$DIST_DIR"
else
    echo "    未检测到 build 模块，回退到 setup.py 方式"
    "$PYTHON" setup.py sdist bdist_wheel --dist-dir "$DIST_DIR" 2>/dev/null || \
        "$PYTHON" -m pip wheel . --no-deps -w "$DIST_DIR"
fi

echo "==> [4/4] 校验产物"
if [ -d "$DIST_DIR" ]; then
    ls -lh "$DIST_DIR"
    echo ""
    echo "构建完成，产物位于 $DIST_DIR/"
else
    echo "警告：未生成构建产物" >&2
    exit 1
fi
