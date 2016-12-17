import ezdxf
import logging
from argparse import ArgumentParser


def main(args):
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="DXF you want to compute the time for.")
    parser.add_argument("-v", type=float, help="Linear velocity")
    parsed = parser.parse_args(args)

    dwg = ezdxf.readfile(parsed.filename)
    modelspace = dwg.modelspace()
