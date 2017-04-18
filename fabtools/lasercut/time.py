import ezdxf
import logging
import numpy as np
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

    path_length = 0
    for element in modelspace:
        if element.dxftype() == 'LINE':
            path_length += np.linalg.norm([element.dxf.start, element.dxf.end])