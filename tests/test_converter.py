"""转换正确性测试：覆盖单字映射、歧义消歧、地区用语三个层次。"""

import unittest

from hanshift import Converter, convert


class TestBasicConversion(unittest.TestCase):
    """基础字形转换。"""

    def test_simplified_to_traditional(self):
        self.assertEqual(convert("中华人民共和国", "s2t"), "中華人民共和國")
        self.assertEqual(convert("软件工程师", "s2t"), "軟件工程師")
        self.assertEqual(convert("学习历史和地理", "s2t"), "學習歷史和地理")

    def test_traditional_to_simplified(self):
        self.assertEqual(convert("中華人民共和國", "t2s"), "中华人民共和国")
        # t2s 仅做字形转换，「軟體」按字形还原为「软体」（用词转换请用 tw2s）
        self.assertEqual(convert("軟體工程師", "t2s"), "软体工程师")
        self.assertEqual(convert("我的頭髮很長", "t2s"), "我的头发很长")

    def test_empty_and_plain_text(self):
        self.assertEqual(convert("", "s2t"), "")
        self.assertEqual(convert("Hello, world! 123", "s2t"), "Hello, world! 123")
        self.assertEqual(convert("标点符号，。！？", "s2t"), "標點符號，。！？")

    def test_ascii_unchanged(self):
        text = "Python 3.11 is great"
        self.assertEqual(convert(text, "s2t"), text)


class TestAmbiguityResolution(unittest.TestCase):
    """一对多歧义消解——本项目最核心的差异化能力。"""

    CASES = [
        # 发：發 / 髮
        ("我的头发很长", "我的頭髮很長"),
        ("经济发展迅速", "經濟發展迅速"),
        ("理发店开张了", "理髮店開張了"),
        # 干：乾 / 幹
        ("这是一个干燥的饼干", "這是一個乾燥的餅乾"),
        ("他干活很卖力", "他幹活很賣力"),
        ("公司和干部", "公司和幹部"),
        # 只：只 / 隻
        ("房间里有一只猫", "房間裏有一隻貓"),
        ("这只是开始", "這只是開始"),
        ("5只猫", "5隻貓"),
        # 面：面 / 麵
        ("我喜欢吃面条", "我喜歡吃麵條"),
        ("不要逃避面对问题", "不要逃避面對問題"),
        # 历：歷 / 曆
        ("学习历史", "學習歷史"),
        ("查看日历", "查看日曆"),
        # 制：制 / 製
        ("制造复杂机器", "製造複雜機器"),
        ("制度需要完善", "制度需要完善"),
        # 系：系 / 係 / 繫
        ("操作系统启动", "操作系統啟動"),
        ("保持密切联系", "保持密切聯繫"),
        # 台：台 / 臺 / 檯 / 颱
        ("台湾是个好地方", "台灣是個好地方"),
        ("演员走上舞台", "演員走上舞臺"),
        ("台风即将登陆", "颱風即將登陸"),
        # 表：表 / 錶
        ("买了一块手表", "買了一塊手錶"),
        ("填写表格", "填寫表格"),
        # 板：板 / 闆
        ("老板很和气", "老闆很和氣"),
        ("木板很结实", "木板很結實"),
        # 征：征 / 徵
        ("象征和平", "象徵和平"),
        ("红军长征", "紅軍長征"),
        # 谷：谷 / 穀
        ("收割稻谷", "收割稻穀"),
        ("走进山谷", "走進山谷"),
        # 松：松 / 鬆
        ("放松心情", "放鬆心情"),
        ("山上有很多松树", "山上有很多松樹"),
        # 脏：髒 / 臟
        ("心脏很重要", "心臟很重要"),
        ("衣服很脏", "衣服很髒"),
        # 了：了 / 瞭
        ("他来了", "他來了"),
        ("我了解情况", "我瞭解情況"),
        # 斗：斗 / 鬥
        ("北斗七星", "北斗七星"),
        ("为理想而奋斗", "為理想而奮鬥"),
        # 尽：盡 / 儘
        ("尽力而为", "盡力而為"),
        ("尽管下雨", "儘管下雨"),
        # 合并：並 / 併
        ("两家公司合并", "兩家公司合併"),
        ("并且非常优秀", "並且非常優秀"),
        # 采：采 / 採
        ("采用新技术", "採用新技術"),
        ("文采飞扬", "文采飛揚"),
        # 丑：丑 / 醜
        ("小丑表演", "小丑表演"),
        ("丑陋的行为", "醜陋的行為"),
        # 曲：曲 / 麴
        ("歌曲很动听", "歌曲很動聽"),
        # 家：家 / 傢
        ("回家吃饭", "回家吃飯"),
        ("购买新家具", "購買新傢俱"),
    ]

    def test_s2t_ambiguity(self):
        for source, expected in self.CASES:
            with self.subTest(source=source):
                self.assertEqual(convert(source, "s2t"), expected)

    def test_t2s_reverse(self):
        """繁转简时，上述歧义词应能正确还原。"""
        for simplified, traditional in self.CASES:
            with self.subTest(traditional=traditional):
                self.assertEqual(convert(traditional, "t2s"), simplified)


