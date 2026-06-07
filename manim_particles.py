from manim import *
import typing
from PIL import Image

__all__ = ["Disintegrate", "Materialize"]


def _apparent_color(m: VMobject) -> np.ndarray:
    if m.get_fill_opacity() > 0:
        return color_to_rgb(m.get_fill_color())
    return color_to_rgb(m.get_stroke_color())


def _apparent_opacity(m: VMobject) -> float:
    return m.get_fill_opacity() or m.get_stroke_opacity()


def _ensure_filled(m: VMobject) -> VMobject:
    if m.get_fill_opacity() > 0:
        return m
    pts = m.points
    color = m.get_stroke_color()
    opacity = m.get_stroke_opacity() or 1
    stroke_radius = max(m.get_stroke_width() / 200, 0.02)
    is_closed = np.linalg.norm(pts[-1] - pts[0]) < 0.01
    n = 64
    if is_closed:
        path_pts = np.array(
            [m.point_from_proportion(t) for t in np.linspace(0, 1, n, endpoint=False)]
        )
        tangents = np.diff(np.vstack([path_pts, path_pts[0]]), axis=0)
        unit_t = tangents / np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-8)
        perps = np.c_[-unit_t[:, 1], unit_t[:, 0], np.zeros(n)]
        avg_perps = (perps + np.roll(perps, 1, axis=0)) / 2
    else:
        path_pts = np.array([m.point_from_proportion(t) for t in np.linspace(0, 1, n)])
        tangents = np.diff(path_pts, axis=0)
        unit_t = tangents / np.maximum(np.linalg.norm(tangents, axis=1, keepdims=True), 1e-8)
        perps = np.c_[-unit_t[:, 1], unit_t[:, 0], np.zeros(n - 1)]
        avg_perps = np.vstack([perps[:1], (perps[:-1] + perps[1:]) / 2, perps[-1:]])
    avg_perps /= np.maximum(np.linalg.norm(avg_perps, axis=1, keepdims=True), 1e-8)
    upper = path_pts + stroke_radius * avg_perps
    lower = path_pts - stroke_radius * avg_perps
    return (
        Polygon(*np.vstack([upper, lower[::-1]]))
        .set_stroke(width=0)
        .set_fill(color=color, opacity=opacity)
    )


def _flatten(mob: Mobject) -> VMobject:
    leaves = [_ensure_filled(m) for m in mob.get_family() if len(m.points) > 0]
    if not leaves:
        return mob
    if len(leaves) == 1:
        return leaves[0]
    return Union(*leaves)


def _to_grid(
    mob: Mobject,
    piece_size: float | None,
    resample: int = Image.Resampling.NEAREST,
) -> VMobject:
    stroke_unit = 0.05  # TODO: What does this magic number mean?
    stroke_offset = stroke_unit * mob.get_stroke_width()
    width_with_stroke = mob.width + 2 * stroke_offset
    height_with_stroke = mob.height + 2 * stroke_offset

    image = np.asarray(mob.get_image(Camera(background_opacity=0)))
    image = image[::-1]  # inverts y axis

    # bounding box of content
    def to_pixel(frame_position: int, frame_size: float, pixel_size: int) -> int:
        pixel_position = int((frame_position + frame_size / 2) * pixel_size / frame_size)
        return max(0, min(pixel_size - 1, pixel_position))

    bb_frame = [
        mob.get_bottom()[1] - stroke_offset,
        mob.get_top()[1] + stroke_offset,
        mob.get_left()[0] - stroke_offset,
        mob.get_right()[0] + stroke_offset,
    ]
    bb_pixel = [
        to_pixel(bb_frame[0], config.frame_height, config.pixel_height),
        to_pixel(bb_frame[1], config.frame_height, config.pixel_height),
        to_pixel(bb_frame[2], config.frame_width, config.pixel_width),
        to_pixel(bb_frame[3], config.frame_width, config.pixel_width),
    ]
    image = image[
        bb_pixel[0] : bb_pixel[1],
        bb_pixel[2] : bb_pixel[3],
    ]

    # resize to fit piece_size
    if piece_size is not None:
        resolution = (int(height_with_stroke / piece_size), int(width_with_stroke / piece_size))
        image = np.asarray(
            Image.fromarray(image).resize((resolution[1], resolution[0]), resample=resample)
        )
    else:
        piece_size = float((bb_frame[1] - bb_frame[0]) / image.shape[0])

    # create grid
    grid = VGroup(
        Square(side_length=piece_size)
        .move_to((bb_frame[2] + piece_size * x, bb_frame[0] + piece_size * y, 0))
        .set_fill(color=pixel, opacity=1)
        .set_stroke(width=0.5, color=pixel, opacity=1)
        for y in range(image.shape[0])
        for x in range(image.shape[1])
        if (pixel := ManimColor.from_rgba(image[y, x])) is not None and pixel[3] > 0
    )
    return grid


class _Scatter(AnimationGroup):
    def __init__(
        self,
        vmobject: VMobject,
        fill_piece_size: float = 0.05,
        stroke_piece_size: float = 0.01,
        to_scale: typing.Callable[[], float] | None = lambda: 0,
        to_fade: typing.Callable[[], float] | None = lambda: 1,
        shift_strength: typing.Callable[[], float] = lambda: np.random.uniform(0.5, 1.5),
        x_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        z_shift: typing.Callable[[], float] = lambda: 0,
        **kwargs,
    ) -> None:
        fill_pieces = _to_grid(vmobject.copy().set_stroke(opacity=0), piece_size=fill_piece_size)
        stroke_pieces = _to_grid(vmobject.copy().set_fill(opacity=0), piece_size=stroke_piece_size)

        def animate_piece(piece: VMobject):
            animation = piece.animate.shift(
                (
                    shift_strength() * x_shift(),
                    shift_strength() * y_shift(),
                    shift_strength() * z_shift(),
                )
            )
            if to_scale is not None:
                animation = animation.scale(to_scale())
            if to_fade is not None:
                animation = animation.fade(to_fade())
            return animation

        animations = (animate_piece(piece) for piece in [*fill_pieces, *stroke_pieces])
        super().__init__(animations, **kwargs)


class Disintegrate(_Scatter):
    def __init__(self, vmobject: VMobject, **kwargs) -> None:
        self.vmobject = vmobject
        super().__init__(vmobject, **kwargs)

    def begin(self) -> None:
        self.vmobject.set_opacity(0)
        super().begin()

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.vmobject)
        super().clean_up_from_scene(scene)


class Materialize(_Scatter):
    def __init__(self, vmobject: VMobject, **kwargs) -> None:
        rate_func = kwargs.get("rate_func", linear)
        kwargs["rate_func"] = lambda t: 1 - rate_func(t)
        self.vmobject = vmobject
        super().__init__(vmobject, **kwargs)

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.add(self.vmobject)
        return super().clean_up_from_scene(scene)
