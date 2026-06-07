from manim import *
from manim_particles import Materialize, Disintegrate

TESTS = [
    "test_00_null_test",
    "test_01_hello",
    "test_02_single_char",
    "test_03_blue_square",
    "test_04_line",
    "test_05_red_arrow",
    "test_06_curved_arrow",
    "test_07_purple_polygon",
    "test_08_cyan_pentagon",
    "test_09_orange_arc",
    "test_10_sine_curve",
    "test_11_number_line",
    "test_12_pink_star",
    "test_13_axes_parabola",
    "test_14_rainbow_text",
    "test_15_rainbow_mathtex",
    "test_16_solid_colored_squares",
    "test_17_mixed_filled_stroked_squares",
    "test_18_colored_circles",
    "test_19_multicolor_shapes",
    "test_20_stroke_squares_multicolor",
    "test_21_stroke_circles_multicolor",
    "test_22_stroke_shapes_multicolor",
    "test_23_stroke_lines_multicolor",
]


class TestScene(Scene):
    def construct(self):
        self.run_all_tests()
        # self.run_test_numbers(23)

    def run_test_numbers(self, *nums):
        for num in nums:
            getattr(self, TESTS[num])()
            self.clear()

    def run_all_tests(self):
        for name in TESTS:
            getattr(self, name)()
            self.clear()

    def test_00_null_test(self):
        pass

    def test_01_hello(self):
        text = Text("Hello", font_size=100).set_opacity(0.66).to_edge(UP)
        self.play(Materialize(text))
        self.wait(0.5)
        self.play(Disintegrate(text), run_time=1.4)
        self.wait(0.5)

    def test_02_single_char(self):
        text = Text("G", font_size=100).set_opacity(0.33)
        self.play(Materialize(text), run_time=1.4)
        self.wait(0.5)
        self.play(Disintegrate(text))
        self.wait(0.5)

    def test_03_blue_square(self):
        my_square = Square(fill_opacity=1).set_fill(BLUE_C)
        self.play(Materialize(my_square))
        self.wait(0.5)
        self.play(Disintegrate(my_square))
        self.wait(0.5)

    def test_04_line(self):
        my_line = Line().shift(UR * 1.3)
        self.play(Materialize(my_line))
        self.wait(0.5)
        self.play(Disintegrate(my_line))
        self.wait(0.5)

    def test_05_red_arrow(self):
        my_arrow = Arrow(LEFT * 2, RIGHT * 2, color=RED)
        self.play(Materialize(my_arrow))
        self.wait(0.5)
        self.play(Disintegrate(my_arrow))
        self.wait(0.5)

    def test_06_curved_arrow(self):
        my_curved_arrow = (
            CurvedArrow(LEFT * 2 + DOWN, RIGHT * 2 + UP, color=BLUE_B).set_opacity(0.7).shift(LEFT)
        )
        self.play(Materialize(my_curved_arrow))
        self.wait(0.5)
        self.play(Disintegrate(my_curved_arrow))
        self.wait(0.5)

    def test_07_purple_polygon(self):
        my_polygon = (
            Polygon(UP * 2, RIGHT * 1.5 + UP * 0.5, RIGHT * 2 + DOWN, DOWN * 1.5, LEFT * 2)
            .set_fill(PURPLE, opacity=0.5)
            .set_stroke(WHITE, width=2)
        )
        self.play(Materialize(my_polygon))
        self.wait(0.5)
        self.play(Disintegrate(my_polygon))
        self.wait(0.5)

    def test_08_cyan_pentagon(self):
        my_pentagon = (
            RegularPolygon(n=5).scale(2).set_stroke(PURE_CYAN, width=4).set_fill(opacity=0)
        )
        self.play(Materialize(my_pentagon))
        self.wait(0.5)
        self.play(Disintegrate(my_pentagon))
        self.wait(0.5)

    def test_09_orange_arc(self):
        my_arc = Arc(radius=2, start_angle=0, angle=3 * PI / 2).set_stroke(ORANGE, width=5)
        self.play(Materialize(my_arc))
        self.wait(0.5)
        self.play(Disintegrate(my_arc))
        self.wait(0.5)

    def test_10_sine_curve(self):
        my_sine = FunctionGraph(lambda x: np.sin(x), x_range=[-PI, PI]).set_stroke(TEAL, width=4)
        self.play(Materialize(my_sine))
        self.wait(0.5)
        self.play(Disintegrate(my_sine))
        self.wait(0.5)

    def test_11_number_line(self):
        my_number_line = NumberLine(x_range=[-3, 3], length=8, color=YELLOW)
        self.play(Materialize(my_number_line))
        self.wait(0.5)
        self.play(Disintegrate(my_number_line))
        self.wait(0.5)

    def test_12_pink_star(self):
        my_star = Star(n=5, outer_radius=1.5).set_fill(PINK, opacity=1).set_stroke(width=0)
        self.play(Materialize(my_star))
        self.wait(0.5)
        self.play(Disintegrate(my_star))
        self.wait(0.5)

    def test_13_axes_parabola(self):
        my_axes = Axes(x_range=[-2, 2], y_range=[-1, 4], x_length=6, y_length=4)
        my_parabola = my_axes.plot(lambda x: x**2, color=MAROON)
        self.play(Materialize(VGroup(my_axes, my_parabola)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(my_axes, my_parabola)))
        self.wait(0.5)

    def test_14_rainbow_text(self):
        my_text = (
            Text("Rainbow", font_size=100)
            .set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
            .to_corner(DL)
        )
        self.play(Materialize(my_text))
        self.wait(0.5)
        self.play(Disintegrate(my_text))
        self.wait(0.5)

    def test_15_rainbow_mathtex(self):
        my_tex = MathTex(r"E = mc^2").scale(3).set_color_by_gradient(RED, YELLOW, GREEN, BLUE)
        self.play(Materialize(my_tex))
        self.wait(0.5)
        self.play(Disintegrate(my_tex))
        self.wait(0.5)

    def test_16_solid_colored_squares(self):
        squares = VGroup(
            Square(fill_opacity=1).set_fill(RED).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(ORANGE).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(YELLOW).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(GREEN).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(BLUE).set_stroke(width=0),
            Square(fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_17_mixed_filled_stroked_squares(self):
        squares = VGroup(
            Square(fill_opacity=1).set_fill(RED_C).set_stroke(width=0),
            Square().set_stroke(GREEN, width=4).set_fill(opacity=0),
            Square(fill_opacity=0.6).set_fill(BLUE_C).set_stroke(YELLOW, width=2),
            Square().set_stroke(ORANGE, width=4).set_fill(opacity=0),
            Square(fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
            Square(fill_opacity=0.4).set_fill(TEAL).set_stroke(WHITE, width=3),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_18_colored_circles(self):
        circles = VGroup(
            Circle(radius=0.6, fill_opacity=1).set_fill(RED).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(ORANGE).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(YELLOW).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(GREEN).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(BLUE).set_stroke(width=0),
            Circle(radius=0.6, fill_opacity=1).set_fill(PURPLE).set_stroke(width=0),
        ).arrange(RIGHT, buff=0.15)
        self.play(Materialize(circles))
        self.wait(0.5)
        self.play(Disintegrate(circles))
        self.wait(0.5)

    def test_19_multicolor_shapes(self):
        shapes = VGroup(
            Triangle().scale(1.5).set_fill(RED_C, opacity=0.9).set_stroke(WHITE, width=1),
            RegularPolygon(n=6)
            .scale(1.5)
            .set_fill(GREEN_C, opacity=0.9)
            .set_stroke(WHITE, width=1),
            Star(n=5, outer_radius=1.5).set_fill(YELLOW, opacity=0.9).set_stroke(WHITE, width=1),
            RegularPolygon(n=8).scale(1.5).set_fill(BLUE_C, opacity=0.9).set_stroke(WHITE, width=1),
        ).arrange(RIGHT, buff=0.3)
        self.play(Materialize(shapes))
        self.wait(0.5)
        self.play(Disintegrate(shapes))
        self.wait(0.5)

    def test_20_stroke_squares_multicolor(self):
        squares = VGroup(
            Square().set_stroke(RED, width=6).set_fill(opacity=0),
            Square().set_stroke(ORANGE, width=6, opacity=0.8).set_fill(opacity=0),
            Square().set_stroke(YELLOW, width=6, opacity=0.6).set_fill(opacity=0),
            Square().set_stroke(GREEN, width=6, opacity=0.4).set_fill(opacity=0),
            Square().set_stroke(BLUE, width=6).set_fill(opacity=0),
            Square().set_stroke(PURPLE, width=6, opacity=0.7).set_fill(opacity=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(squares))
        self.wait(0.5)
        self.play(Disintegrate(squares))
        self.wait(0.5)

    def test_21_stroke_circles_multicolor(self):
        circles = (
            VGroup(
                Circle(radius=0.6).set_stroke(TEAL, width=3).set_fill(opacity=0),
                Circle(radius=0.6).set_stroke(PINK, width=5, opacity=0.9).set_fill(opacity=0),
                Circle(radius=0.6).set_stroke(GOLD, width=8, opacity=0.6).set_fill(opacity=0),
                Circle(radius=0.6).set_stroke(MAROON, width=4, opacity=0.8).set_fill(opacity=0),
                Circle(radius=0.6)
                .set_stroke(LIGHT_BROWN, width=6, opacity=0.5)
                .set_fill(opacity=0),
            )
            .arrange(RIGHT, buff=0.25)
            .to_corner(UL)
        )
        self.play(Materialize(circles))
        self.wait(0.5)
        self.play(Disintegrate(circles))
        self.wait(0.5)

    def test_22_stroke_shapes_multicolor(self):
        shapes = VGroup(
            Triangle().scale(1.3).set_stroke(RED_C, width=5).set_fill(opacity=0),
            RegularPolygon(n=5)
            .scale(1.3)
            .set_stroke(PURE_GREEN, width=4, opacity=0.7)
            .set_fill(opacity=0),
            Star(n=5, outer_radius=1.3)
            .set_stroke(YELLOW, width=3, opacity=0.5)
            .set_fill(opacity=0),
            RegularPolygon(n=6)
            .scale(1.3)
            .set_stroke(BLUE_C, width=6, opacity=0.9)
            .set_fill(opacity=0),
            Arc(radius=1.2, angle=3 * PI / 2)
            .set_stroke(ORANGE, width=5, opacity=0.8)
            .set_fill(opacity=0),
        ).arrange(RIGHT, buff=0.2)
        self.play(Materialize(shapes))
        self.wait(0.5)
        self.play(Disintegrate(shapes))
        self.wait(0.5)

    def test_23_stroke_lines_multicolor(self):
        lines = VGroup(
            Line(stroke_width=23).scale(1.3).set_stroke(RED_C, width=5).set_fill(opacity=0),
            Line().scale(1.3).set_stroke(PURE_GREEN, width=4, opacity=0.7).set_fill(opacity=0),
            Line().set_stroke(YELLOW, width=3, opacity=0.5).set_fill(opacity=0),
            Line().scale(1.3).set_stroke(BLUE_C, width=6, opacity=0.9).set_fill(opacity=0),
            Line().set_stroke(ORANGE, width=5, opacity=0.8).set_fill(opacity=0),
        ).arrange(DOWN, buff=0.2)
        self.play(Materialize(lines))
        self.wait(0.5)
        self.play(Disintegrate(lines))
        self.wait(0.5)


# --- Check that TESTS array is correct ---
_ALL_TESTS = sorted(name for name in vars(TestScene) if name.startswith("test_"))
_missing_from_list = set(_ALL_TESTS) - set(TESTS)
_missing_from_class = set(TESTS) - set(_ALL_TESTS)
if _missing_from_list or _missing_from_class:
    msg = "TESTS list is out of sync with TestScene methods."
    if _missing_from_list:
        msg += f"\n  Defined in class but absent from TESTS: {sorted(_missing_from_list)}"
    if _missing_from_class:
        msg += f"\n  Listed in TESTS but missing from class: {sorted(_missing_from_class)}"
    raise RuntimeError(msg)


TESTS_3D = [
    "test_00_3d_sphere",  # Fails
    "test_01_3d_cube",
    "test_02_3d_cylinder",
    "test_03_3d_cone",
    "test_04_3d_torus",
    "test_05_3d_axes",
    "test_06_3d_line",
    "test_07_3d_arrow",
    "test_08_3d_plane",
    "test_09_3d_paraboloid",
    "test_10_3d_saddle",
    "test_11_3d_sine_surface",
    "test_12_3d_axes_with_plot",
    "test_13_3d_colored_solids",
    "test_14_3d_platonic_solids",
    "test_15_3d_sphere_wireframe",
]


class Test3DScene(ThreeDScene):
    def construct(self):
        self.run_all_tests()
        # self.run_test_numbers(0)

    def run_test_numbers(self, *nums):
        for num in nums:
            getattr(self, TESTS_3D[num])()
            self.clear()

    def run_all_tests(self):
        for name in TESTS_3D:
            getattr(self, name)()
            self.clear()

    def _setup_camera(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

    def test_00_3d_sphere(self):
        self._setup_camera()
        sphere = Sphere(radius=1.5).set_color(BLUE_C).set_opacity(0.9)
        self.play(Materialize(sphere))
        self.wait(0.5)
        self.play(Disintegrate(sphere))
        self.wait(0.5)

    def test_01_3d_cube(self):
        self._setup_camera()
        cube = Cube(side_length=2).set_color(RED_C).set_opacity(0.85)
        self.play(Materialize(cube))
        self.wait(0.5)
        self.play(Disintegrate(cube))
        self.wait(0.5)

    def test_02_3d_cylinder(self):
        self._setup_camera()
        cylinder = Cylinder(radius=1, height=2.5).set_color(GREEN_C).set_opacity(0.85)
        self.play(Materialize(cylinder))
        self.wait(0.5)
        self.play(Disintegrate(cylinder))
        self.wait(0.5)

    def test_03_3d_cone(self):
        self._setup_camera()
        cone = Cone(base_radius=1.2, height=2.5).set_color(ORANGE).set_opacity(0.85)
        self.play(Materialize(cone))
        self.wait(0.5)
        self.play(Disintegrate(cone))
        self.wait(0.5)

    def test_04_3d_torus(self):
        self._setup_camera()
        torus = Torus(major_radius=1.2, minor_radius=0.4).set_color(PURPLE).set_opacity(0.9)
        self.play(Materialize(torus))
        self.wait(0.5)
        self.play(Disintegrate(torus))
        self.wait(0.5)

    def test_05_3d_axes(self):
        self._setup_camera()
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        labels = axes.get_axis_labels(
            Text("x").scale(0.6), Text("y").scale(0.6), Text("z").scale(0.6)
        )
        self.play(Materialize(VGroup(axes, labels)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(axes, labels)))
        self.wait(0.5)

    def test_06_3d_line(self):
        self._setup_camera()
        lines = VGroup(
            Line3D(start=LEFT * 2 + IN, end=RIGHT * 2 + OUT, color=TEAL),
            Line3D(start=DOWN * 2 + LEFT, end=UP * 2 + RIGHT, color=PINK),
            Line3D(start=OUT * 2 + DOWN, end=IN * 2 + UP, color=GOLD),
        )
        self.play(Materialize(lines))
        self.wait(0.5)
        self.play(Disintegrate(lines))
        self.wait(0.5)

    def test_07_3d_arrow(self):
        self._setup_camera()
        arrows = VGroup(
            Arrow3D(start=ORIGIN, end=RIGHT * 2, color=RED),
            Arrow3D(start=ORIGIN, end=UP * 2, color=GREEN),
            Arrow3D(start=ORIGIN, end=OUT * 2, color=BLUE),
        )
        self.play(Materialize(arrows))
        self.wait(0.5)
        self.play(Disintegrate(arrows))
        self.wait(0.5)

    def test_08_3d_plane(self):
        self._setup_camera()
        plane = (
            Surface(
                lambda u, v: np.array([u, v, 0]),
                u_range=[-2.5, 2.5],
                v_range=[-2.5, 2.5],
                resolution=(8, 8),
            )
            .set_color(BLUE_B)
            .set_opacity(0.6)
        )
        grid = NumberPlane(x_range=[-3, 3], y_range=[-3, 3]).set_opacity(0.4)
        self.play(Materialize(VGroup(plane, grid)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(plane, grid)))
        self.wait(0.5)

    def test_09_3d_paraboloid(self):
        self._setup_camera()
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[0, 4],
            x_length=5,
            y_length=5,
            z_length=4,
        )
        surface = axes.plot_surface(
            lambda x, y: x**2 + y**2,
            x_range=[-1.8, 1.8],
            y_range=[-1.8, 1.8],
            colorscale=[BLUE, TEAL, GREEN, YELLOW],
        )
        self.play(Materialize(VGroup(axes, surface)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(axes, surface)))
        self.wait(0.5)

    def test_10_3d_saddle(self):
        self._setup_camera()
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-2, 2],
            x_length=5,
            y_length=5,
            z_length=4,
        )
        surface = axes.plot_surface(
            lambda x, y: x**2 - y**2,
            x_range=[-1.5, 1.5],
            y_range=[-1.5, 1.5],
            colorscale=[BLUE, WHITE, RED],
        )
        self.play(Materialize(VGroup(axes, surface)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(axes, surface)))
        self.wait(0.5)

    def test_11_3d_sine_surface(self):
        self._setup_camera()
        axes = ThreeDAxes(
            x_range=[-PI, PI],
            y_range=[-PI, PI],
            z_range=[-1, 1],
            x_length=6,
            y_length=6,
            z_length=3,
        )
        surface = axes.plot_surface(
            lambda x, y: np.sin(x) * np.cos(y),
            x_range=[-PI, PI],
            y_range=[-PI, PI],
            colorscale=[PURPLE, BLUE, TEAL, GREEN, YELLOW, ORANGE, RED],
        )
        self.play(Materialize(VGroup(axes, surface)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(axes, surface)))
        self.wait(0.5)

    def test_12_3d_axes_with_plot(self):
        self._setup_camera()
        axes = ThreeDAxes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            z_range=[-1, 1],
            x_length=5,
            y_length=5,
            z_length=3,
        )
        curve = ParametricFunction(
            lambda t: axes.c2p(t, np.sin(2 * t), np.cos(3 * t)),
            t_range=[-PI, PI],
            color=YELLOW,
            stroke_width=4,
        )
        surface = axes.plot_surface(
            lambda x, y: np.exp(-(x**2 + y**2)),
            x_range=[-2, 2],
            y_range=[-2, 2],
            colorscale=[BLUE_E, TEAL, GREEN_B],
            opacity=0.7,
        )
        self.play(Materialize(VGroup(axes, surface, curve)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(axes, surface, curve)))
        self.wait(0.5)

    def test_13_3d_colored_solids(self):
        self._setup_camera()
        solids = VGroup(
            Sphere(radius=0.6).set_color(RED).set_opacity(0.9).shift(LEFT * 2.5),
            Cube(side_length=1.1).set_color(ORANGE).set_opacity(0.9),
            Cylinder(radius=0.5, height=1.2).set_color(GREEN).set_opacity(0.9).shift(RIGHT * 2.5),
        )
        self.play(Materialize(solids))
        self.wait(0.5)
        self.play(Disintegrate(solids))
        self.wait(0.5)

    def test_14_3d_platonic_solids(self):
        self._setup_camera()
        solids = VGroup(
            Tetrahedron().scale(0.8).set_color(RED_C).set_opacity(0.235).shift(LEFT * 3),
            Octahedron().scale(0.8).set_color(GREEN_C).set_opacity(0.85).shift(LEFT * 1),
            Icosahedron().scale(0.8).set_color(BLUE_C).set_opacity(0.5).shift(RIGHT * 1),
            Dodecahedron().scale(0.8).set_color(PURPLE).set_opacity(0.85).shift(RIGHT * 3),
        )
        self.play(Materialize(solids))
        self.wait(0.5)
        self.play(Disintegrate(solids))
        self.wait(0.5)

    def test_15_3d_sphere_wireframe(self):
        self._setup_camera()
        sphere = Sphere(radius=1.5).set_color(TEAL).set_opacity(0.15)
        wireframe = (
            Surface(
                lambda u, v: np.array(
                    [
                        1.5 * np.cos(u) * np.sin(v),
                        1.5 * np.sin(u) * np.sin(v),
                        1.5 * np.cos(v),
                    ]
                ),
                u_range=[0, TAU],
                v_range=[0, PI],
                resolution=(12, 8),
            )
            .set_stroke(TEAL, width=1, opacity=0.8)
            .set_fill(opacity=0)
        )
        self.play(Materialize(VGroup(sphere, wireframe)))
        self.wait(0.5)
        self.play(Disintegrate(VGroup(sphere, wireframe)))
        self.wait(0.5)


# --- Check that TESTS_3D array is correct ---
_ALL_TESTS_3D = sorted(name for name in vars(Test3DScene) if name.startswith("test_"))
_missing_from_list_3d = set(_ALL_TESTS_3D) - set(TESTS_3D)
_missing_from_class_3d = set(TESTS_3D) - set(_ALL_TESTS_3D)
if _missing_from_list_3d or _missing_from_class_3d:
    msg = "TESTS_3D list is out of sync with Test3DScene methods."
    if _missing_from_list_3d:
        msg += f"\n  Defined in class but absent from TESTS_3D: {sorted(_missing_from_list_3d)}"
    if _missing_from_class_3d:
        msg += f"\n  Listed in TESTS_3D but missing from class: {sorted(_missing_from_class_3d)}"
    raise RuntimeError(msg)
