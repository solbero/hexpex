<!-- PROJECT TITLE -->
<h1 align="center">Hexpex</h1>

<!-- PROJECT BLURB -->
<p align="center">
  <em>A type-hinted, object-oriented Python implementation for working with hex grids</em>
</p>

<!-- PROJECT SHIELDS -->
<div align="center">
  <a href="https://github.com/solbero/hexpex/actions/workflows/build.yaml/" target="_blank">
    <img src="https://github.com/solbero/hexpex/actions/workflows/build.yaml/badge.svg?branch=main&event=push" alt="Build checks">
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

<!-- TABLE OF CONTENTS -->
<div align="center">
  <details>
    <summary>Table of Contents</summary>
    <p>
      <a href="#about-the-project">About the Project</a>
      <br>
      <a href="#prerequisites">Prerequisites</a>
      <br>
      <a href="#installation">Installation</a>
      <br>
      <a href="#usage">Usage</a>
      <br>
      <a href="#roadmap">Roadmap</a>
      <br>
      <a href="#contributing">Contributing</a>
      <br>
      <a href="#license">License</a>
      <br>
      <a href="#contact">Contact</a>
      <br>
      <a href="#project-links">Project Links</a>
      </br>
      <a href="#acknowledgments">Acknowledgments</a>
    </p>
  </details>
</div>

<!-- ABOUT THE PROJECT -->
## About the Project

This is a type-hinted, object-oriented implementation in Python of [hexagonal grids](https://www.redblobgames.com/grids/hexagons/) as described on [Red Blob Games](https://www.redblobgames.com/).
This package allows you to easily work with hexagonal grids in Python.
All of its classes, attributes and methods are type-hinted which allows your editor to autocomplete signatures and catch bugs and mistakes early.

<p align="right">(<a href="#hexpex">back to top</a>)</p>

<!-- PREREQUISITES -->
## Prerequisites

Because this package uses type hints, keyword-only and positional-only arguments you must have Python 3.9 or greater installed.

<p align="right">(<a href="#hexpex">back to top</a>)</p>

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

<p align="right">(<a href="#hexpex">back to top</a>)</p>

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

A cube object can be converted to an axial object using the `convert_to_axial()` method.
The reverse is true for an axial object using the `convert_to_cube()` method.

```python

from hexpex import Axial, Cube

cube = Cube(1, 0, -1)
axial = Axial(1, 0)

cube.convert_to_axial()
#> Axial(1, 0)
axial.convert_to_cube()
#> Cube(1, 0, -1)
```

<p align="right">(<a href="#hexpex">back to top</a>)</p>

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

<p align="right">(<a href="#hexpex">back to top</a>)</p>

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

<p align="right">(<a href="#hexpex">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPLv3 License.
See [`LICENSE.txt`](https://github.com/solbero/hexpex/blob/master/LICENSE.txt) for more information.

<p align="right">(<a href="#hexpex">back to top</a>)</p>

<!-- CONTACT -->
## Contact

* Email: [njord.solberg@gmail.com](mailto:njord.solberg@gmail.com)

<p align="right">(<a href="#hexpex">back to top</a>)</p>

<!-- PROJECT LINKS -->
## Project Links

* Github: [https://github.com/solbero/hexpex](https://github.com/solbero/hexpex)
* PyPI: [https://pypi.org/project/hexpex/](https://pypi.org/project/hexpex/)

<p align="right">(<a href="#hexpex">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [KeeganW's](https://github.com/KeeganW) [TI4 Generator](https://github.com/KeeganW/ti4) for tile, map and faction data
* [dotlogx](https://github.com/dotlogix) for tile scans

<p align="right">(<a href="#hexpex">back to top</a>)</p>
