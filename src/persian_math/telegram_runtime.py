from __future__ import annotations

import logging
from io import BytesIO
from typing import Any

from PIL import Image
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .application import ApplicationService
from .domain import Difficulty, EducationalLevel
from .ocr import ImageMetadata, TesseractOcrBackend, reconstruct_math_text, validate_image_bytes
from .runtime_config import load_runtime_config
from .telegram_adapter import IncomingMessage, MessageKind, OutgoingMessage

LOGGER = logging.getLogger(__name__)
_SERVICE = ApplicationService()
_OCR = TesseractOcrBackend(language="eng")

MAIN_MENU = ReplyKeyboardMarkup(
    [
        ["🧮 حل مسئله", "📝 تمرین"],
        ["👤 پروفایل", "📚 تاریخچه"],
        ["⚙️ تنظیمات", "❓ راهنما"],
    ],
    resize_keyboard=True,
    is_persistent=True,
)

LEVELS = (
    ("ابتدایی", EducationalLevel.ELEMENTARY.value),
    ("متوسطه اول", EducationalLevel.MIDDLE.value),
    ("متوسطه دوم", EducationalLevel.HIGH_SCHOOL.value),
    ("کنکور", EducationalLevel.ENTRANCE_EXAM.value),
    ("دانشگاه", EducationalLevel.UNIVERSITY.value),
    ("پیشرفته", EducationalLevel.ADVANCED.value),
    ("المپیاد", EducationalLevel.OLYMPIAD.value),
)


def _text_message(user_id: int, text: str) -> IncomingMessage:
    return IncomingMessage(str(user_id), MessageKind.TEXT, text=text)


def _inline(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(label, callback_data=data) for label, data in row] for row in rows]
    )


async def _send_response(update: Update, response: OutgoingMessage) -> None:
    if not update.message:
        return
    await update.message.reply_text(response.text_fa, reply_markup=MAIN_MENU)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        response = _SERVICE.menu(str(update.effective_user.id))
        await update.message.reply_text(
            "سلام! به دستیار ریاضی خوش آمدی.\n\n" + response.text_fa,
            reply_markup=MAIN_MENU,
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        await _send_response(update, _SERVICE.help(str(update.effective_user.id)))


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        await _send_response(update, _SERVICE.menu(str(update.effective_user.id)))


async def _exercise_menu(update: Update) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "موضوع تمرین را انتخاب کن:",
        reply_markup=_inline(
            [
                [("جبر", "exercise:algebra"), ("حساب", "exercise:arithmetic")],
                [("حسابان", "exercise:calculus")],
                [("بازگشت", "menu")],
            ]
        ),
    )


async def _difficulty_menu(update: Update, domain: str) -> None:
    if not update.callback_query:
        return
    await update.callback_query.edit_message_text(
        "سطح تمرین را انتخاب کن:",
        reply_markup=_inline(
            [
                [("آسان", f"generate:{domain}:easy"), ("متوسط", f"generate:{domain}:medium")],
                [("سخت", f"generate:{domain}:hard"), ("پیشرفته", f"generate:{domain}:expert")],
                [("بازگشت", "exercise_menu")],
            ]
        ),
    )


