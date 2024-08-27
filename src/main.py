#!/usr/bin/env python3
import os
import sys
import argparse
import math

import synthesis
import utils

from typing import List, Set, Dict, Tuple

def main(argv: List[str]):
    if len(argv) < 2:
        print("Usage: python main.py run -i <input_dir> -l <live_vars> -o <output_dir>")
        sys.exit(1)
    mode = argv[1]
    if mode not in ["run"]:
        print("Error: mode must be one of [run]")
        sys.exit(1)
    if mode == "run":
        argparser = argparse.ArgumentParser()
        argparser.add_argument("--input-dir", "-i", help="Input directory", required=True)
        argparser.add_argument("--live-vars", "-l", help="Live variables", required=True)
        argparser.add_argument("--output", "-o", help="Output file", required=False, default="")
        argparser.add_argument("--pac-delta", "-e", help="delta value for pac learning", required=False, default=0.01)
        args = argparser.parse_args(argv[2:])
        input_dir = args.input_dir
        live_vars_file = args.live_vars
        output_file = args.output
        pac_delta = float(args.pac_delta)
        output = sys.stdout
        if output_file:
            output = open(output_file, "w")
        paths = [input_dir, live_vars_file]
        for path in paths:
            if not os.path.exists(path):
                print(f"Error: file {input_dir} not found!")
                sys.exit(1)
        # create initial hypothesis space
        live_vars = utils.get_live_vars(live_vars_file)
        synthesizer = synthesis.Synthesizer(live_vars)
        hypothesis_space = synthesizer.synthesize()
        original_size = len(hypothesis_space)
        # validate hypothesis space
        neg_vals_raw = utils.get_valuations(os.path.join(input_dir, "neg"))
        neg_vals = utils.parse_valuation(neg_vals_raw)
        pos_vals_raw = utils.get_valuations(os.path.join(input_dir, "pos"))
        pos_vals = utils.parse_valuation(pos_vals_raw)
        hypothesis_space = synthesizer.validate(hypothesis_space, neg_vals, pos_vals)
        # write output
        int_vars = 0
        for v in live_vars.values():
            if v.var_type == utils.VarType.INT:
                int_vars += 1
        output.write(f"[metadata] [live-variables] [total {len(live_vars)}] [int {int_vars}]\n")
        output.write(f"[metadata] [hypothesis-space] [original {original_size}] [final {len(hypothesis_space)}]\n")
        samples = len(neg_vals) + len(pos_vals)
        non_uniq_samples = len(neg_vals) + len(pos_vals)
        output.write(f"[metadata] [valuation] [neg {len(neg_vals)}] [pos {len(pos_vals)}] [uniq {samples}] [non-uniq {non_uniq_samples}]\n")
        pac_epsilon = (1 / samples) * (math.log(len(hypothesis_space)) + (math.log(1 / pac_delta)))
        output.write(f"[metadata] [pac] [delta {pac_delta}] [eps {pac_epsilon}]\n")
        output.write(f"[metadata] [pac-no-uniq] [delta {pac_delta}] [eps {pac_epsilon}]\n")
        output.write("[final] --------------\n")
        for inv in hypothesis_space:
            output.write(f"[invariant] [expr {inv.to_str(live_vars)}]\n")
        

if __name__ == "__main__":
    main(sys.argv)