from persian_math.application import ApplicationService
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


def test_history_starts_empty_and_tracks_solved_input(monkeypatch) -> None:
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
