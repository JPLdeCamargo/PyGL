from game_objects.wireframe import WireFrame
from game_objects.line import Line
from game_objects.point import Point

y = 2000
x = 5000
basic_square = WireFrame(True, [(x, x), (y, x), (y, y), (x, y)])
basic_line = Line((1000, 1000), (-5000,400))
cool_triangle = WireFrame(True, [(0,0), (7000, 0), (3500, 3500)])
smol_point = Point((-200, -200))

to_load = [basic_square, basic_line, cool_triangle, smol_point]