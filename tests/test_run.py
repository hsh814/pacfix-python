import unittest
import os
import pacfix
import pysmt.shortcuts as smt

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")


class TestRun(unittest.TestCase):
    def test_run(self):
        val_dir = os.path.join(EXAMPLES_DIR, "example01", "mem")
        val_raw_neg = pacfix.utils.get_valuations(os.path.join(val_dir, "neg"))
        val_raw_pos = pacfix.utils.get_valuations(os.path.join(val_dir, "pos"))
        vals_neg, vals_pos = pacfix.utils.parse_valuation(val_raw_neg, val_raw_pos)
        lv_file = os.path.join(EXAMPLES_DIR, "example01", "live-variables.txt")
        with open(lv_file, "r") as f:
            live_vars = pacfix.utils.get_live_vars(f)
        c_id = 3
        for lv in live_vars.values():
            if lv.name == "c":
                c_id = lv.id
        result = pacfix.learn(live_vars, vals_neg, vals_pos, 0.1)
        expected = smt.Not(smt.Equals(live_vars[c_id].var, smt.Int(0)))
        for inv in result.inv_mgr.invs:
            self.assertEqual(inv.convert_to_smt(live_vars), expected)