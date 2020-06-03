import execfile
import logging

import argparse

parser = argparse.ArgumentParser(
    prog="byterun",
    description="Run Python programs with a Python bytecode interpreter.",
)
parser.add_argument(
    '-m', dest='module', action='store_true',
    help="prog is a module name, not a file name.",
)

args = parser.parse_args()

if args.module:
    run_fn = execfile.run_python_module
else:
    run_fn = execfile.run_python_file

level = logging.DEBUG if args.verbose else logging.WARNING
logging.basicConfig(level=level)

argv = [args.prog] + args.args
run_fn(args.prog, argv)
