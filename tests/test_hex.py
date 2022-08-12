from collections.abc import Sequence
from typing import TypeVar

import pytest

from hexpex.hex import Axial
from hexpex.hex import AxialFlatAdjacentDirection as AxialAdjacentDirection
from hexpex.hex import AxialFlatDiagonalDirection as AxialDiagonalDirection
from hexpex.hex import Cube
from hexpex.hex import CubeFlatAdjacentDirection as CubeAdjacentDirection
from hexpex.hex import CubeFlatDiagonalDirection as CubeDiagonalDirection
from hexpex.hex import Move

T = TypeVar("T")


@pytest.fixture()
def cube_ring():
    return [
        Cube(1, 0, -1),
        Cube(0, 1, -1),
        Cube(-1, 1, 0),
        Cube(-1, 0, 1),
        Cube(0, -1, 1),
        Cube(1, -1, 0),
    ]


@pytest.fixture()
def axial_ring():
    return [
        Axial(1, 0),
        Axial(0, 1),
        Axial(-1, 1),
        Axial(-1, 0),
        Axial(0, -1),
        Axial(1, -1),
    ]


def reverse_ring(ring: Sequence[T]) -> list[T]:
    first, *rest = ring
    reversed_ring = []
    reversed_ring.append(first)
    reversed_ring.extend(reversed(rest))
    return reversed_ring


@pytest.fixture()
def cube_spiral(cube_ring):
    spiral = []
    spiral.append(Cube(0, 0, 0))
    spiral.extend(cube_ring)
    return spiral


@pytest.fixture()
def axial_spiral(axial_ring):
    spiral = []
    spiral.append(Axial(0, 0))
    spiral.extend(axial_ring)
    return spiral


@pytest.fixture()
def cube_spiral_reversed(cube_ring):
    reversed_spiral = []
    reversed_spiral.append(Cube(0, 0, 0))
    reversed_spiral.extend(reverse_ring(cube_ring))
    return reversed_spiral


@pytest.fixture()
def axial_spiral_reversed(axial_ring):
    reversed_spiral = []
    reversed_spiral.append(Axial(0, 0))
    reversed_spiral.extend(reverse_ring(axial_ring))
    return reversed_spiral


class TestHex:
    def test_cube_repr(self):
        hex = Cube(0, 0, 0)
        expected = "Cube(0, 0, 0)"
        assert repr(hex) == expected

    def test_axial_repr(self):
        hex = Axial(0, 0)
        expected = "Axial(0, 0)"
        assert repr(hex) == expected

    def test_cube_hash(self):
        hex = Cube(0, 0, 0)
        expected = 3010437511937009226
        assert hash(hex) == expected

    def test_axial_hash(self):
        hex = Axial(0, 0)
        expected = -8458139203682520985
        assert hash(hex) == expected

    def test_cube_raises_validation(self):
        match = r"attributes 'q', 'r', 's' must have a sum of 0, not \d+$"
        with pytest.raises(ValueError, match=match):
            _ = Cube(1, 0, 1)


