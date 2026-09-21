from __future__ import annotations

from dataclasses import dataclass, replace

from .domain import Difficulty, EducationalLevel, UserProfile
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
        if not user_id.strip():
            raise ValueError("user id required")
        return self._sessions.setdefault(user_id, AppSession(UserProfile(user_id)))

    def menu(self, user_id: str) -> OutgoingMessage:
        self.session(user_id)
        return OutgoingMessage(
            "منوی اصلی را انتخاب کن:",
            ("حل مسئله", "تمرین", "پروفایل", "تاریخچه", "راهنما", "تنظیمات"),
        )

    def profile(self, user_id: str) -> OutgoingMessage:
        session = self.session(user_id)
        level = session.education_mode or session.user.educational_level
        return OutgoingMessage(
            f"پروفایل آموزشی\n\nسطح: {level.value}\nزبان: فارسی\n"
            f"تعداد مسائل ثبت‌شده در این نشست: {len(session.history)}",
            ("تغییر سطح", "بازگشت"),
        )

    def settings(self, user_id: str) -> OutgoingMessage:
        self.session(user_id)
        return OutgoingMessage(
            "تنظیمات\n\nزبان فعلی: فارسی\nحالت پاسخ: آموزشی\n\n"
            "تنظیمات پیشرفته در نسخه‌های بعدی فعال می‌شوند.",
            ("تغییر سطح", "بازگشت"),
        )

    def history(self, user_id: str) -> OutgoingMessage:
        session = self.session(user_id)
        if not session.history:
            return OutgoingMessage("هنوز مسئله‌ای در این نشست ثبت نشده است.", ("بازگشت",))
        items = "\n".join(
            f"{index}. {item[:120]}" for index, item in enumerate(reversed(session.history), 1)
        )
        return OutgoingMessage(f"تاریخچه این نشست:\n\n{items}", ("بازگشت",))

    def set_level(self, user_id: str, value: str) -> OutgoingMessage:
        session = self.session(user_id)
        try:
            level = EducationalLevel(value)
        except ValueError:
            return OutgoingMessage("سطح آموزشی معتبر نیست.")
        self._sessions[user_id] = replace(session, education_mode=level)
        return OutgoingMessage(f"سطح آموزشی روی «{value}» تنظیم شد.", ("بازگشت",))

    def exercises(
        self,
        user_id: str,
        domain: str = "algebra",
        difficulty: Difficulty = Difficulty.MEDIUM,
        count: int = 3,
    ) -> OutgoingMessage:
        self.session(user_id)
        exercises = tuple(
            e for e in generate(ExerciseSpec(domain, difficulty, count)) if validate_exercise(e)
        )
        if not exercises:
            return OutgoingMessage("تمرین معتبر تولید نشد. لطفاً دوباره تلاش کن.", ("بازگشت",))
        body = "\n".join(
            f"{index}. {exercise.prompt}" for index, exercise in enumerate(exercises, 1)
        )
        return OutgoingMessage(
            f"تمرین‌های {domain} — سطح {difficulty.value}:\n\n{body}",
            ("تمرین جدید", "بازگشت"),
        )

    def help(self, user_id: str) -> OutgoingMessage:
        self.session(user_id)
        return OutgoingMessage(
            "راهنما\n\n"
            "• حل مسئله: متن سؤال یا عکس واضح بفرست.\n"
            "• تمرین: موضوع و سختی را انتخاب کن.\n"
            "• پروفایل: سطح آموزشی را ببین یا تغییر بده.\n"
            "• تاریخچه: مسائل همین نشست را ببین.\n"
            "• تنظیمات: تنظیمات فعلی را مشاهده کن.\n\n"
            "می‌توانی هر زمان /start یا /menu را هم ارسال کنی.",
            ("بازگشت",),
        )

    def handle(self, message: IncomingMessage) -> OutgoingMessage:
        validate_incoming(message)
        session = self.session(message.user_id)
        if message.kind != MessageKind.TEXT:
            return OutgoingMessage("فایل دریافت شد. پس از اعتبارسنجی، پردازش آن آغاز می‌شود.")
        text = message.text.strip()
        if text in {"/start", "/menu"}:
            return self.menu(message.user_id)
        if text == "/help":
            return self.help(message.user_id)
        if text.startswith("/level "):
            return self.set_level(message.user_id, text.split(maxsplit=1)[1])
        if text == "/profile":
            return self.profile(message.user_id)
        if text == "/history":
            return self.history(message.user_id)
        if text == "/settings":
            return self.settings(message.user_id)
        if text == "/exercise":
            return self.exercises(message.user_id)
        result = process(text)
        self._sessions[message.user_id] = replace(
            session, history=(*session.history[-19:], text)
        )
        if not result.solver.success:
            return OutgoingMessage(
                "این مسئله فعلاً با اطمینان کافی قابل حل نیست. لطفاً صورت سؤال را واضح‌تر ارسال کن."
            )
        verified = result.verification.verified if result.verification else False
        suffix = "نتیجه مستقل تأیید شد." if verified else "نتیجه هنوز تأیید مستقل کامل ندارد."
        return OutgoingMessage(f"پاسخ: {result.solver.value}\n\n{suffix}")
