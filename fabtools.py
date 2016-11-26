import ezdxf
from argparse import ArgumentParser
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename", type=str, help="DXF filename to process.")
    args = parser.parse_args()

    dwg = ezdxf.readfile(args.filename)
    modelspace = dwg.modelspace()

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
                plt.plot(zip(*mat_points)[0], zip(*mat_points)[1])
        elif element.dxftype() == "POLYLINE":
            print("POLYLINE")
        else:
            print(element.dxftype())
        # elif element.dxftype() == "REGION":
        #     with element.edit_data() as data:
        #         print(data)

plt.show()