class TestHexOperators:
    def test_cube_equal(self):
        hex1 = Cube(0, 0, 0)
        hex2 = Cube(0, 0, 0)
        assert hex1 == hex2

    def test_axial_equal(self):
        hex1 = Axial(0, 0)
        hex2 = Axial(0, 0)
        assert hex1 == hex2

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Cube(0, 0, 0), Cube(1, 0, -1)),
            (Cube(0, 0, 0), 1),
        ],
    )
    def test_cube_unequal(self, hex1, hex2):
        assert hex1 != hex2

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Axial(0, 0), Axial(1, 0)),
            (Axial(0, 0), 1),
        ],
    )
    def test_axial_unequal(self, hex1, hex2):
        assert hex1 != hex2

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Cube(0, 1, -1), Cube(0, -1, 1)),
            (Cube(0, 1, -1), Axial(0, -1)),
        ],
    )
    def test_cube_add(self, hex1, hex2):
        expected = Cube(0, 0, 0)
        assert hex1 + hex2 == expected

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Axial(0, 1), Axial(0, -1)),
            (Axial(0, 1), Cube(0, -1, 1)),
        ],
    )
    def test_axial_add(self, hex1, hex2):
        expected = Axial(0, 0)
        assert hex1 + hex2 == expected

    @pytest.mark.parametrize(
        ("hex2", "expected"),
        [
            ("1, 0, -1", TypeError),
            ((1, 0, -1), TypeError),
        ],
    )
    def test_cube_add_raises(self, hex2, expected):
        hex1 = Cube(1, 0, -1)
        with pytest.raises(expected):
            _ = hex1 + hex2

    @pytest.mark.parametrize(
        ("hex2", "expected"),
        [
            ("1, 0", TypeError),
            ((1, 0), TypeError),
        ],
    )
    def test_axial_add_raises(self, hex2, expected):
        hex1 = Axial(1, 0)
        with pytest.raises(expected):
            _ = hex1 + hex2

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Cube(0, 1, -1), Cube(0, 1, -1)),
            (Cube(0, 1, -1), Axial(0, 1)),
        ],
    )
    def test_cube_sub(self, hex1, hex2):
        expected = Cube(0, 0, 0)
        assert hex1 - hex2 == expected

    @pytest.mark.parametrize(
        ("hex1", "hex2"),
        [
            (Axial(0, 1), Axial(0, 1)),
            (Axial(0, 1), Cube(0, 1, -1)),
        ],
    )
    def test_axial_sub(self, hex1, hex2):
        expected = Axial(0, 0)
        assert hex1 - hex2 == expected

    @pytest.mark.parametrize(
        ("hex1", "hex2", "expected"),
        [
            (Cube(1, 0, -1), "1, 0, -1", TypeError),
            (Cube(1, 0, -1), (1, 0, -1), TypeError),
        ],
    )
    def test_cube_sub_raises(self, hex1, hex2, expected):
        with pytest.raises(expected):
            _ = hex1 - hex2

    @pytest.mark.parametrize(
        ("hex1", "hex2", "expected"),
        [
            (Axial(1, 0), "1, 0", TypeError),
            (Axial(1, 0), (1, 0), TypeError),
        ],
    )
    def test_axial_sub_raises(self, hex1, hex2, expected):
        with pytest.raises(expected):
            _ = hex1 - hex2

    @pytest.mark.parametrize(
        ("factor1", "factor2"),
        [
            (Cube(1, 0, -1), 2),
            (2, Cube(1, 0, -1)),
        ],
    )
    def test_cube_mul(self, factor1, factor2):
        expected = Cube(2, 0, -2)
        assert factor1 * factor2 == expected

    @pytest.mark.parametrize(
        ("factor1", "factor2"),
        [
            (Axial(1, 0), 2),
            (2, Axial(1, 0)),
        ],
    )
    def test_axial_mul(self, factor1, factor2):
        expected = Axial(2, 0)
        assert factor1 * factor2 == expected

    @pytest.mark.parametrize(
        ("factor1", "factor2", "exception"),
        [
            (Cube(0, 1, -1), 2.5, TypeError),
            (2.5, Cube(0, 1, -1), TypeError),
        ],
    )
    def test_cube_mul_raises(self, factor1, factor2, exception):
        with pytest.raises(exception):
            _ = factor1 * factor2

    @pytest.mark.parametrize(
        ("factor1", "factor2", "exception"),
        [
            (Axial(0, 1), 2.5, TypeError),
            (2.5, Axial(0, 1), TypeError),
        ],
    )
    def test_axial_mul_raises(self, factor1, factor2, exception):
        with pytest.raises(exception):
            _ = factor1 * factor2

    @pytest.mark.parametrize(
        ("hex", "divisor", "expected"),
        [
            (Cube(0, -2, 2), 2, Cube(0, -1, 1)),
            (Cube(0, -1, 1), 2, Cube(0, 0, 0)),
        ],
    )
    def test_cube_floordiv(self, hex, divisor, expected):
        assert hex // divisor == expected

    @pytest.mark.parametrize(
        ("hex", "divisor", "expected"),
        [
            (Axial(0, -2), 2, Axial(0, -1)),
            (Axial(0, -1), 2, Axial(0, 0)),
        ],
    )
    def test_axial_floordiv(self, hex, divisor, expected):
        assert hex // divisor == expected

    def test_cube_floordiv_raises(self):
        hex = Cube(0, 1, -1)
        divisor = 2.5
        with pytest.raises(TypeError):
            _ = hex // divisor  # type: ignore

    def test_hex_floordiv_raises(self):
        hex = Axial(0, 1)
        divisor = 2.5
        with pytest.raises(TypeError):
            _ = hex // divisor  # type: ignore

    def test_cube_abs(self):
        hex = Cube(1, 0, -1)
        expected = 2
        assert abs(hex) == expected

    def test_axial_abs(self):
        hex = Axial(1, 0)
        expected = 2
        assert abs(hex) == expected


