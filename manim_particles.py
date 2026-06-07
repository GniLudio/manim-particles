from manim import *
import typing

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
        path_pts = np.array([m.point_from_proportion(t) for t in np.linspace(0, 1, n, endpoint=False)])
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
    return Polygon(*np.vstack([upper, lower[::-1]])).set_stroke(width=0).set_fill(color=color, opacity=opacity)

def _flatten(mob: Mobject) -> VMobject:
    leaves = [_ensure_filled(m) for m in mob.get_family() if len(m.points) > 0]
    if not leaves:
        return mob
    if len(leaves) == 1:
        return leaves[0]
    return Union(*leaves)

class _Scatter(AnimationGroup):
    def __init__(
        self,
        vmobject: VMobject,
        piece_size: float = 0.1,
        to_scale: typing.Callable[[], float] | None = lambda: 0,
        to_fade: typing.Callable[[], float] | None = lambda: 1,
        shift_strength: typing.Callable[[], float] = lambda: np.random.uniform(0.5, 1.5),
        x_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: typing.Callable[[], float] = lambda: np.sin(np.random.uniform(0, 2 * PI)),
        z_shift: typing.Callable[[], float] = lambda: 0,
        **kwargs,
    ) -> None:
        def _intersect(a, b):
            try:
                return Intersection(a, b)
            except Exception:
                return VMobject()

        union = _flatten(vmobject)

        # Render vmobject on a transparent background so each piece can be
        # colored with the actual hue of the region it covers, not a mean average.
        px_arr = np.asarray(vmobject.get_image())  # H × W × 4 RGBA uint8
        img_h, img_w = px_arr.shape[:2]
        fw, fh = config.frame_width, config.frame_height
        fallback_color = _apparent_color(union)
        fallback_opacity = _apparent_opacity(union)

        def _sample(point):
            col = int(np.clip((point[0] + fw / 2) / fw * img_w, 0, img_w - 1))
            row = int(np.clip((fh / 2 - point[1]) / fh * img_h, 0, img_h - 1))
            rgba = px_arr[row, col].astype(float)
            if rgba[3] < 10:
                return rgb_to_color(fallback_color), fallback_opacity
            # un-premultiply: get_image() returns premultiplied RGBA, so dividing
            # RGB by alpha recovers the true color regardless of opacity.
            rgb = np.clip(rgba[:3] / rgba[3], 0, 1)
            return rgb_to_color(rgb), rgba[3] / 255.0

        pieces = VGroup()
        for x in np.arange(vmobject.get_left()[0], vmobject.get_right()[0] + piece_size, piece_size):
            for y in np.arange(vmobject.get_bottom()[1], vmobject.get_top()[1] + piece_size, piece_size):
                piece = _intersect(union, Square(side_length=piece_size).move_to((x, y, 0)))
                if piece.has_points():
                    color, opacity = _sample(piece.get_center())
                    piece.set_stroke(opacity=0).set_fill(color=color, opacity=opacity)
                    pieces.add(piece)

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

        animations = (animate_piece(piece) for piece in pieces)
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