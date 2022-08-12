from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from collections import deque
from collections.abc import Iterable, Iterator
from enum import Enum
from typing import Any, TypeVar, Union, cast

T = TypeVar("T", bound="_Hex")

AdjacentDirection = Union[
    "CubeFlatAdjacentDirection",
    "CubePointyAdjacentDirection",
    "AxialFlatAdjacentDirection",
    "AxialPointyAdjacentDirection",
]
DiagonalDirection = Union[
    "CubeFlatDiagonalDirection",
    "CubePointyDiagonalDirection",
    "AxialFlatDiagonalDirection",
    "AxialPointyDiagonalDirection",
]


class Move(Enum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1


class _Hex(ABC):
    @abstractproperty
    def _adjacent_vectors(self: T) -> tuple[T, ...]:  # pragma: no cover​
        ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool:  # pragma: no cover​
        ...

    @abstractmethod
    def __ne__(self, other: Any) -> bool:  # pragma: no cover​
        ...

    @abstractmethod
    def __hash__(self) -> int:  # pragma: no cover​
        ...

    @abstractmethod
    def __add__(self: T, other: _Hex) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def __sub__(self: T, other: _Hex) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def __mul__(self: T, other: int) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def __rmul__(self: T, other: int) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def __floordiv__(self: T, other: int) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def __abs__(self) -> int:  # pragma: no cover​
        ...

    @abstractmethod
    def __repr__(self) -> str:  # pragma: no cover​
        ...

    def adjacent(self: T, direction: AdjacentDirection | _Hex, /) -> T:
        """Returns the hex position in a given adjacent direction from self position."""
        if isinstance(direction, Enum):
            return self + direction.value
        return self + direction

    def diagonal(self: T, direction: DiagonalDirection | _Hex, /) -> T:
        """Returns the hex position in a given diagonal direction from self position."""
        if isinstance(direction, Enum):
            return self + direction.value
        return self + direction

    def distance(self, position: _Hex, /) -> int:
        """Returns the distance from self position to another hex position."""
        return abs(self - position) // 2

    def ring(self: T, distance: int, /) -> set[T]:
        """Returns a ring of hex positions a certain distance from self position.

        Note:
            Returns an empty set if argument of 'distance' is '0'.

        Args:
            distance: Distance of ring from self position.

        Returns:
            Set of hex positions in ring.
        """
        direction_vector = self._adjacent_vectors[0]
        scaled_vector = direction_vector * distance
        position = self + scaled_vector

        adjacent_vectors = deque(self._adjacent_vectors)

        # Rearranges 'adjacent_vectors' to the correct order for moving around the ring.
        steps = adjacent_vectors.index(direction_vector) + 2
        adjacent_vectors.rotate(-steps)

        hexes_in_ring = set()
        for direction_vector in adjacent_vectors:
            for _ in range(distance):
                hexes_in_ring.add(position)
                position = position.adjacent(direction_vector)
        return hexes_in_ring

    def range(self: T, distance: int) -> set[T]:
        """Returns a range of hex positions up to a certain distance from self position.

        Note:
            Return self position if 'distance' is '0'.

        Args:
            distance: Max distance of range from self position.

        Returns:
            Set of hex position in range.
        """
        hexes_in_range = set()
        hexes_in_range.add(self)
        for radius in range(1, distance + 1):
            hexes_in_range.update(self.ring(radius))
        return hexes_in_range

    def spiral(self: T, distance: int, direction: AdjacentDirection, move: Move = Move.CLOCKWISE) -> Iterator[T]:
        """Yields a spiral of hex positions out to a passed distance from self position.

        Args:
            distance: Max distance to spiral out from self position.
            direction: Direction from self position to first position in the spiral.
            move: Direction to move around the spiral.

        Yields:
            Hex position in the spiral.
        """

        direction_vector = cast(T, direction.value)
        scaled_vector = direction_vector * distance
        position = self + scaled_vector

        adjacent_vectors = deque(self._adjacent_vectors)

        if move is Move.COUNTERCLOCKWISE:
            adjacent_vectors.reverse()

        # Rearranges 'adjacent_vectors' to the correct order for moving around the spiral.
        steps = adjacent_vectors.index(direction_vector) + 2
        adjacent_vectors.rotate(-steps)

        yield self
        for direction_vector in adjacent_vectors:
            for _ in range(1, distance + 1):
                yield position
                position = position.adjacent(direction_vector)

    @abstractmethod
    def _rotate_clockwise(self: T) -> T:  # pragma: no cover​
        ...

    @abstractmethod
    def _rotate_counterclockwise(self: T) -> T:  # pragma: no cover​
        ...

    def rotate(self: T, hexes: Iterable[T], angle: int) -> set[T]:
        """Returns a set of hex positions rotated around the self position.

        Note:
            If 'angle' is positive rotation is clockwise, if negative rotation is counterclockwise.

        Args:
            hexes: Iterable of hex positions to rotate.
            angle: Degrees to rotate hexes around self position.

        Raises:
            ValueError: If 'angle' is not divisible by 60.

        Returns:
            Rotated cube position(s).
        """

        # Check if 'angle' is divisible by 60.
        if angle % 60 != 0:
            raise ValueError("argument of 'angle' must be in 60 degree increments.")

        rotated = set()
        steps = abs((angle % 360) // 60)

        for hex in hexes:
            vector = hex - self
            if angle > 0:
                *_, vector = (hex._rotate_clockwise() for _ in range(steps))
            elif angle < 0:
                *_, vector = (hex._rotate_counterclockwise() for _ in range(steps))
            rotated.add(self + vector)
        return rotated

    def to_tuple(self) -> tuple[int, ...]:
        """Convert self to tuple representation."""
        return tuple(vars(self).values())

    def to_dict(self) -> dict[str, int]:
        """Convert self to dict representation."""
        return vars(self)


class Axial(_Hex):
    "An axial representation of a position or vector in a hexagonal grid."

    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r

    @property
    def _adjacent_vectors(self):
        return (
            Axial(1, 0),
            Axial(0, 1),
            Axial(-1, 1),
            Axial(-1, 0),
            Axial(0, -1),
            Axial(1, -1),
        )

    def __eq__(self, other):
        if isinstance(other, Axial):
            return self.q == other.q and self.r == other.r
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.q, self.r))

    def __add__(self, other):
        if isinstance(other, Axial):
            return Axial(self.q + other.q, self.r + other.r)
        elif isinstance(other, Cube):
            return Axial(self.q + other.q, self.r + other.r)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Axial):
            return Axial(self.q - other.q, self.r - other.r)
        elif isinstance(other, Cube):
            return Axial(self.q - other.q, self.r - other.r)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            return Axial(self.q * other, self.r * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Axial(int(self.q / other), int(self.r / other))
        return NotImplemented

    def __abs__(self):
        return abs(self.q) + abs(self.r) + abs(-self.q - self.r)

    def __repr__(self):
        return f"{type(self).__name__}({self.q}, {self.r})"

    def _rotate_clockwise(self) -> Axial:
        return Axial(q=-self.r, r=-(-self.q - self.r))

    def _rotate_counterclockwise(self) -> Axial:
        return Axial(q=-(-self.q - self.r), r=-self.q)

    def to_cube(self):
        """Convert self to cube representation."""
        return Cube(self.q, self.r, -self.q - self.r)


class Cube(_Hex):
    "A cube representation of a position or vector in a hexagonal grid."

    def __init__(self, q: int, r: int, s: int):
        self.q = q
        self.r = r
        self.s = s

        self._validate(self.q, self.r, self.s)

    @property
    def _adjacent_vectors(self):
        return (
            Cube(1, 0, -1),
            Cube(0, 1, -1),
            Cube(-1, 1, 0),
            Cube(-1, 0, 1),
            Cube(0, -1, 1),
            Cube(1, -1, 0),
        )

    def __eq__(self, other):
        if isinstance(other, Cube):
            return self.q == other.q and self.r == other.r and self.s == other.s
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.q, self.r, self.s))

    def __add__(self, other):
        if isinstance(other, Cube):
            return Cube(self.q + other.q, self.r + other.r, self.s + other.s)
        elif isinstance(other, Axial):
            return Cube(self.q + other.q, self.r + other.r, self.s + (-other.q - other.r))
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Cube):
            return Cube(self.q - other.q, self.r - other.r, self.s - other.s)
        elif isinstance(other, Axial):
            return Cube(self.q - other.q, self.r - other.r, self.s - (-other.q - other.r))
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, int):
            return Cube(self.q * other, self.r * other, self.s * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Cube(q=int(self.q / other), r=int(self.r / other), s=int(self.s / other))
        return NotImplemented

    def __abs__(self):
        return abs(self.q) + abs(self.r) + abs(self.s)

    def __repr__(self):
        return f"{type(self).__name__}({self.q}, {self.r}, {self.s})"

    def _rotate_clockwise(self) -> Cube:
        return Cube(q=-self.r, r=-self.s, s=-self.q)

    def _rotate_counterclockwise(self) -> Cube:
        return Cube(q=-self.s, r=-self.q, s=-self.r)

    def to_axial(self) -> Axial:
        """Convert self to axial representation."""
        return Axial(self.q, self.r)

    @staticmethod
    def _validate(q: int, r: int, s: int):
        if q + r + s != 0:
            raise ValueError(f"attributes 'q', 'r', 's' must have a sum of 0, not {q + r + s}")


class CubeFlatAdjacentDirection(Enum):
    """Enumerate adjacent cardinal directions for flat cube coordinates."""

    SE = Cube(1, 0, -1)
    S = Cube(0, 1, -1)
    SW = Cube(-1, 1, 0)
    NW = Cube(-1, 0, 1)
    N = Cube(0, -1, 1)
    NE = Cube(1, -1, 0)


class CubeFlatDiagonalDirection(Enum):
    """Enumerate diagonal cardinal directions for flat cube coordinates."""

    E = Cube(2, -1, -1)
    SSE = Cube(1, 1, -2)
    SSW = Cube(-1, 2, -1)
    W = Cube(-2, 1, 1)
    NNW = Cube(-1, -1, 2)
    NNE = Cube(1, -2, 1)


class CubePointyAdjacentDirection(Enum):
    """Enumerate adjacent cardinal directions for pointy cube coordinates."""

    E = Cube(1, 0, -1)
    SE = Cube(0, 1, -1)
    SW = Cube(-1, 1, 0)
    W = Cube(-1, 0, 1)
    NW = Cube(0, -1, 1)
    NE = Cube(1, -1, 0)


class CubePointyDiagonalDirection(Enum):
    """Enumerate diagonal cardinal directions for pointy cube coordinates."""

    ENE = Cube(2, -1, -1)
    SSE = Cube(1, 1, -2)
    S = Cube(-1, 2, -1)
    SSW = Cube(-2, 1, 1)
    WNW = Cube(-1, -1, 2)
    N = Cube(1, -2, 1)


class AxialFlatAdjacentDirection(Enum):
    """Enumerate adjacent cardinal directions for flat axial coordinates."""

    SE = Axial(1, 0)
    S = Axial(0, 1)
    SW = Axial(-1, 1)
    NW = Axial(-1, 0)
    N = Axial(0, -1)
    NE = Axial(1, -1)


class AxialFlatDiagonalDirection(Enum):
    """Enumerate diagonal cardinal directions for flat axial coordinates."""

    E = Axial(2, -1)
    SSE = Axial(1, 1)
    SSW = Axial(-1, 2)
    W = Axial(-2, 1)
    NNW = Axial(-1, -1)
    NNE = Axial(1, -2)


class AxialPointyAdjacentDirection(Enum):
    """Enumerate adjacent cardinal directions for pointy axial coordinates."""

    E = Axial(1, 0)
    SE = Axial(0, 1)
    SW = Axial(-1, 1)
    W = Axial(-1, 0)
    NW = Axial(0, -1)
    NE = Axial(1, -1)


class AxialPointyDiagonalDirection(Enum):
    """Enumerate diagonal cardinal directions for pointy axial coordinates."""

    ENE = Axial(2, -1)
    SSE = Axial(1, 1)
    S = Axial(-1, 2)
    SSW = Axial(-2, 1)
    WNW = Axial(-1, -1)
    N = Axial(1, -2)
