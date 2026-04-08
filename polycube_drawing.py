import functools

import matplotlib.pyplot as plt
import numpy as np

import polycube as polyc

COLOR_LIST = [
    "red",
    "orange",
    "yellow",
    "green",
    "cyan",
    "blue",
    "purple",
    "magenta",
    "brown",
    "white",
    "black",
]


def _polycube_voxels(shape, polycube):
    voxels = np.zeros(shape, dtype=bool)
    for cube in polycube.cubes:
        voxels[cube.x][cube.y][cube.z] = True
    return voxels


def _calculate_bounding_box_shape(polycubes: list[polyc.Polycube]):
    _, x_max, _, y_max, _, z_max = functools.reduce(
        lambda acc, polycube: acc.combine(polycube),
        polycubes,
        polyc.Polycube([]),
    ).get_bounds()
    return (x_max + 1, y_max + 1, z_max + 1)


def draw_polycubes_tiling(polycubes: list[polyc.Polycube]):
    shape = _calculate_bounding_box_shape(polycubes)

    polycube_masks = [_polycube_voxels(shape, polycube) for polycube in polycubes]
    voxelarray = np.logical_or.reduce(polycube_masks)
    colors = np.empty(shape, dtype=object)

    num_colors = len(COLOR_LIST)
    for i, mask in enumerate(polycube_masks):
        colors[mask] = COLOR_LIST[i % num_colors]

    ax = plt.figure().add_subplot(projection="3d")
    ax.voxels(voxelarray, facecolors=colors, edgecolors="k")
    plt.show()


def _float_to_character(n: float) -> str:
    i = int(n)
    if i == 0:
        return "."
    elif 1 <= i <= 26:
        return chr(ord("a") + i - 1)
    elif 27 <= i <= 52:
        return chr(ord("A") + i - 27)
    elif 53 <= i <= 62:
        return chr(ord("0") + i - 53)
    else:
        return chr(192 + i - 63)


def print_polycube_tiling_layers(polycubes: list[polyc.Polycube]):
    shape = _calculate_bounding_box_shape(polycubes)
    voxels = np.zeros(shape)
    for i, polycube in enumerate(polycubes):
        for cube in polycube.cubes:
            voxels[cube.x][cube.y][cube.z] = i + 1

    for i, layer in enumerate(np.vectorize(_float_to_character)(voxels)):
        print(f"Layer {i}")
        for row in layer:
            print("".join(row))
        print("")
