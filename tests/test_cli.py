"""命令行端到端测试。"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run_cli(*args):
    """以子进程方式调用 CLI，返回 (返回码, 标准输出, 标准错误)。"""
    env = dict(os.environ)
    env["PYTHONPATH"] = ROOT
    proc = subprocess.run(
        [sys.executable, "-m", "hanshift", *args],
        capture_output=True, text=True, env=env, cwd=ROOT,
    )
    return proc.returncode, proc.stdout, proc.stderr


class TestCliConvert(unittest.TestCase):
    def test_convert_text(self):
        code, out, _ = run_cli("convert", "我的头发很长")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "我的頭髮很長")

    def test_convert_mode(self):
        code, out, _ = run_cli("convert", "-t", "s2tw", "鼠标和打印机")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "滑鼠和印表機")

    def test_convert_json(self):
        code, out, _ = run_cli("convert", "--format", "json", "中华人民共和国")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["result"], "中華人民共和國")
        self.assertIn("stats", payload)

    def test_invalid_mode(self):
        code, _, err = run_cli("convert", "-t", "bad-mode", "测试")
        self.assertEqual(code, 2)
        self.assertIn("错误", err)

    def test_file_in_out(self):
        tmp = tempfile.mkdtemp()
        try:
            src = os.path.join(tmp, "a.txt")
            dst = os.path.join(tmp, "b.txt")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write("房间里有一只猫")
            code, out, _ = run_cli("convert", "-i", src, "-o", dst)
            self.assertEqual(code, 0)
            with open(dst, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "房間裏有一隻貓")
        finally:
            shutil.rmtree(tmp)

    def test_directory_in_place(self):
        tmp = tempfile.mkdtemp()
        try:
            src = os.path.join(tmp, "doc.md")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write("软件工程师")
            code, _, _ = run_cli("convert", "-i", tmp, "--in-place")
            self.assertEqual(code, 0)
            with open(src, encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "軟件工程師")
        finally:
            shutil.rmtree(tmp)


class TestCliOtherCommands(unittest.TestCase):
    def test_detect(self):
        code, out, _ = run_cli("detect", "中華人民共和國")
        self.assertEqual(code, 0)
        self.assertIn("繁体", out)

    def test_lookup(self):
        code, out, _ = run_cli("lookup", "发")
        self.assertEqual(code, 0)
        self.assertIn("發", out)
        self.assertIn("髮", out)

    def test_modes(self):
        code, out, _ = run_cli("modes")
        self.assertEqual(code, 0)
        for mode in ("s2t", "t2s", "s2tw", "s2hk", "tw2s", "hk2s"):
            self.assertIn(mode, out)

    def test_version(self):
        code, out, _ = run_cli("--version")
        self.assertEqual(code, 0)
        self.assertIn("HanShift", out)


if __name__ == "__main__":
    unittest.main()
