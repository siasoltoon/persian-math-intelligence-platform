from __future__ import annotations

from dataclasses import dataclass, replace

from .domain import EducationalLevel, UserProfile
from .engine import process
from .exercises import ExerciseSpec, generate, validate_exercise
from .telegram_adapter import IncomingMessage, MessageKind, OutgoingMessage, validate_incoming


@dataclass(frozen=True)
class AppSession:
    user: UserProfile
    history: tuple[str, ...] = ()
    education_mode: EducationalLevel | None = None


class ApplicationService:
    def __init__(self) -> None:
        self._sessions: dict[str, AppSession] = {}

    def session(self, user_id: str) -> AppSession:
        return self._sessions.setdefault(user_id, AppSession(UserProfile(user_id)))

    def handle(self, message: IncomingMessage) -> OutgoingMessage:
        validate_incoming(message)
        session = self.session(message.user_id)
        if message.kind != MessageKind.TEXT:
            return OutgoingMessage("فایل دریافت شد. پس از اعتبارسنجی، پردازش آن آغاز می‌شود.")
        text = message.text.strip()
        if text == "/start":
            return OutgoingMessage("سلام! صورت مسئله را بفرست یا یکی از گزینه‌های حل مسئله، تمرین و پروفایل را انتخاب کن.")
        if text == "/help":
            return OutgoingMessage("دستورها: /start، /help، /exercise و ارسال مستقیم صورت مسئله.")
        if text.startswith("/level "):
            value = text.split(maxsplit=1)[1]
            try:
                level = EducationalLevel(value)
            except ValueError:
                return OutgoingMessage("سطح آموزشی معتبر نیست.")
            self._sessions[message.user_id] = replace(session, education_mode=level)
            return OutgoingMessage(f"سطح آموزشی روی «{value}» تنظیم شد.")
        if text == "/exercise":
            exercises = tuple(e for e in generate(ExerciseSpec("algebra", session.user.educational_level and __import__("persian_math.domain", fromlist=["Difficulty"]).Difficulty.MEDIUM, 3)) if validate_exercise(e))
            return OutgoingMessage("تمرین‌های پیشنهادی:
" + "
".join(f"• {e.prompt}" for e in exercises))
        result = process(text)
        self._sessions[message.user_id] = replace(session, history=(*session.history[-19:], text))
        if not result.solver.success:
            return OutgoingMessage("این مسئله فعلاً با اطمینان کافی قابل حل نیست. لطفاً صورت سؤال را واضح‌تر ارسال کن.")
        verified = result.verification.verified if result.verification else False
        suffix = "نتیجه مستقل تأیید شد." if verified else "نتیجه هنوز تأیید مستقل کامل ندارد."
        return OutgoingMessage(f"پاسخ: {result.solver.value}

{suffix}")
