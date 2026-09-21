import pytest

from persian_math.benchmark import BenchmarkCase, pass_rate, run_benchmark
from persian_math.domain import Difficulty, EducationalLevel, UserProfile
from persian_math.file_pipeline import Page, index_text_pages, validate_document
from persian_math.jobs import InMemoryJobQueue, JobStatus
from persian_math.learning_profile import ProblemRecord, create_learning_profile
from persian_math.security import safe_filename, validate_text, validate_url
from persian_math.telegram_adapter import (
    IncomingMessage,
    MessageKind,
    localize_error,
    validate_incoming,
)
from persian_math.tutoring import (
    TutorAction,
    TutorStep,
    check,
    hint,
    reexplain,
    start_tutor,
)


def user() -> UserProfile:
    return UserProfile("u", EducationalLevel.HIGH_SCHOOL)


def test_phase_11_tutor_progress_and_hint():
    s = start_tutor(
        "s1",
        user(),
        "معادله",
        (TutorStep(0, "x را پیدا کن", 3, "عدد ثابت را به طرف دیگر ببر."),),
    )
    assert hint(s).action == TutorAction.HINT
    s2, response = check(s, 3)
    assert response.correct is True
    assert s2.completed
    with pytest.raises(ValueError):
        reexplain(s2)


def test_phase_12_exercise_validation_path():
    profile = create_learning_profile(user())
    updated = profile.add(ProblemRecord("algebra", Difficulty.MEDIUM, True))
    assert updated.accuracy == 1.0
    assert updated.recommended_difficulty() == Difficulty.MEDIUM


def test_phase_13_learning_profile_privacy_and_weak_topics():
    profile = create_learning_profile(user())
    profile = profile.add(ProblemRecord("geometry", Difficulty.EASY, False))
    profile = profile.add(ProblemRecord("geometry", Difficulty.EASY, False))
    assert "geometry" in profile.weak_topics
    assert profile.privacy_enabled


def test_phase_14_telegram_adapter_is_transport_neutral():
    message = IncomingMessage("u", MessageKind.TEXT, "حل x+1=2")
    validate_incoming(message)
    assert "ورودی" in localize_error("invalid_input").text_fa


def test_phase_15_pdf_index_and_question_lookup():
    data = b"%PDF-1.7 fake"
    validate_document(data)
    index = index_text_pages((Page(1, "1. سؤال اول\n2) سؤال دوم"),))
    assert index.question(2).text == "سؤال دوم"


def test_phase_16_job_lifecycle_and_retry():
    q = InMemoryJobQueue()
    job = q.enqueue("solve", {"text": "x+1=2"})
    running = q.claim(job.job_id)
    assert running.status == JobStatus.RUNNING
    queued = q.finish(job.job_id, False)
    assert queued.status == JobStatus.QUEUED


def test_phase_17_security_bounds_and_ssrf_baseline():
    assert validate_text("x+1") == "x+1"
    assert safe_filename("question.pdf") == "question.pdf"
    with pytest.raises(ValueError):
        safe_filename("../secret")
    with pytest.raises(ValueError):
        validate_url("http://127.0.0.1:8080")


def test_phase_18_metrics():
    from persian_math.observability import Metrics

    metrics = Metrics()
    metrics.observe("solver.latency_ms", 12.5, domain="algebra")
    assert metrics.snapshot()[0].tags == (("domain", "algebra"),)


def test_phase_19_failure_is_a_benchmark_result():
    cases = (BenchmarkCase("a", "algebra", "1+1", "2"),)
    results = run_benchmark(cases, lambda _: "2")
    assert pass_rate(results) == 1.0


def test_phase_20_benchmark_detects_failure():
    cases = (
        BenchmarkCase("a", "algebra", "1+1", "2"),
        BenchmarkCase("b", "geometry", "bad", "ok"),
    )
    results = run_benchmark(cases, lambda x: "2" if x == "1+1" else "wrong")
    assert pass_rate(results) == 0.5
