import unittest
import os
import pacfix

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")


class TestLV(unittest.TestCase):
    def test_lv(self):
        lv_file = os.path.join(EXAMPLES_DIR, "example01", "live-variables.txt")
        with open(lv_file, "r") as f:
            live_vars = pacfix.utils.get_live_vars(f)
        self.assertEqual(len(live_vars), 5)
        self.assertSetEqual(set([lv.name for lv in live_vars.values()]), {"x", "y", "z", "b", "c"})
