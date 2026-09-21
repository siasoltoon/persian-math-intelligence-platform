from __future__ import annotations

import sympy as sp

from persian_math.adversarial import run_adversarial
from persian_math.benchmark import BenchmarkCase, pass_rate, run_benchmark
from persian_math.ocr_benchmark import OcrBenchmarkCase, aggregate, score_case
from persian_math.production import (
    ProductionConfig,
    RecoveryPlan,
    validate_config,
    validate_recovery,
)
from persian_math.quality import FailurePolicy, TestCase, retry, run_matrix
from persian_math.quality import pass_rate as matrix_rate
from persian_math.release_audit import REQUIRED_AREAS, build_audit
from persian_math.ux import render_answer


def test_phase_19_failure_matrix_and_retry():
    results = run_matrix(
        (
            TestCase("ok", "unit", lambda: True),
            TestCase("failure", "recovery", lambda: False),
            TestCase("crash", "failure", lambda: 1 / 0 == 1),
        )
    )
    assert matrix_rate(results) == 1 / 3
    attempts = {"n": 0}

    def flaky() -> str:
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise RuntimeError("transient")
        return "ok"

    assert retry(flaky, FailurePolicy(max_attempts=3)) == "ok"


def test_phase_20_benchmark_corpus():
    cases = (
        BenchmarkCase("arith", "arithmetic", "2+3", "5"),
        BenchmarkCase("algebra", "algebra", "2*x=4", "(2,)"),
        BenchmarkCase("calculus", "calculus", "x**2", "x**2"),
    )
    results = run_benchmark(
        cases,
        lambda value: {"2+3": "5", "2*x=4": "(2,)", "x**2": "x**2"}[value],
    )
    assert pass_rate(results) == 1.0


def test_phase_21_ocr_benchmark_metrics():
    case = OcrBenchmarkCase(
        "fraction",
        "formula",
        "x^2 + 1/2",
        ("power", "fraction", "operator"),
    )
    result = score_case(case, "x^2 + 1/2", ("power", "fraction", "operator"))
    assert result.character_accuracy == 1.0
    assert aggregate((result,))["structure_accuracy"] == 1.0


def test_phase_22_adversarial_inputs_never_crash():
    results = run_adversarial()
    assert len(results) >= 6
    assert all(isinstance(actual, bool) for _, actual, _ in results)
    assert sp.sympify("sqrt(-1)") == sp.I


def test_phase_23_persian_rtl_rendering():
    answer = render_answer("راه‌حل مرحله‌به‌مرحله آماده است.", verified=True)
    assert answer.direction == "rtl"
    assert "تأییدشده" in answer.title_fa


def test_phase_24_production_and_recovery_controls():
    validate_config(ProductionConfig("production"))
    validate_recovery(RecoveryPlan())
    for bad in (
        ProductionConfig("unknown"),
        ProductionConfig("production", max_request_bytes=0),
        ProductionConfig("production", worker_timeout_seconds=0),
    ):
        try:
            validate_config(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid production config accepted")


def test_phase_25_release_audit_blocks_missing_evidence():
    audit = build_audit({area: True for area in REQUIRED_AREAS})
    assert audit.passed
    incomplete = build_audit({"architecture": True})
    assert not incomplete.passed
    assert len(incomplete.blockers) == len(REQUIRED_AREAS) - 1