async def _level_menu(update: Update) -> None:
    if not update.callback_query:
        return
    await update.callback_query.edit_message_text(
        "سطح آموزشی را انتخاب کن:",
        reply_markup=_inline(
            [[(label, f"level:{value}")] for label, value in LEVELS]
            + [[("بازگشت", "menu")]]
        ),
    )


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not update.effective_user:
        return
    await query.answer()
    user_id = str(update.effective_user.id)
    data = query.data or ""

    try:
        if data == "menu":
            await query.edit_message_text(
                _SERVICE.menu(user_id).text_fa,
                reply_markup=_inline(
                    [
                        [("حل مسئله", "solve"), ("تمرین", "exercise_menu")],
                        [("پروفایل", "profile"), ("تاریخچه", "history")],
                        [("تنظیمات", "settings"), ("راهنما", "help")],
                    ]
                ),
            )
            return
        if data == "solve":
            await query.edit_message_text(
                "صورت مسئله را به‌صورت متن بفرست یا یک عکس واضح ارسال کن.",
                reply_markup=_inline([[("بازگشت", "menu")]]),
            )
            return
        if data == "exercise_menu":
            await query.edit_message_text(
                "موضوع تمرین را انتخاب کن:",
                reply_markup=_inline(
                    [
                        [("جبر", "exercise:algebra"), ("حساب", "exercise:arithmetic")],
                        [("حسابان", "exercise:calculus")],
                        [("بازگشت", "menu")],
                    ]
                ),
            )
            return
        if data.startswith("exercise:"):
            await _difficulty_menu(update, data.split(":", 1)[1])
            return
        if data.startswith("generate:"):
            _, domain, raw_difficulty = data.split(":", 2)
            difficulty = Difficulty(raw_difficulty)
            response = _SERVICE.exercises(user_id, domain, difficulty, 3)
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline(
                    [
                        [("تمرین جدید", f"generate:{domain}:{raw_difficulty}")],
                        [("موضوع دیگر", "exercise_menu"), ("منوی اصلی", "menu")],
                    ]
                ),
            )
            return
        if data == "profile":
            response = _SERVICE.profile(user_id)
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline(
                    [[("تغییر سطح", "level_menu"), ("منوی اصلی", "menu")]]
                ),
            )
            return
        if data == "level_menu":
            await _level_menu(update)
            return
        if data.startswith("level:"):
            response = _SERVICE.set_level(user_id, data.split(":", 1)[1])
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline([[("پروفایل", "profile"), ("منوی اصلی", "menu")]]),
            )
            return
        if data == "history":
            response = _SERVICE.history(user_id)
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline([[("منوی اصلی", "menu")]]),
            )
            return
        if data == "settings":
            response = _SERVICE.settings(user_id)
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline(
                    [[("تغییر سطح", "level_menu"), ("منوی اصلی", "menu")]]
                ),
            )
            return
        if data == "help":
            response = _SERVICE.help(user_id)
            await query.edit_message_text(
                response.text_fa,
                reply_markup=_inline([[("منوی اصلی", "menu")]]),
            )
            return
    except Exception:
        LOGGER.exception("callback request failed")
        await query.edit_message_text("در اجرای این گزینه مشکلی پیش آمد. دوباره تلاش کن.")


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.text:
        return
    try:
        user_id = str(update.effective_user.id)
        text = update.message.text.strip()
        routes = {
            "🧮 حل مسئله": "solve",
            "📝 تمرین": "exercise_menu",
            "👤 پروفایل": "profile",
            "📚 تاریخچه": "history",
            "⚙️ تنظیمات": "settings",
            "❓ راهنما": "help",
        }
        if text in routes:
            route = routes[text]
            if route == "exercise_menu":
                await _exercise_menu(update)
                return
            if route == "solve":
                await update.message.reply_text(
                    "صورت مسئله را بفرست؛ می‌توانی متن سؤال یا عکس واضح ارسال کنی.",
                    reply_markup=MAIN_MENU,
                )
                return
            response = {
                "profile": _SERVICE.profile(user_id),
                "history": _SERVICE.history(user_id),
                "settings": _SERVICE.settings(user_id),
                "help": _SERVICE.help(user_id),
            }[route]
            await _send_response(update, response)
            return
        response = _SERVICE.handle(_text_message(update.effective_user.id, text))
        await _send_response(update, response)
    except Exception:
        LOGGER.exception("text request failed")
        await update.message.reply_text(
            "پردازش مسئله با خطا روبه‌رو شد. لطفاً دوباره تلاش کن.",
            reply_markup=MAIN_MENU,
        )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.photo:
        return
    try:
        photo = update.message.photo[-1]
        telegram_file = await photo.get_file()
        data = bytes(await telegram_file.download_as_bytearray())
        validate_image_bytes(data)
        with Image.open(BytesIO(data)) as image:
            metadata = ImageMetadata(image.width, image.height, len(image.getbands()))
        ocr = _OCR.recognize(data, metadata)
        if ocr.confidence < 0.60:
            await update.message.reply_text(
                "اطمینان OCR کافی نیست؛ لطفاً عکس واضح‌تر و مستقیم‌تری ارسال کن.",
                reply_markup=MAIN_MENU,
            )
            return
        text = reconstruct_math_text(ocr, metadata)
        if not text.strip():
            await update.message.reply_text(
                "نتوانستم متن ریاضی قابل اعتمادی از تصویر استخراج کنم.",
                reply_markup=MAIN_MENU,
            )
            return
        response = _SERVICE.handle(_text_message(update.effective_user.id, text))
        await update.message.reply_text(
            f"متن تشخیص‌داده‌شده:\n{text}\n\n{response.text_fa}",
            reply_markup=MAIN_MENU,
        )
    except Exception:
        LOGGER.exception("image request failed")
        await update.message.reply_text(
            "تصویر قابل پردازش نبود؛ لطفاً عکس واضح‌تری ارسال کن.",
            reply_markup=MAIN_MENU,
        )


def build_application() -> Application[Any, Any, Any, Any, Any, Any]:
    config = load_runtime_config()
    application = Application.builder().token(config.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    return application


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    build_application().run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