class TestRegionalVariants(unittest.TestCase):
    """地区用语差异。"""

    def test_taiwan_variants(self):
        self.assertEqual(convert("鼠标和打印机", "s2tw"), "滑鼠和印表機")
        self.assertEqual(convert("软件工程师", "s2tw"), "軟體工程師")
        self.assertEqual(convert("网络信息", "s2tw"), "網路資訊")

    def test_hongkong_variants(self):
        self.assertEqual(convert("软件工程师", "s2hk"), "軟件工程師")
        self.assertEqual(convert("出租车", "s2hk"), "的士")

    def test_tw2s(self):
        self.assertEqual(convert("滑鼠和印表機", "tw2s"), "鼠标和打印机")
        self.assertEqual(convert("軟體工程師在網路上查閱資訊", "tw2s"), "软件工程师在网络上查阅信息")

    def test_hk2s(self):
        self.assertEqual(convert("軟件工程師", "hk2s"), "软件工程师")

    def test_s2twp_alias(self):
        self.assertEqual(convert("鼠标", "s2twp"), convert("鼠标", "s2tw"))

    def test_pure_s2t_keeps_mainland_words(self):
        """纯字形模式不应改动地区用词。"""
        self.assertEqual(convert("软件", "s2t"), "軟件")


class TestConverterObject(unittest.TestCase):
    """转换器对象与统计能力。"""

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            Converter("no-such-mode")

    def test_all_modes_available(self):
        for mode in Converter.MODES:
            Converter(mode)

    def test_stats(self):
        converter = Converter("s2t")
        _, stats = converter.convert_with_stats("中华人民共和国")
        self.assertEqual(stats["mode"], "s2t")
        self.assertEqual(stats["source_length"], 7)
        self.assertGreater(stats["changed_chars"], 0)

    def test_idempotent_for_traditional_input(self):
        """已是繁体的文本再次转繁体应保持稳定。"""
        once = convert("中华人民共和国", "s2t")
        twice = convert(once, "s2t")
        self.assertEqual(once, twice)


class TestRoundTrip(unittest.TestCase):
    """往返一致性：简 -> 繁 -> 简 应能回到原文。"""

    SAMPLES = [
        "中华人民共和国",
        "我的头发很长，需要理发了",
        "他干活很卖力，是个能干的干部",
        "房间里有一只猫和两只狗",
        "我喜欢吃面条，也喜欢面包",
        "制造复杂机器的制度",
        "象征胜利的征程",
        "心脏和内脏都很健康",
        "老板在胡同口买了生姜",
        "伙伴们放松一下再干活",
        "折叠纸抽签决定顺序",
        "秋千架上挂着胡须造型的装饰",
        "防御寒冷抵御敌人",
        "了解情况后才能尽力而为",
        "北斗七星出现在夜空",
        "收获的季节到了",
    ]

    def test_roundtrip_stability(self):
        for sample in self.SAMPLES:
            with self.subTest(sample=sample):
                traditional = convert(sample, "s2t")
                back = convert(traditional, "s2t")
                self.assertEqual(traditional, back, "繁体再转繁体应稳定")

    def test_roundtrip_to_simplified(self):
        """简 -> 繁 -> 简，常用词应回到原文。"""
        for sample in self.SAMPLES:
            with self.subTest(sample=sample):
                traditional = convert(sample, "s2t")
                back = convert(traditional, "t2s")
                self.assertEqual(sample, back)


if __name__ == "__main__":
    unittest.main()
