#!/usr/bin/env python3
from argparse import ArgumentParser, REMAINDER
import importlib

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("toolbox", type=str, help="Choose the toolbox you need.")
    parser.add_argument("command", type=str, help="Choose the tool from the toolbox.")
    parser.add_argument('args', nargs=REMAINDER)
    args = parser.parse_args()

    module = importlib.import_module("fabtools.{}.{}".format(args.toolbox, args.command))
    if hasattr(module, "main"):
        main_function = getattr(module, "main")
        main_function(args.args)
