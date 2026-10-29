#!/usr/bin/env bash
# HanShift 一键测试脚本：运行完整单元测试套件。
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> 运行单元测试"
python3 -m unittest discover -s tests -v

echo ""
echo "==> 全部测试通过"
