from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees, hypot, pi


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return hypot(self.end.x - self.start.x, self.end.y - self.start.y)


@dataclass(frozen=True)
class Triangle:
    a: Point
    b: Point
    c: Point


@dataclass(frozen=True)
class Circle:
    center: Point
    radius: float


@dataclass(frozen=True)
class GeometryResult:
    value: float
    method: str
    verified: bool


def distance(a: Point, b: Point) -> GeometryResult:
    return GeometryResult(hypot(b.x - a.x, b.y - a.y), "euclidean_distance", True)


def triangle_area(triangle: Triangle) -> GeometryResult:
    value = (
        abs(
            triangle.a.x * (triangle.b.y - triangle.c.y)
            + triangle.b.x * (triangle.c.y - triangle.a.y)
            + triangle.c.x * (triangle.a.y - triangle.b.y)
        )
        / 2
    )
    return GeometryResult(value, "shoelace_area", True)


def triangle_is_degenerate(triangle: Triangle) -> bool:
    return triangle_area(triangle).value == 0


def circle_area(circle: Circle) -> GeometryResult:
    if circle.radius < 0:
        raise ValueError("radius must be non-negative")
    return GeometryResult(pi * circle.radius**2, "circle_area", True)


def circle_circumference(circle: Circle) -> GeometryResult:
    if circle.radius < 0:
        raise ValueError("radius must be non-negative")
    return GeometryResult(2 * pi * circle.radius, "circle_circumference", True)


def angle_degrees(vertex: Point, first: Point, second: Point) -> GeometryResult:
    ax, ay = first.x - vertex.x, first.y - vertex.y
    bx, by = second.x - vertex.x, second.y - vertex.y
    if (ax == 0 and ay == 0) or (bx == 0 and by == 0):
        raise ValueError("angle requires distinct points")
    value = abs(degrees(atan2(ay, ax) - atan2(by, bx))) % 360
    return GeometryResult(min(value, 360 - value), "coordinate_angle", True)


def line_intersection(first: Segment, second: Segment) -> Point | None:
    x1, y1 = first.start.x, first.start.y
    x2, y2 = first.end.x, first.end.y
    x3, y3 = second.start.x, second.start.y
    x4, y4 = second.end.x, second.end.y
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        return None
    determinant1 = x1 * y2 - y1 * x2
    determinant2 = x3 * y4 - y3 * x4
    px = (determinant1 * (x3 - x4) - (x1 - x2) * determinant2) / denominator
    py = (determinant1 * (y3 - y4) - (y1 - y2) * determinant2) / denominator
    return Point(px, py)
