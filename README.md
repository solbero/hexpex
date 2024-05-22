<!-- PROJECT TITLE -->
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/solbero/hexpex/main/logo-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/solbero/hexpex/main/logo-light.png">
    <img src="https://raw.githubusercontent.com/solbero/hexpex/main/logo-light.png" alt="Hexpex project logo" />
  </picture>
</p>

<!-- PROJECT BLURB -->
<p align="center">
  <em>A type-hinted, object-oriented Python implementation for working with hex grids</em>
</p>

<!-- PROJECT SHIELDS -->
<div align="center">
  <a href="https://github.com/solbero/hexpex/actions/workflows/build.yaml" target="_blank">
    <img src="https://img.shields.io/github/actions/workflow/status/solbero/hexpex/build.yaml?label=build" alt="Build action">
  </a>
  <a href="https://github.com/solbero/hexpex/actions/workflows/publish.yaml" target="_blank">
    <img src="https://img.shields.io/github/actions/workflow/status/solbero/hexpex/publish.yaml?label=publish" alt="Publish action" >

  </a>
  <a href="https://app.codecov.io/gh/solbero/hexpex" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/solbero/hexpex" alt="Code coverage">
  </a>
  <a href="https://pypi.org/project/hexpex/" target="_blank">
    <img src="https://img.shields.io/pypi/v/hexpex" alt="Package version">
  </a>
  <a href="https://pypi.org/project/hexpex/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/hexpex" alt="Supported Python versions">
  </a>
  <a href="https://github.com/solbero/hexpex/blob/master/LICENSE.txt" target="_blank">
    <img src="https://img.shields.io/github/license/solbero/hexpex" alt="License">
  </a>
</div>

<!-- ABOUT THE PROJECT -->
## About the Project

