from argparse import ArgumentParser
from cycler import cycler
import matplotlib.pyplot as plt
import ezdxf


def main(args):
    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="DXF file to show you.")
    parser.add_argument("-d", "--debug", action="store_true", default=False)
    parsed = parser.parse_args(args)
    dwg = ezdxf.readfile(parsed.filename)
    modelspace = dwg.modelspace()

    if not parsed.debug:
        plt.rc('axes', prop_cycle=(cycler('color', ['black'])))

    for element in modelspace:
        if element.dxftype() == 'LINE':
            start_pnt = element.dxf.start
            end_pnt = element.dxf.end
            plt.plot([start_pnt[0], end_pnt[0]], [start_pnt[1], end_pnt[1]])
            print(start_pnt)
            print(end_pnt)
        elif element.dxftype() == "LWPOLYLINE":
            pass
            with element.points() as points:
                mat_points = []
                for point in points:
                    mat_points.append(point[0:2])

                points_it = zip(*mat_points)
                first_point = next(points_it)
                second_point = next(points_it)
                plt.plot(first_point, second_point)
        elif element.dxftype() == "POLYLINE":
            print("POLYLINE")
        else:
            print(element.dxftype())
        # elif element.dxftype() == "REGION":
        #     with element.edit_data() as data:
        #         print(data)

    plt.show()