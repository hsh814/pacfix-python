import os
import sys
import argparse
from contextlib import closing
from functools import partial

from . import __version__
from . import invariant
from . import synthesis
from . import utils


def run(args: argparse.Namespace):
    input_dir = args.input_dir
    pac_delta = args.pac_delta
    output = args.output
    # create initial hypothesis space
    with closing(args.live_vars):
        live_vars = utils.get_live_vars(args.live_vars)
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
    pac_epsilon = utils.calculate_pac(samples, len(hypothesis_space), pac_delta)
    output.write(f"[metadata] [pac] [delta {pac_delta}] [eps {pac_epsilon}]\n")
    pac_epsilon_no_uniq = utils.calculate_pac(non_uniq_samples, len(hypothesis_space), pac_delta)
    output.write(f"[metadata] [pac-no-uniq] [delta {pac_delta}] [eps {pac_epsilon_no_uniq}]\n")
    output.write("[final] --------------\n")
    inv_manager = invariant.InvariantManager(live_vars)
    inv_manager.reduce()
    for inv in refined_space:
        inv_manager.add_invariant(inv)
    inv_manager.dump(output, args.output_smt)


def run_uni(args: argparse.Namespace):
    input_dir = args.input_dir
    pac_delta = args.pac_delta
    output = args.output
    # create initial hypothesis space
    with closing(args.live_vars):
        live_vars = utils.get_live_vars(args.live_vars)
    if args.lv_file is not None:
        with closing(args.lv_file):
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
    inv_manager = invariant.InvariantManager(live_vars)
    inv_manager.reduce()
    for inv in refined_space:
        inv_manager.add_invariant(inv)
    inv_manager.dump(output, "")


def directory(path: str, read: bool) -> str:
    if not os.path.isdir(path):
        if read:
            raise argparse.ArgumentTypeError(f"{path} is not a directory")
        try:
            os.mkdir(path)
        except Exception as e:
            raise argparse.ArgumentTypeError(f"mkdir: {e}")
    return path


def main():
    arg_parser = argparse.ArgumentParser(prog="pacfix")
    arg_parser.add_argument('-v', '--version', action='version',
                            version=f'%(prog)s {__version__}')
    arg_subparsers = arg_parser.add_subparsers(dest="mode", required=True)
    arg_parser_base = argparse.ArgumentParser(add_help=False)
    arg_parser_base.add_argument("-i", "--input-dir", metavar="DIR",
        help="Input directory",
        type=partial(directory, read=True), required=True)
    arg_parser_base.add_argument("-l", "--live-vars", metavar="FILE",
        help="Live variables", type=argparse.FileType('r'), required=True)
    arg_parser_base.add_argument("-D", "--pac-delta", metavar="NUMBER",
        help="delta value for pac learning", type=float, default=0.01)
    arg_parser_base.add_argument("-o", "--output", metavar="FILE",
        help="Output file", type=argparse.FileType('w'), default=sys.stdout)
    arg_parser_run = arg_subparsers.add_parser('run',
        parents=[arg_parser_base])
    arg_parser_run.add_argument("-s", "--output-smt", metavar="DIR",
        help="Output directory for smt files",
        type=partial(directory, read=False))
    arg_parser_uni = arg_subparsers.add_parser('uni',
        parents=[arg_parser_base])
    arg_parser_uni.add_argument("-f", "--lv-file", metavar="FILE",
        help="Live variables file those are actually used",
        type=argparse.FileType('r'))
    args = arg_parser.parse_args()
    if args.mode == "run":
        with closing(args.output):
            run(args)
    elif args.mode == "uni":
        with closing(args.output):
            run_uni(args)


if __name__ == "__main__":
    main()
