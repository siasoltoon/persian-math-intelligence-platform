from __future__ import annotations

from dataclasses import dataclass, replace

from .batch import split_problem_batch
from .domain import Difficulty, EducationalLevel, UserProfile
from .engine import EngineResult, process
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
            "سلام! منوی اصلی را انتخاب کن:",
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
            "• برای چند سؤال، همه را در یک پیام و با «۱.»، «۲.» یا «سؤال ۱:» جدا کن.\n"
            "• تمرین: موضوع و سختی را انتخاب کن.\n"
            "• پروفایل: سطح آموزشی را ببین یا تغییر بده.\n"
            "• تاریخچه: مسائل همین نشست را ببین.\n"
            "• تنظیمات: تنظیمات فعلی را مشاهده کن.\n\n"
            "می‌توانی هر زمان /start یا /menu را هم ارسال کنی.",
            ("بازگشت",),
        )

    @staticmethod
    def _render_result(result: EngineResult) -> tuple[bool, str]:
        solver = result.solver
        if not solver.success:
            return False, "این مسئله فعلاً با اطمینان کافی قابل حل نیست."
        verified = result.verification.verified if result.verification else False
        suffix = "نتیجه مستقل تأیید شد." if verified else "نتیجه هنوز تأیید مستقل کامل ندارد."
        value = solver.value
        if getattr(solver, "method", "") == "function_analysis" and isinstance(value, dict):
            critical = "، ".join(
                f"x={point} ({'ماکزیمم نسبی' if kind == 'max' else 'مینیمم نسبی' if kind == 'min' else 'نوع نامعین'}، f(x)={value_at})"
                for point, value_at, kind in value["critical_points"]
            )
            inflections = "، ".join(
                f"({point}, {value_at})" for point, value_at in value["inflection_points"]
            )
            rendered = (
                f"نقاط بحرانی: {critical or 'ندارد'}\n"
                f"بازه‌های صعود: {value['increasing']}\n"
                f"بازه‌های نزول: {value['decreasing']}\n"
                f"نقاط عطف: {inflections or 'ندارد'}"
            )
        elif isinstance(value, dict):
            rendered = "، ".join(f"{key} = {item}" for key, item in value.items())
        elif isinstance(value, tuple):
            rendered = "{" + ", ".join(str(item) for item in value) + "}"
        else:
            rendered = str(value)
        return verified, f"پاسخ: {rendered}\n\n{suffix}"

    def _handle_single_problem(self, user_id: str, text: str) -> tuple[bool, str]:
        session = self.session(user_id)
        try:
            result = process(text)
            rendered = self._render_result(result)
        except Exception:
            rendered = (
                False,
                "این مسئله به‌دلیل یک خطای داخلی قابل پردازش نبود. "
                "لطفاً صورت همین سؤال را دوباره ارسال کن."
            )
        self._sessions[user_id] = replace(session, history=(*session.history[-19:], text))
        return rendered

    def handle_batch(self, user_id: str, problems: tuple[str, ...]) -> OutgoingMessage:
        if not problems:
            return OutgoingMessage("هیچ مسئله‌ای برای پردازش دریافت نشد.")
        if len(problems) > 12:
            return OutgoingMessage(
                "تعداد مسائل یک پیام بیش از حد مجاز است. حداکثر ۱۲ مسئله ارسال کن."
            )
        rendered: list[str] = []
        for index, problem in enumerate(problems, 1):
            _, answer = self._handle_single_problem(user_id, problem)
            rendered.append(f"سؤال {index}:\n{answer}")
        return OutgoingMessage(
            f"نتیجه {len(problems)} مسئله:\n\n" + "\n\n".join(rendered),
            ("حل مسئله", "منوی اصلی"),
        )

    def handle(self, message: IncomingMessage) -> OutgoingMessage:
        validate_incoming(message)
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
        problems = split_problem_batch(text)
        if len(problems) > 1:
            return self.handle_batch(message.user_id, problems)
        _, rendered = self._handle_single_problem(message.user_id, text)
        return OutgoingMessage(rendered)
