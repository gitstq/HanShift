#!/usr/bin/env bash
# HanShift 功能演示脚本：一次跑通所有典型用法。
set -euo pipefail

cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"

run() {
    echo "$ $*"
    PYTHONPATH=. "$PYTHON" -m hanshift "$@"
    echo ""
}

echo "========== HanShift 功能演示 =========="
echo ""

run convert "我的头发很长"
run convert -t s2tw "鼠标和打印机"
run convert -t s2hk "软件工程师坐出租车"
run convert -t t2s "軟體工程師在電腦上編寫程式碼"
run convert -t tw2s "滑鼠和印表機"
run detect "中華人民共和國"
run lookup 发 干 只
run modes
