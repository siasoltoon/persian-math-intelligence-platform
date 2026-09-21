from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass

from .ocr import OcrRegion, OcrResult


@dataclass(frozen=True)
class MathToken:
    text: str
    bbox: tuple[int, int, int, int]
    role: str = "inline"


@dataclass(frozen=True)
class MathStructure:
    tokens: tuple[MathToken, ...]
    fractions: tuple[tuple[str, str], ...] = ()
    superscripts: tuple[tuple[str, str], ...] = ()
    subscripts: tuple[tuple[str, str], ...] = ()
    rows: tuple[tuple[str, ...], ...] = ()
    kind: str = "expression"
    confidence: float = 0.0
    warnings: tuple[str, ...] = ()


_MATH_CHARS = re.compile(r"[=+\-*/^<>≤≥√∫∑∏()\[\]{}]|\d|[A-Za-zα-ωΑ-Ω]")


def _center(region: OcrRegion) -> tuple[float, float]:
    x, y, w, h = region.bbox
    return x + w / 2, y + h / 2


def _line_groups(regions: Iterable[OcrRegion]) -> tuple[tuple[OcrRegion, ...], ...]:
    ordered = sorted(regions, key=lambda r: (r.bbox[1], r.bbox[0]))
    lines: list[list[OcrRegion]] = []
    for region in ordered:
        _, cy = _center(region)
        target = None
        for line in reversed(lines[-4:]):
            ref = line[-1]
            _, ref_cy = _center(ref)
            tolerance = max(region.bbox[3], ref.bbox[3]) * 0.65
            if abs(cy - ref_cy) <= max(3.0, tolerance):
                target = line
                break
        if target is None:
            lines.append([region])
        else:
            target.append(region)
    for line in lines:
        line.sort(key=lambda r: r.bbox[0])
    return tuple(tuple(line) for line in lines)


def _contains_math(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if any(ch in stripped for ch in "=+*/^<>√∫∑∏"):
        return True
    return bool(_MATH_CHARS.search(stripped) and any(ch.isdigit() for ch in stripped))


def _relation(a: OcrRegion, b: OcrRegion) -> str:
    ax, ay, aw, ah = a.bbox
    bx, by, _bw, bh = b.bbox
    a_bottom = ay + ah
    b_bottom = by + bh
    if bx < ax + aw * 0.15 or bx > ax + aw * 1.8:
        return "none"
    if by + bh <= ay + ah * 0.72:
        return "superscript"
    if by >= ay + ah * 0.42 and by + bh <= a_bottom + ah * 0.75:
        return "subscript"
    if by < a_bottom and b_bottom > ay and abs((by + b_bottom) / 2 - (ay + a_bottom) / 2) < max(ah, bh):
        return "inline"
    return "none"


def _detect_fraction(regions: tuple[OcrRegion, ...]) -> tuple[tuple[str, str], ...]:
    fractions: list[tuple[str, str]] = []
    for i, bar in enumerate(regions):
        if bar.text.strip() not in {"-", "−", "_", "—"}:
            continue
        bx, by, bw, bh = bar.bbox
        if bw < max(10, bh * 2):
            continue
        above: list[str] = []
        below: list[str] = []
        for j, region in enumerate(regions):
            if i == j:
                continue
            rx, ry, rw, rh = region.bbox
            overlap = max(0, min(bx + bw, rx + rw) - max(bx, rx))
            if overlap < 0.35 * min(bw, rw):
                continue
            if ry + rh <= by and by - (ry + rh) <= max(3, 1.5 * max(rh, bh)):
                above.append(region.text.strip())
            elif ry >= by + bh and ry - (by + bh) <= max(3, 1.5 * max(rh, bh)):
                below.append(region.text.strip())
        if above and below:
            fractions.append((" ".join(above), " ".join(below)))
    return tuple(fractions)


def analyze_math_structure(result: OcrResult) -> MathStructure:
    regions = tuple(r for r in result.regions if r.text.strip())
    if not regions:
        return MathStructure((), confidence=0.0, warnings=("no_regions",))

    lines = _line_groups(regions)
    tokens = tuple(
        MathToken(r.text.strip(), r.bbox)
        for r in sorted(regions, key=lambda r: (r.bbox[1], r.bbox[0]))
    )
    supers: list[tuple[str, str]] = []
    subs: list[tuple[str, str]] = []
    for a in regions:
        for b in regions:
            if a is b:
                continue
            relation = _relation(a, b)
            if relation == "superscript":
                supers.append((a.text.strip(), b.text.strip()))
            elif relation == "subscript":
                subs.append((a.text.strip(), b.text.strip()))

    fractions = _detect_fraction(regions)
    row_values = tuple(tuple(r.text.strip() for r in line) for line in lines)
    columns = max((len(line) for line in lines), default=0)
    matrix_like = len(lines) >= 2 and columns >= 2 and all(
        abs(len(line) - columns) <= 1 for line in lines
    )
    math_density = sum(_contains_math(r.text) for r in regions) / len(regions)
    warnings: list[str] = []
    if result.confidence < 0.70:
        warnings.append("ocr_confidence_below_structure_threshold")
    if len(regions) > 80:
        warnings.append("high_region_count_review_recommended")
    if matrix_like:
        kind = "matrix_or_table"
    elif fractions:
        kind = "fractional_expression"
    elif supers or subs:
        kind = "indexed_or_powered_expression"
    elif math_density >= 0.45:
        kind = "mathematical_expression"
    else:
        kind = "mixed_text_math"

    structural_signal = 0.0
    structural_signal += min(0.35, math_density * 0.35)
    structural_signal += 0.25 if fractions else 0.0
    structural_signal += 0.20 if supers or subs else 0.0
    structural_signal += 0.20 if matrix_like else 0.0
    confidence = min(result.confidence, max(0.0, 0.35 + structural_signal))
    return MathStructure(
        tokens=tokens,
        fractions=fractions,
        superscripts=tuple(dict.fromkeys(supers)),
        subscripts=tuple(dict.fromkeys(subs)),
        rows=row_values if matrix_like else (),
        kind=kind,
        confidence=confidence,
        warnings=tuple(warnings),
    )


def structure_to_math_text(structure: MathStructure) -> str:
    if not structure.tokens:
        return ""
    if structure.kind == "matrix_or_table" and structure.rows:
        return "[" + "; ".join(", ".join(row) for row in structure.rows) + "]"
    return " ".join(token.text for token in structure.tokens)
