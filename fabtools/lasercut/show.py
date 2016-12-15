from argparse import ArgumentParser
from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import patches
import ezdxf
import os
import math


def main(args):
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
            #plt.plot([start_pnt[0], end_pnt[0]], [start_pnt[1], end_pnt[1]])
            print(start_pnt)
            print(end_pnt)
        elif element.dxftype() == "LWPOLYLINE":
            with element.points() as points:
                mat_points = []
                print(points)
                for a, b in zip(points, points[1:] + [points[0]]):
                    xa, ya, start_width_a, end_width_a, bulge_a = a
                    xb, yb, start_width_b, end_width_b, bulge_b = b

                    if bulge_a == 0:
                        #plt.plot([xa, xb], [ya, yb])
                        pass
                    else:
                        p0 = (xa, ya)
                        bulge = bulge_a
                        p1 = (xb, yb)
                        print(p0)
                        print(p1)
                        my1 = (p0[1] + p1[1]) / 2.0
                        mx1 = (p0[0] + p1[0]) / 2.0
                        angle = math.atan(bulge) * 4.0
                        angleDeg = angle * (180.0 / math.pi)

                        dist = math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)
                        sagitta = dist / 2.0 * bulge
                        radius = abs(((dist / 2.0)**2+sagitta**2) / (2*sagitta))

                        alen = abs(radius * angle)
                        theta = 4.0 * math.atan(abs(bulge))
                        gamma = (math.pi - theta) / 2.0

                        if bulge > 0:
                            phi = math.atan2(p1[1] - p0[1], p1[0]-p0[0]) + gamma
                        else:
                            phi = math.atan2(p1[1] - p0[1], p1[0]-p0[0]) - gamma

                        cx = p0[0] + radius*math.cos(phi)
                        cy = p0[1] + radius*math.sin(phi)
                        startAngle = math.acos((p0[0] - cx) / radius)
                        endAngle = startAngle + angle
                        if (p1[1] - cy) < 0:
                            startAngle = (2.0 * math.pi) - startAngle
                        plt.plot(p0[0], p0[1], "or")
                        plt.plot(p1[0], p1[1], "ob")
                        print("radius", radius)
                        print("start angle: ", startAngle*(180.0/math.pi))
                        print("angle: ", angleDeg)
                        print("theta: ", theta*(180.0/math.pi))
                        print("gamma: ", gamma*(180.0/math.pi))
                        plt.plot(cx, cy, "^g")
                        if angleDeg < 0:
                            arc = patches.Arc((cx, cy), 2*radius, 2*radius, startAngle*(180.0/math.pi), angleDeg, 0)
                        else:
                            arc = patches.Arc((cx, cy), 2 * radius, 2 * radius, startAngle * (180.0 / math.pi),
                                              0, angleDeg)
                        plt.gca().add_patch(arc)

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