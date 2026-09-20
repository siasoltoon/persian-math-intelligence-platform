from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GraphAxis:
    name: str
    minimum: float
    maximum: float
    label: str = ""


@dataclass(frozen=True)
class GraphPoint:
    x: float
    y: float
    label: str = ""


@dataclass(frozen=True)
class GraphSeries:
    name: str
    points: tuple[GraphPoint, ...]


@dataclass(frozen=True)
class VisualScene:
    points: tuple[object, ...] = ()
    segments: tuple[object, ...] = ()
    circles: tuple[object, ...] = ()
    axes: tuple[GraphAxis, ...] = ()
    series: tuple[GraphSeries, ...] = ()


def validate_scene(scene: VisualScene) -> None:
    if len(scene.axes) not in (0, 2):
        raise ValueError("a Cartesian scene requires zero or two axes")
    for axis in scene.axes:
        if axis.minimum >= axis.maximum:
            raise ValueError("axis minimum must be smaller than maximum")
    for series in scene.series:
        if not series.name.strip():
            raise ValueError("graph series requires a name")
        if not series.points:
            raise ValueError("graph series requires points")


def graph_from_points(name: str, points: tuple[GraphPoint, ...]) -> GraphSeries:
    series = GraphSeries(name, points)
    validate_scene(VisualScene(series=(series,)))
    return series
