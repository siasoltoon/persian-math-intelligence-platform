import io

import pytest
import sympy as sp
from PIL import Image

from persian_math.canonical import (
    parse_derivative,
    parse_fraction,
    parse_integral,
    parse_limit,
    parse_probability,
    parse_series,
    parse_vector,
)
from persian_math.domain import EducationalLevel, ProblemInput, UserProfile
from persian_math.education import curriculum_for, learning_objectives
from persian_math.geometry import Point, Segment, line_intersection
from persian_math.input_understanding import understand
from persian_math.ocr import (
    ImageMetadata,
    ImageQuality,
    OcrRegion,
    OcrResult,
    preprocess_image,
    reconstruct_math_text,
    validate_image_bytes,
    validate_ocr_result,
)
from persian_math.explanation import explain_solution
from persian_math.ocr_consensus import RecognitionCandidate, consensus
from persian_math.verification import verify_equation_independently
from persian_math.visual_math import GraphAxis, GraphPoint, VisualScene, graph_from_points, validate_scene


def _png_bytes() -> bytes:
    output = io.BytesIO()
    Image.new("RGB", (20, 20), "white").save(output, format="PNG")
    return output.getvalue()


def test_phase_1_to_4_typed_and_independently_verified():
    x = sp.Symbol("x")
    result = verify_equation_independently(x + 2, 5, x, (sp.Integer(3),))
    assert result.verified
    assert "independent_solver_agreement" in result.evidence


def test_phase_2_canonical_mathematical_families():
    x = sp.Symbol("x")
    assert parse_fraction("2/3") == sp.Rational(2, 3)
    assert parse_vector("[1, 2, 3]") == (sp.Integer(1), sp.Integer(2), sp.Integer(3))
    assert parse_derivative("x^3") == 3 * x**2
    assert parse_integral("2*x") == x**2
    assert parse_limit("sin(x)/x") == 1
    assert parse_series("1/(1-x)", order=4) == 1 + x + x**2 + x**3 + sp.Order(x**4)
    assert parse_probability(1, 4) == sp.Rational(1, 4)


def test_phase_5_understanding_domain_coverage():
    result = understand(ProblemInput("گراف و ترکیبیات را توضیح بده"))
    assert result.classification.domain == "discrete_math"


def test_phase_6_ocr_validation_and_reconstruction():
    image = _png_bytes()
    metadata = ImageMetadata(20, 20, 3, ImageQuality.GOOD)
    validate_image_bytes(image)
    prepared = preprocess_image(image, metadata)
    assert prepared
    result = OcrResult(
        "x + 1",
        0.95,
        (OcrRegion("x + 1", 0.95, (0, 0, 20, 20)),),
    )
    validate_ocr_result(result, metadata)
    assert reconstruct_math_text(result, metadata) == "x + 1"


def test_phase_6_rejects_unsafe_resource_inputs():
    with pytest.raises(ValueError):
        validate_image_bytes(b"")
    with pytest.raises(ValueError):
        validate_ocr_result(OcrResult("x", 1.1, ()), ImageMetadata(10, 10, 1))


def test_phase_8_visual_geometry_intersection():
    first = Segment(Point(0, 0), Point(2, 2))
    second = Segment(Point(0, 2), Point(2, 0))
    assert line_intersection(first, second) == Point(1, 1)


def test_phase_10_full_level_coverage():
    for level in EducationalLevel:
        profile = UserProfile("u", level)
        assert curriculum_for(profile).level == level
        assert learning_objectives(profile, "algebra")


def test_phase_10_education_levels_are_distinct():
    assert EducationalLevel.ENTRANCE_EXAM.value == "entrance_exam"



def test_phase_7_rejection_provides_retry_and_clarification():
    result = consensus(
        (
            RecognitionCandidate("2x+3", 0.95, "a"),
            RecognitionCandidate("2x-3", 0.94, "b"),
        )
    )
    assert not result.accepted
    assert result.retry_recommended
    assert result.clarification_fa


def test_phase_8_visual_scene_contract():
    series = graph_from_points("f(x)", (GraphPoint(0, 0), GraphPoint(1, 1)))
    scene = VisualScene(
        axes=(GraphAxis("x", -1, 2, "x"), GraphAxis("y", -1, 2, "y")),
        series=(series,),
    )
    validate_scene(scene)


def test_phase_9_persian_explanation_has_notes_and_mistakes():
    explanation = explain_solution(5, method="symbolic")
    assert explanation.verification_fa is None
    assert explanation.notes_fa
    assert explanation.common_mistakes_fa
