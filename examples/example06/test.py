import pacfix
import pacfix.utils
from pacfix.invariant import Invariant, InvariantType
import argparse
import pysmt.shortcuts as smt

def main():
    live_var_file = "live-variables.txt"
    with open(live_var_file, "r") as f:
        live_vars = pacfix.utils.get_live_vars(f)
    inv =  Invariant(InvariantType.LE, Invariant(InvariantType.VAR, data=1), Invariant(InvariantType.VAR, data=2)) # x <= y
    inv2 = Invariant(InvariantType.LE, Invariant(InvariantType.VAR, data=1), Invariant(InvariantType.CONST, data=3)) # x <= 3
    inv3 = Invariant(InvariantType.AND, inv, inv2)
    smt_inv = inv3.convert_to_smt(live_vars)
    smt.write_smtlib(smt_inv, "out.smt2")


if __name__ == "__main__":
    main()
