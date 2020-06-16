"""
From Raymond Hettingers talk : Dataclasses: The code generator to end all code generators - PyCon 2018

"""

from dataclasses import dataclass


@dataclass(order=True, frozen=True)  # Options for sorting, ordering (frozen is hashable)
class Color:
    x: int
    y: float
    z: float = .05


x = 2
y = 3.7

data = {
    'colors': [
        {'x': x, 'y': y},
        {'x': 1, 'y': 6.337},
    ]
}

c = Color(5, 2.7)

colors = [Color(**color) for color in data['colors']]

for i in colors:
    print(i)

