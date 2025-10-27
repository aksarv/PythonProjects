"""
Pasting here so I don't lose it
"""

def get_point(x1, y1, x2, y2, t):
    return [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t]


def bezier(cp, t):
    new = []
    for i in range(len(cp) - 1):
        new.append(get_point(*cp[i], *cp[i + 1], t))
    if len(new) == 1:
        return new[0]
    return bezier(new, t)
