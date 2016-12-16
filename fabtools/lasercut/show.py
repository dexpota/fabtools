from argparse import ArgumentParser
from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import patches
import ezdxf
import os
import math
import logging

def bulge_to_arc(p0, p1, bulge):
    my1 = (p0[1] + p1[1]) / 2.0
    mx1 = (p0[0] + p1[0]) / 2.0
    angle = math.atan(bulge) * 4.0
    angleDeg = math.degrees(angle)

    dist = math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
    sagitta = dist / 2.0 * bulge
    radius = abs(((dist / 2.0) ** 2 + sagitta ** 2) / (2 * sagitta))

    alen = abs(radius * angle)
    theta = 4.0 * math.atan(abs(bulge))
    gamma = (math.pi - theta) / 2.0

    if bulge > 0:
        phi = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) + gamma
    else:
        phi = math.atan2(p1[1] - p0[1], p1[0] - p0[0]) - gamma

    cx = p0[0] + radius * math.cos(phi)
    cy = p0[1] + radius * math.sin(phi)
    startAngle = math.acos((p0[0] - cx) / radius)
    endAngle = startAngle + angle

    return (cx, cy), radius, math.degrees(startAngle), angleDeg

def main(args):
    logger = logging.getLogger(__name__)

    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="DXF file to show you.")
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parsed = parser.parse_args(args)
    dwg = ezdxf.readfile(parsed.filename)
    modelspace = dwg.modelspace()

    rcParams['toolbar'] = 'None'
    if not parsed.debug:
        plt.rc('axes', prop_cycle=(cycler('color', ['black'])))

    for element in modelspace:
        if element.dxftype() == 'LINE':
            start_pnt = element.dxf.start
            end_pnt = element.dxf.end
            plt.plot([start_pnt[0], end_pnt[0]], [start_pnt[1], end_pnt[1]])
        elif element.dxftype() == "LWPOLYLINE":
            with element.points() as points:
                mat_points = []
                for a, b in zip(points, points[1:] + [points[0]]):
                    xa, ya, start_width_a, end_width_a, bulge_a = a
                    xb, yb, start_width_b, end_width_b, bulge_b = b

                    if bulge_a != 0:
                        (cx, cy), radius, startAngle, angleDeg = bulge_to_arc((xa, ya), (xb, yb), bulge_a)

                        if angleDeg < 0:
                            arc = patches.Arc((cx, cy), 2 * radius, 2 * radius, startAngle, angleDeg, 0)
                        else:
                            arc = patches.Arc((cx, cy), 2 * radius, 2 * radius, startAngle, 0, angleDeg)

                        plt.plot(xa, ya, "^g")
                        plt.plot(xb, yb, "^b")
                        plt.gca().add_patch(arc)

                for a, b in zip(points, points[1:]):
                    xa, ya, start_width_a, end_width_a, bulge_a = a
                    xb, yb, start_width_b, end_width_b, bulge_b = b
                    if bulge_a == 0:
                        plt.plot([xa, xb], [ya, yb])

        elif element.dxftype() == "POLYLINE":
            print("POLYLINE")
        else:
            print(element.dxftype())
        # elif element.dxftype() == "REGION":
        #     with element.edit_data() as data:
        #         print(data)

    plt.gcf().canvas.set_window_title(os.path.basename(parsed.filename))
    plt.axis('equal')
    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        left="off",
        right="off",
        labelleft="off",
        bottom='off',  # ticks along the bottom edge are off
        top='off',
        labelbottom='off'
    )
    plt.gcf().set_tight_layout(True)
    plt.show()