from .game_objects.wireframe import WireFrame
from .game_objects.line import Line
from .game_objects.point import Point

"""
file with parameters that we can change according to our preferences
we will implement an interactive window where we will create our wireframe 
with its name, color, coordinates, etc...
"""

y = 2000
x = 5000
basic_square = WireFrame("Bob", True, [(x, x), (y, x), (y, y), (x, y)])

basic_line = Line("Roger", (1000, 1000), (7000, 7000))
cool_triangle = WireFrame("Érica", True, [(0,0), (7000, 0), (3500, 3500)])
smol_point = Point("Enzo", (-200, -200))

to_load = [basic_square, basic_line, cool_triangle, smol_point]