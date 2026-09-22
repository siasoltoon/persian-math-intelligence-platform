import pytest

from persian_math.application import ApplicationService
from persian_math.batch import MAX_BATCH_ITEMS, split_problem_batch
from persian_math.domain import Difficulty
from persian_math.telegram_adapter import IncomingMessage, MessageKind


def message(user_id: str, text: str) -> IncomingMessage:
    return IncomingMessage(user_id, MessageKind.TEXT, text=text)


def test_start_returns_main_menu_buttons() -> None:
    service = ApplicationService()
    response = service.handle(message("1", "/start"))
    assert "حل مسئله" in response.buttons
    assert "تمرین" in response.buttons
    assert "پروفایل" in response.buttons


def test_profile_and_level_flow() -> None:
    service = ApplicationService()
    response = service.profile("1")
    assert "سطح" in response.text_fa

    response = service.set_level("1", "university")
    assert "university" in response.text_fa
    assert service.session("1").education_mode.value == "university"


def test_history_starts_empty_and_tracks_solved_input(monkeypatch: pytest.MonkeyPatch) -> None:
    service = ApplicationService()
    empty = service.history("1")
    assert "هنوز مسئله‌ای" in empty.text_fa

    class Verification:
        verified = True

    class Solver:
        success = True
        value = 4

    class Result:
        solver = Solver()
        verification = Verification()

    monkeypatch.setattr("persian_math.application.process", lambda _: Result())
    service.handle(message("1", "2 + 2"))
    history = service.history("1")
    assert "2 + 2" in history.text_fa


def test_batch_split_explicit_question_labels() -> None:
    text = "سؤال ۱: 2 + 2\nسؤال ۲: 3 × 4\nسؤال ۳: x + 2 = 5"
    assert split_problem_batch(text) == ("2 + 2", "3 × 4", "x + 2 = 5")


def test_batch_split_numbered_questions() -> None:
    text = "1) 2 + 2\n2) 3 + 4\n3) 5 × 6"
    assert split_problem_batch(text) == ("2 + 2", "3 + 4", "5 × 6")


def test_batch_does_not_split_multiline_system_or_function_analysis() -> None:
    system = "x + y = 5\n2x - y = 1"
    assert split_problem_batch(system) == (system,)
    analysis = (
        "تابع f(x) = x^3 - 3x\n\n"
        "1. نقاط بحرانی را پیدا کنید.\n"
        "2. بازه‌های صعود و نزول را تعیین کنید.\n"
        "3. نقاط عطف را پیدا کنید."
    )
    assert split_problem_batch(analysis) == (analysis,)


def test_batch_application_solves_all_problems_in_one_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = ApplicationService()

    class Verification:
        verified = True

    class Solver:
        success = True
        value = 0

    class Result:
        solver = Solver()
        verification = Verification()

    values = iter((4, 12, 5))

    def fake_process(_: str) -> Result:
        Result.solver.value = next(values)
        return Result()

    monkeypatch.setattr("persian_math.application.process", fake_process)
    response = service.handle(message("1", "1) 2 + 2\n2) 3 × 4\n3) x + 2 = 5"))
    assert "نتیجه 3 مسئله" in response.text_fa
    assert "سؤال 1:" in response.text_fa
    assert "پاسخ: 4" in response.text_fa
    assert "پاسخ: 12" in response.text_fa
    assert "پاسخ: 5" in response.text_fa
    assert len(service.session("1").history) == 3


def test_batch_limits_are_bounded() -> None:
    text = "\n".join(f"{i}) {i} + 1" for i in range(1, MAX_BATCH_ITEMS + 1))
    assert len(split_problem_batch(text)) == MAX_BATCH_ITEMS
    with pytest.raises(ValueError, match="too many"):
        split_problem_batch(text + f"\n{MAX_BATCH_ITEMS + 1}) 99 + 1")


def test_exercise_domains_and_difficulty_are_validated() -> None:
    service = ApplicationService()
    response = service.exercises("1", "calculus", Difficulty.HARD, 2)
    assert "calculus" in response.text_fa
    assert "hard" in response.text_fa
    assert "1." in response.text_fa
    assert "2." in response.text_fa


def test_help_and_settings_are_user_safe() -> None:
    service = ApplicationService()
    assert "راهنما" in service.help("1").text_fa
    assert "تنظیمات" in service.settings("1").text_fa
