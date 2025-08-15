from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from collections.abc import Iterable


class Cube:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __str__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Cube)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __lt__(self, other: Cube) -> bool:
        return self.to_tuple().__lt__(other.to_tuple())

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def translate(self, dx: int, dy: int, dz: int) -> Cube:
        return Cube(self.x + dx, self.y + dy, self.z + dz)

    def rotate_anticlockwise_about_x_axis(self) -> Cube:
        return Cube(self.x, -self.z, self.y)

    def rotate_anticlockwise_about_y_axis(self) -> Cube:
        return Cube(self.z, self.y, -self.x)

    def rotate_anticlockwise_about_z_axis(self) -> Cube:
        return Cube(-self.y, self.x, self.z)

    def mirror_about_xy_plane(self) -> Cube:
        return Cube(self.x, self.y, -self.z)

    def mirror_about_yz_plane(self) -> Cube:
        return Cube(-self.x, self.y, self.z)

    def mirror_about_xz_plane(self) -> Cube:
        return Cube(self.x, -self.y, self.z)


class Polycube:
    MAX_XYZ = 999

    def __init__(self, cubes: Iterable[Cube]) -> None:
        self.cubes: set[Cube] = set(cubes)

    def __str__(self) -> str:
        return f"Polycube({','.join((str(cube) for cube in self.cubes))})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Polycube) and self.cubes == other.cubes

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.cubes)))

    def get_bounds(self) -> tuple[int, int, int, int, int, int]:
        x_min = Polycube.MAX_XYZ
        y_min = Polycube.MAX_XYZ
        z_min = Polycube.MAX_XYZ
        x_max = -Polycube.MAX_XYZ
        y_max = -Polycube.MAX_XYZ
        z_max = -Polycube.MAX_XYZ
        for cube in self.cubes:
            if cube.x < x_min:
                x_min = cube.x
            if cube.x > x_max:
                x_max = cube.x
            if cube.y < y_min:
                y_min = cube.y
            if cube.y > y_max:
                y_max = cube.y
            if cube.z < z_min:
                z_min = cube.z
            if cube.z > z_max:
                z_max = cube.z
        return (x_min, x_max, y_min, y_max, z_min, z_max)

    def translate_to_origin(self) -> Polycube:
        x_min = Polycube.MAX_XYZ
        y_min = Polycube.MAX_XYZ
        z_min = Polycube.MAX_XYZ
        for cube in self.cubes:
            if cube.x < x_min:
                x_min = cube.x
            if cube.y < y_min:
                y_min = cube.y
            if cube.z < z_min:
                z_min = cube.z
        return self.translate(-x_min, -y_min, -z_min)

    def translate(self, dx: int, dy: int, dz: int) -> Polycube:
        return Polycube((cube.translate(dx, dy, dz) for cube in self.cubes))

    def rotate_anticlockwise_about_x_axis(self) -> Polycube:
        return Polycube(
            (cube.rotate_anticlockwise_about_x_axis() for cube in self.cubes)
        )

    def rotate_anticlockwise_about_y_axis(self) -> Polycube:
        return Polycube(
            (cube.rotate_anticlockwise_about_y_axis() for cube in self.cubes)
        )

    def rotate_anticlockwise_about_z_axis(self) -> Polycube:
        return Polycube(
            (cube.rotate_anticlockwise_about_z_axis() for cube in self.cubes)
        )

    def mirror_about_xy_plane(self) -> Polycube:
        return Polycube((cube.mirror_about_xy_plane() for cube in self.cubes))

    def mirror_about_yz_plane(self) -> Polycube:
        return Polycube((cube.mirror_about_yz_plane() for cube in self.cubes))

    def mirror_about_xz_plane(self) -> Polycube:
        return Polycube((cube.mirror_about_xz_plane() for cube in self.cubes))

    def apply_transform(self, transform: str) -> Polycube:
        piece = self
        match transform.upper():
            case "RX":
                piece = piece.rotate_anticlockwise_about_x_axis()
            case "RY":
                piece = piece.rotate_anticlockwise_about_y_axis()
            case "RZ":
                piece = piece.rotate_anticlockwise_about_z_axis()
            case "MXY" | "MZ":
                piece = piece.mirror_about_xy_plane()
            case "MYZ" | "MX":
                piece = piece.mirror_about_yz_plane()
            case "MXZ" | "MZ":
                piece = piece.mirror_about_xz_plane()
            case _:
                # Do nothing
                pass
        return piece

    def apply_rotations(self, rotations: str) -> Polycube:
        piece = self
        for c in rotations.upper():
            if c == "X":
                piece = piece.rotate_anticlockwise_about_x_axis()
            if c == "Y":
                piece = piece.rotate_anticlockwise_about_y_axis()
            if c == "Z":
                piece = piece.rotate_anticlockwise_about_z_axis()
        return piece

    def contains(self, polycube: Polycube) -> bool:
        return all((cube in self.cubes for cube in polycube.cubes))


def generate_positions(
    origin_box: Polycube, origin_polycube: Polycube
) -> set[Polycube]:
    (_, box_x_max, _, box_y_max, _, box_z_max) = origin_box.get_bounds()
    (_, x_max, _, y_max, _, z_max) = origin_polycube.get_bounds()
    displacements = product(
        range(1 + box_x_max - x_max),
        range(1 + box_y_max - y_max),
        range(1 + box_z_max - z_max),
    )
    return set(
        filter(
            lambda p: origin_box.contains(p),
            (origin_polycube.translate(x, y, z) for (x, y, z) in displacements),
        )
    )
