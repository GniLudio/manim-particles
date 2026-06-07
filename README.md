# manim-particles

Particle disintegration and materialization animations for [Manim Community](https://www.manim.community/).

Objects shatter into hundreds of small pieces that scatter outward (`Disintegrate`), or the reverse — pieces fly in from all directions and assemble into an object (`Materialize`). Colors and opacity are sampled per-particle from a rendered image of the original object, so multicolor and gradient objects work correctly.

## Installation

```bash
pip install git+https://github.com/noah59049/manim-particles
```

Developed and tested against Manim Community v0.20.1. Requires Python 3.10+.


## Quick start

```python
from manim import *
from manim_particles import Disintegrate, Materialize

class Example(Scene):
    def construct(self):
        text = Text("Hello", font_size=120)
        self.play(Materialize(text))
        self.wait()
        self.play(Disintegrate(text))
```

## Usage

Both classes accept any `VMobject` or `VGroup` and all standard Manim animation kwargs (`run_time`, `rate_func`, `lag_ratio`, …).

```python
# Materialize — pieces converge into the object, then the object appears
self.play(Materialize(my_mob, run_time=2))

# Disintegrate — the object disappears, pieces fly outward
self.play(Disintegrate(my_mob, run_time=1.5))
```

### Parameters

Both classes share the same keyword arguments beyond standard Manim kwargs:

| Parameter | Default | Description |
|---|---|---|
| `piece_size` | `0.1` | Side length of each square particle in Manim units |
| `to_scale` | `lambda: 0` | Callable returning the scale factor each piece shrinks to. `None` to skip. |
| `to_fade` | `lambda: 1` | Callable returning how much each piece fades (0 = stays, 1 = fully fades). `None` to skip. |
| `shift_strength` | `lambda: uniform(0.5, 1.5)` | Callable returning the distance each piece travels |
| `x_shift` | `lambda: sin(uniform(0, 2π))` | Callable returning the x component of travel direction |
| `y_shift` | `lambda: sin(uniform(0, 2π))` | Callable returning the y component of travel direction |
| `z_shift` | `lambda: 0` | Callable returning the z component of travel direction |

All callables are invoked independently per particle, so passing a lambda with `random` gives a different value for each piece.

### Examples

```python
# Slower, bigger pieces
self.play(Disintegrate(mob, piece_size=0.2, run_time=3))

# Pieces fly only upward
self.play(Disintegrate(mob, y_shift=lambda: 1, x_shift=lambda: 0))

# Pieces don't shrink or fade — just drift
self.play(Disintegrate(mob, to_scale=None, to_fade=None))

# Pieces explode outward with more spread
self.play(Disintegrate(mob, shift_strength=lambda: np.random.uniform(2, 4)))
```

## Supported object types

Works with any 2D `VMobject` or `VGroup`, including:

- **Text / MathTex / Tex** — including gradient and multicolor text
- **Filled shapes** — `Square`, `Circle`, `Triangle`, `Polygon`, `Star`, …
- **Stroke-only shapes** — outlines, `RegularPolygon` with no fill, `Arc`, …
- **Open paths** — `Line`, `Arrow`, `CurvedArrow`, `FunctionGraph`, …
- **Compound objects** — `Axes`, `NumberLine`, `VGroup` of mixed shapes
- **Semi-transparent objects** — opacity is preserved per particle

Does not work with 3D objects.

## How it works

1. The object is flattened to a single filled union using boolean operations. Stroke-only paths are converted to thin filled strip polygons first.
2. A grid of square particles is produced by intersecting the union with axis-aligned cells.
3. Each particle's color and opacity are sampled from a rendered image of the original object (`vmobject.get_image()`), so multicolor gradients are reproduced faithfully.
4. `Disintegrate` hides the original object at frame 0 and animates the particles outward. `Materialize` runs the same animation in reverse, then reveals the object at the last frame.

## Credits

Created by [Noah](https://github.com/noah59049) and [GniLudio](https://github.com/GniLudio)
Additional contributions by uwezi.
