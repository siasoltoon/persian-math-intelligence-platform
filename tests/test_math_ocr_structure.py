from persian_math.math_ocr import analyze_math_structure, structure_to_math_text
from persian_math.ocr import OcrRegion, OcrResult


def test_detects_fraction_structure():
    result = OcrResult(
        "x 2 - 3",
        0.95,
        (
            OcrRegion("2", 0.95, (20, 10, 20, 20)),
            OcrRegion("-", 0.95, (18, 35, 50, 4)),
            OcrRegion("3", 0.95, (20, 45, 20, 20)),
        ),
    )
    structure = analyze_math_structure(result)
    assert structure.fractions == (("2", "3"),)
    assert structure.kind == "fractional_expression"


def test_detects_superscript():
    result = OcrResult(
        "x 2",
        0.95,
        (
            OcrRegion("x", 0.95, (20, 20, 40, 40)),
            OcrRegion("2", 0.95, (58, 5, 15, 15)),
        ),
    )
    structure = analyze_math_structure(result)
    assert structure.superscripts


def test_detects_matrix_like_rows():
    result = OcrResult(
        "1 2\n3 4",
        0.95,
        (
            OcrRegion("1", 0.95, (10, 10, 20, 20)),
            OcrRegion("2", 0.95, (50, 10, 20, 20)),
            OcrRegion("3", 0.95, (10, 50, 20, 20)),
            OcrRegion("4", 0.95, (50, 50, 20, 20)),
        ),
    )
    structure = analyze_math_structure(result)
    assert structure.kind == "matrix_or_table"
    assert structure.rows == (("1", "2"), ("3", "4"))
    assert structure_to_math_text(structure) == "[1, 2; 3, 4]"