This is a type-hinted, object-oriented implementation in Python of [hexagonal grids](https://www.redblobgames.com/grids/hexagons/) as described on [Red Blob Games](https://www.redblobgames.com/).
This package allows you to easily work with hexagonal grids in Python.
All of its classes, attributes and methods are type-hinted which allows your editor to autocomplete signatures and catch bugs and mistakes early.

<!-- PREREQUISITES -->
## Prerequisites

Because this package uses type hints, keyword-only and positional-only arguments you must have Python 3.9 or greater installed.

<!-- INSTALLATION -->

## Installation

### Using PIP

   ```sh
   pip install hexpex
   ```

### Using Poetry

   ```sh
   poetry add hexpex
   ```

### Manually (for testing or development)

  ```sh
  git clone https://github.com/solbero/hexpex.git
  cd hexpex
  poetry install
  ```

<!-- USAGE EXAMPLES -->
## Usage

### Classes

Hexpex provides classes for working with hexagonal grids in both the cube and axial coordinate systems.
For more information about the difference between these two coordinate systems see the writeup on [Red Blob Games](https://www.redblobgames.com/grids/hexagons/#coordinates).

```python
from hexpex import Axial, Cube

Cube(q=1, r=0, s=-1)
Axial(q=1, r=0)
```

### Object Methods

<dl>
  <dt><code>adjacent()</code></dt>
  <dd>Returns the hex coordinate in adjacent direction from self</dd>

  <dt><code>diagonal()</code></dt>
  <dd>Returns the hex coordinate in diagonal direction from self</dd>

  <dt><code>distance()</code></dt>
  <dd>Returns the distance between passed hex coordinate and self</dd>

  <dt><code>range()</code></dt>
  <dd>Returns a set of hex coordinates within passed distance of self</dd>

  <dt><code>ring()</code></dt>
  <dd>Returns a set of hex coordinates on a ring passed distance from self</dd>

  <dt><code>rotation()</code></dt>
  <dd>Returns a set of rotated hex coordinates rotated around self</dd>

  <dt><code>spiral()</code></dt>
  <dd>Yields hex positions in a spiral from self out to passed distance from self</dd>
</dl>

### Operations

Objects can be added or subtracted from each other, and multiplied or divided by integers.

```python
from hexpex import Axial, Cube

cube_1 = Cube(q=2, r=0, s=-2)
cube_2 = Cube(q=-1, r=0, s=1)

cube_1 + cube_2
#> Cube(1, 0, -1)
cube_1 - cube_2
#> Cube(3, 0, -3)
cube_1 * 2
#> Cube(4, 0, -4)
cube_1 // 2
#> Cube(1, 0, -1)

axial_1 = Axial(q=2, r=0)
axial_2 = Axial(q=-1, r=0)

axial_1 + axial_2
#> Axial(1, 0)
axial_1 - axial_2
#> Axial(3, 0)
axial_1 * 2
#> Axial(4, 0)
axial_1 // 2
#> Axial(1, 0)

```

### Direction Vectors

Hexpex provides some helper enums for giving direction vectors to the methods `adjacent()`, `diagonal()` and `spiral()`.
To use them import the enums for your coordinate system and hex orientation (pointy or flat).
For more information on the difference between the two hex orientations see [Red Blob Games](https://www.redblobgames.com/grids/hexagons/#basics).

```python
from hexpex import Cube, CubeFlatAdjacentDirection as AdjacentDirection, CubeFlatDiagonalDirection as DiagonalDirection

cube = Cube(0, 0, 0)

cube.adjacent(AdjacentDirection.SE)
#> Cube(1, 0, -1)
cube.diagonal(DiagonalDirection.E)
#> Cube(2, -1, -1)
```

### Conversion

A cube object can be converted to an axial object using the `to_axial()` method.
The reverse is true for an axial object using the `to_cube()` method.

Both representations can also be converted to a tuple using the `to_tuple()` method and to a dict using the `to_dict()`method.

```python

from hexpex import Axial, Cube

cube = Cube(1, 0, -1)
axial = Axial(1, 0)

cube.to_axial()
#> Axial(1, 0)
axial.to_cube()
#> Cube(1, 0, -1)

cube.to_tuple()
#> (1, 0, -1)
axial.to_tuple()
#> (1, 0)

cube.to_dict()
#> {"q": 1, "r": 0, "s": -1}
axial.to_dict()
#> {"q": 1, "r": 0}
```

<!-- ROADMAP -->
## Roadmap

### Coordinate systems

* [x] Cube coordinates
* [x] Axial coordinates
* [ ] Double offset coordinates

### Methods

* [x] Distances
* [x] Neighbors
* [x] Range
* [x] Rings
* [x] Rotation
* [x] Spiral
* [ ] Line drawing
* [ ] Reflection
* [ ] Rounding
* [ ] Hex to pixel
* [ ] Pixel to hex

See the [open issues](https://github.com/solbero/hexpex/issues) for a full list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this project better, please [fork the repo](https://github.com/solbero/hexpex/fork) and create a pull request.
You can also simply [open an issue](https://github.com/solbero/hexpex/issues/new/choose) with the label "enhancement".

1. Fork the project
2. Create your feature branch

  ```sh
  git checkout -b feature/AmazingFeature
  ```

3. Commit your changes

  ```sh
  git commit -m 'Add some AmazingFeature'
  ```

4. Push to the branch

```sh
git push origin feature/AmazingFeature
```

5. Open a pull request

<!-- LICENSE -->
## License

Distributed under the GPLv3 License.
See [`LICENSE.txt`](https://github.com/solbero/hexpex/blob/master/LICENSE.txt) for more information.

<!-- CONTACT -->
## Contact

* Email: [njord.solberg@gmail.com](mailto:njord.solberg@gmail.com)

<!-- PROJECT LINKS -->
## Project Links

* Github: [https://github.com/solbero/hexpex](https://github.com/solbero/hexpex)
* PyPI: [https://pypi.org/project/hexpex/](https://pypi.org/project/hexpex/)
