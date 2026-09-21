from __future__ import annotations

import logging
from io import BytesIO
from typing import Any

from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .application import ApplicationService
from .ocr import ImageMetadata, TesseractOcrBackend, reconstruct_math_text, validate_image_bytes
from .runtime_config import load_runtime_config
from .telegram_adapter import IncomingMessage, MessageKind

LOGGER = logging.getLogger(__name__)
_SERVICE = ApplicationService()
_OCR = TesseractOcrBackend(language="eng")


def _text_message(user_id: int, text: str) -> IncomingMessage:
    return IncomingMessage(str(user_id), MessageKind.TEXT, text=text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        response = _SERVICE.handle(_text_message(update.effective_user.id, "/start"))
        await update.message.reply_text(response.text_fa)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user and update.message:
        response = _SERVICE.handle(_text_message(update.effective_user.id, "/help"))
        await update.message.reply_text(response.text_fa)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.text:
        return
    try:
        response = _SERVICE.handle(_text_message(update.effective_user.id, update.message.text))
        await update.message.reply_text(response.text_fa)
    except Exception:
        LOGGER.exception("text request failed")
        await update.message.reply_text("پردازش مسئله با خطا روبه‌رو شد. لطفاً دوباره تلاش کن.")


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
            )
            return
        text = reconstruct_math_text(ocr, metadata)
        if not text.strip():
            await update.message.reply_text("نتوانستم متن ریاضی قابل اعتمادی از تصویر استخراج کنم.")
            return
        response = _SERVICE.handle(_text_message(update.effective_user.id, text))
        await update.message.reply_text(f"متن تشخیص‌داده‌شده:\n{text}\n\n{response.text_fa}")
    except Exception:
        LOGGER.exception("image request failed")
        await update.message.reply_text("تصویر قابل پردازش نبود؛ لطفاً عکس واضح‌تری ارسال کن.")


def build_application() -> Application[Any, Any, Any, Any, Any, Any]:
    config = load_runtime_config()
    application = Application.builder().token(config.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    return application


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    build_application().run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
