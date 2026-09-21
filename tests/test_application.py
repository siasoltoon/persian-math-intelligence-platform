from persian_math.application import ApplicationService
from persian_math.telegram_adapter import IncomingMessage, MessageKind


def test_application_commands_and_history():
    app = ApplicationService()
    assert "سلام" in app.handle(IncomingMessage("u", MessageKind.TEXT, "/start")).text_fa
    assert "تمرین" in app.handle(IncomingMessage("u", MessageKind.TEXT, "/exercise")).text_fa
    assert "پاسخ:" in app.handle(IncomingMessage("u", MessageKind.TEXT, "1+1")).text_fa
    assert app.session("u").history == ("1+1",)


def test_application_handles_file_transport():
    app = ApplicationService()
    result = app.handle(IncomingMessage("u", MessageKind.IMAGE, payload=b"image"))
    assert "فایل" in result.text_fa


def test_application_renders_equation_solution_set_cleanly():
    service = ApplicationService()
    response = service.handle(IncomingMessage("u", MessageKind.TEXT, "2x² - 7x + 3 = 0"))
    assert "پاسخ: {" in response.text_fa
    assert "نتیجه مستقل تأیید شد." in response.text_fa