class TestNeighbors:
    @pytest.mark.parametrize(
        ("direction"),
        [
            (CubeAdjacentDirection.SE),
            (Cube(1, 0, -1)),
        ],
    )
    def test_cube_adjacent(self, direction):
        hex = Cube(0, 0, 0)
        adjacent = hex.adjacent(direction)
        expected = Cube(1, 0, -1)
        assert adjacent == expected

    @pytest.mark.parametrize(
        ("direction"),
        [
            (AxialAdjacentDirection.SE),
            (Axial(1, 0)),
        ],
    )
    def test_axial_adjacent(self, direction):
        hex = Axial(0, 0)
        adjacent = hex.adjacent(direction)
        expected = Axial(1, 0)
        assert adjacent == expected

    @pytest.mark.parametrize(
        ("direction"),
        [
            (CubeDiagonalDirection.E),
            (Cube(2, -1, -1)),
        ],
    )
    def test_cube_diagonal(self, direction):
        hex = Cube(0, 0, 0)
        diagonal = hex.diagonal(direction)
        expected = Cube(2, -1, -1)
        assert diagonal == expected

    @pytest.mark.parametrize(
        ("direction"),
        [
            (AxialDiagonalDirection.E),
            (Axial(2, -1)),
        ],
    )
    def test_axial_diagonal(self, direction):
        hex = Axial(0, 0)
        diagonal = hex.diagonal(direction)
        expected = Axial(2, -1)
        assert diagonal == expected


class TestHexRing:
    def test_cube_ring(self, cube_ring):
        center = Cube(0, 0, 0)
        radius = 1
        ring = center.ring(radius)
        expected = set(cube_ring)
        assert ring == expected

    def test_axial_ring(self, axial_ring):
        center = Axial(0, 0)
        radius = 1
        ring = center.ring(radius)
        expected = set(axial_ring)
        assert ring == expected


class TestHexRotate:
    def test_hex_rotate(self):
        center = Cube(0, 0, 0)
        angle = 0
        hexes = {Cube(2, 0, -2), Cube(-2, 0, 2)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Cube(2, 0, -2), Cube(-2, 0, 2)}
        assert rotated == expected

    def test_axial_rotate(self):
        center = Axial(0, 0)
        angle = 0
        hexes = {Axial(2, 0), Axial(-2, 0)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Axial(2, 0), Axial(-2, 0)}
        assert rotated == expected

    def test_hex_rotate_clockwise(self):
        center = Cube(0, 0, 0)
        angle = 60
        hexes = {Cube(2, 0, -2), Cube(-2, 0, 2)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Cube(0, 2, -2), Cube(0, -2, 2)}
        assert rotated == expected

    def test_axial_rotate_clockwise(self):
        center = Axial(0, 0)
        angle = 60
        hexes = {Axial(2, 0), Axial(-2, 0)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Axial(0, 2), Axial(0, -2)}
        assert rotated == expected

    def test_cube_rotate_counterclockwise(self):
        center = Cube(0, 0, 0)
        angle = -60
        hexes = {Cube(2, 0, -2), Cube(-2, 0, 2)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Cube(2, -2, 0), Cube(-2, 2, 0)}
        assert rotated == expected

    def test_axial_rotate_counterclockwise(self):
        center = Axial(0, 0)
        angle = -60
        hexes = {Axial(2, 0), Axial(-2, 0)}
        rotated = center.rotate(hexes, angle=angle)
        expected = {Axial(2, -2), Axial(-2, 2)}
        assert rotated == expected

    def test_cube_rotate_raises_angle(self):
        center = Cube(0, 0, 0)
        angle = 30
        hexes = {Cube(2, 0, -2), Cube(-2, 0, 2)}
        exception = ValueError
        with pytest.raises(exception):
            _ = list(center.rotate(hexes, angle=angle))

    def test_axial_rotate_raises_angle(self):
        center = Axial(0, 0)
        angle = 30
        hexes = {Axial(2, 0), Axial(-2, 0)}
        exception = ValueError
        with pytest.raises(exception):
            _ = list(center.rotate(hexes, angle=angle))


