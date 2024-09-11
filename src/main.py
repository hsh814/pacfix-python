#!/usr/bin/env python3
import os
import sys
import argparse
import math

import synthesis
import utils

from typing import List, Set, Dict, Tuple

def run(argv: List[str]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input-dir", "-i", help="Input directory", required=True)
    argparser.add_argument("--live-vars", "-l", help="Live variables", required=True)
    argparser.add_argument("--output", "-o", help="Output file", required=False, default="")
    argparser.add_argument("--pac-delta", "-d", help="delta value for pac learning", required=False, default=0.01)
    args = argparser.parse_args(argv)
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
    pos_vals_raw = utils.get_valuations(os.path.join(input_dir, "pos"))
    neg_vals_init, pos_vals_init = utils.parse_valuation(neg_vals_raw, pos_vals_raw)
    initial_neg = len(neg_vals_init)
    initial_pos = len(pos_vals_init)
    neg_vals = utils.filter_duplicate(neg_vals_init)
    pos_vals = utils.filter_duplicate(pos_vals_init)
    refined_space = synthesizer.validate(hypothesis_space, neg_vals, pos_vals)
    # write output
    int_vars = 0
    for v in live_vars.values():
        if v.var_type == utils.VarType.INT:
            int_vars += 1
    output.write(f"[metadata] [live-variables] [total {len(live_vars)}] [int {int_vars}]\n")
    output.write(f"[metadata] [hypothesis-space] [original {original_size}] [final {len(refined_space)}]\n")
    samples = len(neg_vals) + len(pos_vals)
    non_uniq_samples = initial_neg + initial_pos
    output.write(f"[metadata] [valuation] [neg {len(neg_vals)}] [pos {len(pos_vals)}] [uniq {samples}] [init-neg {initial_neg}] [init-pos {initial_pos}] [non-uniq {non_uniq_samples}]\n")
    pac_epsilon = utils.calculate_pac(samples, len(refined_space), pac_delta)
    output.write(f"[metadata] [pac] [delta {pac_delta}] [eps {pac_epsilon}]\n")
    pac_epsilon_no_uniq = utils.calculate_pac(non_uniq_samples, len(refined_space), pac_delta)
    output.write(f"[metadata] [pac-no-uniq] [delta {pac_delta}] [eps {pac_epsilon_no_uniq}]\n")
    output.write("[final] --------------\n")
    for inv in refined_space:
        output.write(f"[invariant] [expr {inv.to_str(live_vars)}]\n")

def run_uni(argv: List[str]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input-dir", "-i", help="Input directory", required=True)
    argparser.add_argument("--live-vars", "-l", help="Live variables", required=True)
    argparser.add_argument("--lv-file", "-f", help="Live variables file those are actually used", required=False, default="")
    argparser.add_argument("--output", "-o", help="Output file", required=False, default="")
    argparser.add_argument("--pac-delta", "-d", help="delta value for pac learning", required=False, default=0.01)
    args = argparser.parse_args(argv)
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
    if args.lv_file != "":
        used_lvs = utils.get_lv_file(args.lv_file)
        live_vars = {k: v for k, v in live_vars.items() if v.name in used_lvs}
    synthesizer = synthesis.Synthesizer(live_vars)
    hypothesis_space = synthesizer.synthesize()
    original_size = len(hypothesis_space)
    # validate hypothesis space
    neg_vals_raw = utils.get_valuations(os.path.join(input_dir, "neg"))
    pos_vals_raw = utils.get_valuations(os.path.join(input_dir, "pos"))
    neg_vals_init, pos_vals_init = utils.parse_valuations_uni([], neg_vals_raw + pos_vals_raw)
    initial_neg = len(neg_vals_init)
    initial_pos = len(pos_vals_init)
    neg_vals = utils.filter_duplicate(neg_vals_init)
    pos_vals = utils.filter_duplicate(pos_vals_init)
    refined_space = synthesizer.validate(hypothesis_space, neg_vals, pos_vals)
    # write output
    int_vars = 0
    for v in live_vars.values():
        if v.var_type == utils.VarType.INT:
            int_vars += 1
    output.write(f"[metadata] [live-variables] [total {len(live_vars)}] [int {int_vars}]\n")
    output.write(f"[metadata] [hypothesis-space] [original {original_size}] [final {len(refined_space)}]\n")
    samples = len(neg_vals) + len(pos_vals)
    non_uniq_samples = initial_neg + initial_pos
    output.write(f"[metadata] [valuation] [neg {len(neg_vals)}] [pos {len(pos_vals)}] [uniq {samples}] [init-neg {initial_neg}] [init-pos {initial_pos}] [non-uniq {non_uniq_samples}]\n")
    pac_epsilon = utils.calculate_pac(samples, len(refined_space), pac_delta)
    output.write(f"[metadata] [pac] [delta {pac_delta}] [eps {pac_epsilon}]\n")
    pac_epsilon_no_uniq = utils.calculate_pac(non_uniq_samples, len(refined_space), pac_delta)
    output.write(f"[metadata] [pac-no-uniq] [delta {pac_delta}] [eps {pac_epsilon_no_uniq}]\n")
    output.write("[final] --------------\n")
    for inv in refined_space:
        output.write(f"[invariant] [expr {inv.to_str(live_vars)}]\n")

def main(argv: List[str]):
    if len(argv) < 2:
        print("Usage: python main.py run -i <input_dir> -l <live_vars> -o <output_file>")
        print("Usage: python main.py uni -i <input_dir> -l <live_vars> -o <output_file>")
        sys.exit(1)
    mode = argv[1]
    modes = ["run", "uni"]
    if mode not in modes:
        print(f"Error: mode must be one of {modes}")
        sys.exit(1)
    if mode == "run":
        run(argv[2:])
    elif mode == "uni":
        run_uni(argv[2:])
        

if __name__ == "__main__":
    main(sys.argv)