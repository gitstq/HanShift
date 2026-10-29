"""简繁体检测测试。"""

import unittest

from hanshift.detect import detect, detect_detail


class TestDetect(unittest.TestCase):
    def test_simplified(self):
        label, confidence = detect("中华人民共和国是一个伟大的国家")
        self.assertEqual(label, "simplified")
        self.assertGreater(confidence, 0.9)

    def test_traditional(self):
        label, confidence = detect("中華人民共和國是一個偉大的國家")
        self.assertEqual(label, "traditional")
        self.assertGreater(confidence, 0.9)

    def test_mixed(self):
        label, _ = detect("这是简体字和繁體字混排的句子")
        self.assertEqual(label, "mixed")

    def test_neutral(self):
        label, confidence = detect("Hello, world! 123")
        self.assertEqual(label, "neutral")
        self.assertEqual(confidence, 0.0)

    def test_empty(self):
        label, confidence = detect("")
        self.assertEqual(label, "neutral")
        self.assertEqual(confidence, 0.0)

    def test_detail_fields(self):
        info = detect_detail("中华人民共和国")
        self.assertIn("label", info)
        self.assertIn("confidence", info)
        self.assertIn("simplified_marks", info)
        self.assertIn("traditional_marks", info)
        self.assertGreater(info["simplified_marks"], 0)
        self.assertEqual(info["traditional_marks"], 0)


if __name__ == "__main__":
    unittest.main()
