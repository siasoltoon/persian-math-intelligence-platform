import pytest

from persian_math.canonical import parse_expression


def test_parser_rejects_python_syntax() -> None:
    with pytest.raises(ValueError):
        parse_expression("__import__('os').system('echo unsafe')")


def test_parser_keeps_supported_math() -> None:
    result = parse_expression("۲x² + ۳")
    assert str(result.expression) == "2*x**2 + 3"
