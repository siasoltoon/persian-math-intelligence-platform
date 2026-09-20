from persian_math.geometry import Point, Segment, Triangle, distance, triangle_area
from persian_math.input_understanding import detect_ambiguity, detect_intent, understand
from persian_math.ocr import ImageMetadata, ImageQuality, preprocess_plan, validate_image_metadata
from persian_math.ocr_consensus import RecognitionCandidate, consensus


def test_understanding_persian_math():
    result = understand("معادله ۲x + ۳ = ۷ را حل کن")
    assert result.intent.intent == "solve"
    assert result.representation.kind == "equation"
    assert not result.ambiguity


def test_ambiguity_detection():
    assert "unbalanced_parentheses" in detect_ambiguity("(2 + 3")
    assert detect_intent("این را توضیح بده").intent == "explain"


def test_ocr_safety_plan():
    metadata = ImageMetadata(1200, 900, 3, ImageQuality.POOR)
    validate_image_metadata(metadata)
    plan = preprocess_plan(metadata)
    assert "deskew" in plan and "adaptive_threshold" in plan


def test_ocr_consensus_rejects_disagreement():
    result = consensus((
        RecognitionCandidate("2x+3", 0.95, "a"),
        RecognitionCandidate("2x-3", 0.94, "b"),
    ))
    assert not result.accepted


def test_geometry_primitives():
    a, b, c = Point(0, 0), Point(3, 0), Point(0, 4)
    assert Segment(a, b).length == 3
    assert distance(a, c).value == 4
    assert triangle_area(Triangle(a, b, c)).value == 6
