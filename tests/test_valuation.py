import unittest
import os
import pacfix

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")


class TestValuation(unittest.TestCase):
    def test_val01(self):
        val_dir = os.path.join(EXAMPLES_DIR, "example01", "mem")
        val_raw_neg = pacfix.utils.get_valuations(os.path.join(val_dir, "neg"))
        val_raw_pos = pacfix.utils.get_valuations(os.path.join(val_dir, "pos"))
        vals_neg, vals_pos = pacfix.utils.parse_valuation(val_raw_neg, val_raw_pos)
        self.assertEqual(len(val_raw_neg), 4)
        self.assertEqual(len(val_raw_pos), 16)
        self.assertEqual(len(vals_neg), 4)
        vals_neg_final = pacfix.utils.filter_duplicate(vals_neg)
        self.assertEqual(len(vals_neg_final), 3)