class TestHexDistance:
    def test_cube_distance(self):
        hex1 = Cube(1, 0, -1)
        hex2 = Cube(-1, 0, 1)
        distance = hex1.distance(hex2)
        expected = 2
        assert distance == expected

    def test_axial_distance(self):
        hex1 = Axial(1, 0)
        hex2 = Axial(-1, 0)
        distance = hex1.distance(hex2)
        expected = 2
        assert distance == expected


class TestSpiral:
    def test_cube_spiral(self, cube_spiral):
        center = Cube(0, 0, 0)
        radius = 1
        direction = CubeAdjacentDirection.SE
        spiral = list(center.spiral(radius, direction))
        expected = cube_spiral
        assert spiral == expected

    def test_axial_spiral(self, axial_spiral):
        center = Axial(0, 0)
        radius = 1
        direction = AxialAdjacentDirection.SE
        spiral = list(center.spiral(radius, direction))
        expected = axial_spiral
        assert spiral == expected

    def test_cube_spiral_reversed(self, cube_spiral_reversed):
        center = Cube(0, 0, 0)
        radius = 1
        direction = CubeAdjacentDirection.SE
        move = Move.COUNTERCLOCKWISE
        spiral = list(center.spiral(radius, direction, move))
        expected = cube_spiral_reversed
        assert spiral == expected

    def test_axial_spiral_reversed(self, axial_spiral_reversed):
        center = Axial(0, 0)
        radius = 1
        direction = AxialAdjacentDirection.SE
        move = Move.COUNTERCLOCKWISE
        spiral = list(center.spiral(radius, direction, move))
        expected = axial_spiral_reversed
        assert spiral == expected


class TestHexConversion:
    def test_cube_to_axial(self):
        cube = Cube(1, 0, -1)
        converted = cube.to_axial()
        expected = Axial(1, 0)
        assert converted == expected

    def test_axial_to_cube(self):
        axial = Axial(1, 0)
        converted = axial.to_cube()
        expected = Cube(1, 0, -1)
        assert converted == expected

    def test_cube_to_tuple(self):
        cube = Cube(1, 0, -1)
        converted = cube.to_tuple()
        expected = (1, 0, -1)
        assert converted == expected

    def test_axial_to_tuple(self):
        axial = Axial(1, 0)
        converted = axial.to_tuple()
        expected = (1, 0)
        assert converted == expected

    def test_cube_to_dict(self):
        cube = Cube(1, 0, -1)
        converted = cube.to_dict()
        expected = {"q": 1, "r": 0, "s": -1}
        assert converted == expected

    def test_axial_to_dict(self):
        axial = Axial(1, 0)
        converted = axial.to_dict()
        expected = {"q": 1, "r": 0}
        assert converted == expected


class TestHexRange:
    def test_cube_range(self, cube_spiral):
        center = Cube(0, 0, 0)
        range = 1
        hexes = center.range(range)
        expected = set(cube_spiral)
        assert hexes == expected

    def test_axial_range(self, axial_spiral):
        center = Axial(0, 0)
        range = 1
        hexes = center.range(range)
        expected = set(axial_spiral)
        assert hexes == expected
