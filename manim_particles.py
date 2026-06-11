from manim import *
from typing import Callable
from PIL import Image

__all__ = ["Disintegrate", "Materialize"]


def _to_grid(mob: VMobject, cell_size: float) -> VMobject:
    stroke_one_px = config.frame_width / config.pixel_width * 100
    stroke_width = 0.01 * mob.get_stroke_width()
    left, right, bottom, top = (
        mob.get_left()[0] - 0.5 * stroke_width,
        mob.get_right()[0] + 0.5 * stroke_width,
        mob.get_bottom()[1] - 0.5 * stroke_width,
        mob.get_top()[1] + 0.5 * stroke_width,
    )
    width, height = right - left, top - bottom
    resolution = (max(int(width / cell_size), 1), max(1, int(height / cell_size)))
    image = np.asarray(Image.fromarray(_to_image(mob)).resize(size=resolution, resample=Image.Resampling.NEAREST))
    cell_height, cell_width = height / image.shape[0], width / image.shape[1]
    image = np.flipud(image)
    return VGroup(
        Rectangle(
            width=cell_height,
            height=cell_width,
            stroke_width=stroke_one_px,
            color=ManimColor.from_rgba(pixel),
            fill_opacity=pixel[3] / 255,
            stroke_opacity=pixel[3] / 255,
        ).move_to((left + (x + 0.5) * cell_width, bottom + (y + 0.5) * cell_height, 0))
        for y in range(image.shape[0])
        for x in range(image.shape[1])
        if (pixel := image[y, x]) is not None and pixel[3] > 0
    )


def _to_image(mob: VMobject) -> np.ndarray:
    stroke_offset = 0.5 * 0.01 * mob.get_stroke_width()
    width = mob.width + 2 * stroke_offset
    height = mob.height + 2 * stroke_offset
    if not width or not height:
        return np.zeros((0, 0, 4), dtype=np.uint8)
    image = np.asarray(mob.get_image(Camera(frame_center=mob.get_center(), background_opacity=0)))
    width_px = width * config.pixel_width / config.frame_width
    height_px = height * config.pixel_height / config.frame_height
    image = image[
        int((image.shape[0] - height_px) / 2) : int((image.shape[0] + height_px) / 2),
        int((image.shape[1] - width_px) / 2) : int((image.shape[1] + width_px) / 2),
    ]
    return image


class _Scatter(AnimationGroup):
    """The scatter animation.

    Parameters
    ----------
    vmobject : VMobject
        The object to the scattered.
    piece_size: float | tuple[float, float]
        The piece size. A tuple can be passed to handle the fill and stroke area separately. Defaults to `(0.1, 0.025)`.
    to_scale : Callable[[VGroup, VMobject], float]
        The target scale factor for each piece. Defaults to `0`.
    to_fade : Callable[[VGroup, VMobject], float]
        The target fade for each piece. Defaults to `1`.
    scatter_distance : Callable[[VGroup, VMobject], float]
        The distance each particle moves. Defaults to `np.random.uniform(0.5, 1.5)`.
    x_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the x-direction. Defaults to `lambda:np.sin(np.random.uniform(0, 2 * PI))`
    y_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the y-direction. Defaults to `np.sin(np.random.uniform(0, 2 * PI))`
    reverse : bool
        Whether to play the animation in reverse. Defaults to `False`.
    """

    def __init__(
        self,
        vmobject: VMobject,
        piece_size: float | tuple[float, float] = (0.1, 0.025),
        to_scale: Callable[[VGroup, VMobject], float] | None = lambda *_: 0,
        to_fade: Callable[[VGroup, VMobject], float] | None = lambda *_: 1,
        scatter_distance: Callable[[VGroup, VMobject], float] = lambda *_: np.random.uniform(0.5, 1.5),
        x_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        reverse: bool = False,
        **kwargs,
    ) -> None:
        self.vmobject = vmobject
        self.reverse = reverse
        if reverse:
            rate_func = kwargs.get("rate_func", linear)
            kwargs["rate_func"] = lambda t: 1 - rate_func(t)

        if isinstance(piece_size, tuple):
            self.pieces = VGroup(
                *_to_grid(vmobject.copy().set_stroke(opacity=0), cell_size=piece_size[0]),
                *_to_grid(vmobject.copy().set_fill(opacity=0), cell_size=piece_size[1]),
            )
        else:
            self.pieces = VGroup(
                *_to_grid(vmobject, cell_size=piece_size),
            )

        def animate_piece(piece: VMobject):
            animation = piece.animate.shift(
                (
                    scatter_distance(self.pieces, piece) * x_shift(self.pieces, piece),
                    scatter_distance(self.pieces, piece) * y_shift(self.pieces, piece),
                    0,
                )
            )
            if to_scale is not None:
                animation = animation.scale(to_scale(self.pieces, piece))
            if to_fade is not None:
                animation = animation.fade(to_fade(self.pieces, piece))
            return animation

        animations = [animate_piece(piece) for piece in self.pieces]
        super().__init__(animations, group=self.pieces, **kwargs)

    def begin(self) -> None:
        if not self.reverse:
            self.vmobject.set_opacity(0)
        super().begin()

    def clean_up_from_scene(self, scene: Scene) -> None:
        if not self.reverse:
            scene.remove(self.vmobject)
        else:
            scene.add(self.vmobject)

        super().clean_up_from_scene(scene)


class Disintegrate(_Scatter):
    """Disintegrates an object into small pieces.

    Parameters
    ----------
    vmobject : VMobject
        The object to the scattered.
    piece_size: float | tuple[float, float]
        The piece size. A tuple can be passed to handle the fill and stroke area separately. Defaults to `(0.1, 0.025)`.
    to_scale : Callable[[VGroup, VMobject], float]
        The target scale factor for each piece. Defaults to `0`.
    to_fade : Callable[[VGroup, VMobject], float]
        The target fade for each piece. Defaults to `1`.
    scatter_distance : Callable[[VGroup, VMobject], float]
        The distance each particle moves. Defaults to `np.random.uniform(0.5, 1.5)`.
    x_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the x-direction. Defaults to `lambda:np.sin(np.random.uniform(0, 2 * PI))`
    y_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the y-direction. Defaults to `np.sin(np.random.uniform(0, 2 * PI))`
    """

    def __init__(
        self,
        vmobject: VMobject,
        piece_size: float | tuple[float, float] = (0.1, 0.025),
        to_scale: Callable[[VGroup, VMobject], float] | None = lambda *_: 0,
        to_fade: Callable[[VGroup, VMobject], float] | None = lambda *_: 1,
        scatter_distance: Callable[[VGroup, VMobject], float] = lambda *_: np.random.uniform(0.5, 1.5),
        x_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        **kwargs,
    ) -> None:
        super().__init__(
            vmobject=vmobject,
            piece_size=piece_size,
            to_scale=to_scale,
            to_fade=to_fade,
            scatter_distance=scatter_distance,
            x_shift=x_shift,
            y_shift=y_shift,
            reverse=False,
            **kwargs,
        )


class Materialize(_Scatter):
    """Materializes an object from small pieces.

    Parameters
    ----------
    vmobject : VMobject
        The object to the scattered.
    piece_size: float | tuple[float, float]
        The piece size. A tuple can be passed to handle the fill and stroke area separately. Defaults to `(0.1, 0.025)`.
    to_scale : Callable[[VGroup, VMobject], float]
        The target scale factor for each piece. Defaults to `0`.
    to_fade : Callable[[VGroup, VMobject], float]
        The target fade for each piece. Defaults to `1`.
    scatter_distance : Callable[[VGroup, VMobject], float]
        The distance each particle moves. Defaults to `np.random.uniform(0.5, 1.5)`.
    x_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the x-direction. Defaults to `lambda:np.sin(np.random.uniform(0, 2 * PI))`
    y_shift : Callable[[VGroup, VMobject], float]
        How much a piece shifts in the y-direction. Defaults to `np.sin(np.random.uniform(0, 2 * PI))`
    """

    def __init__(
        self,
        vmobject: VMobject,
        piece_size: float | tuple[float, float] = (0.1, 0.025),
        to_scale: Callable[[VGroup, VMobject], float] | None = lambda *_: 0,
        to_fade: Callable[[VGroup, VMobject], float] | None = lambda *_: 1,
        scatter_distance: Callable[[VGroup, VMobject], float] = lambda *_: np.random.uniform(0.5, 1.5),
        x_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        y_shift: Callable[[VGroup, VMobject], float] = lambda *_: np.sin(np.random.uniform(0, 2 * PI)),
        **kwargs,
    ) -> None:
        super().__init__(
            vmobject=vmobject,
            piece_size=piece_size,
            to_scale=to_scale,
            to_fade=to_fade,
            scatter_distance=scatter_distance,
            x_shift=x_shift,
            y_shift=y_shift,
            reverse=True,
            **kwargs,
        )
