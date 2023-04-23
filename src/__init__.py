import argparse
import logging
import os
import tempfile

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from PIL import Image

from criteria.space import space
from criteria.tabular import tabular

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def load_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = context.bot.getFile(update.message.document)
    return file


def load_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = context.bot.getFile(update.message.photo[-1])
    return file


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE, load_function):
    source = None
    with tempfile.NamedTemporaryFile() as tmp:
        file = await load_function(update=update, context=context)
        await file.download_to_drive(tmp.name)

        source = Image.open(tmp).convert("RGB")
        source.save("last.jpg")

        space_rate, space_mask = space(source)
        tabular_check, tabular_mask = tabular(source)

        reply = Image.new("RGB", (source.width * 2, source.height))
        reply.paste(Image.blend(source, space_mask, alpha=0.9), (0, 0))
        reply.paste(Image.blend(source, tabular_mask, alpha=0.9), (source.width, 0))
        reply.save(tmp.name, "JPEG")

        await context.bot.send_photo(
            reply_to_message_id=update.message.id,
            chat_id=update.effective_chat.id,
            photo=tmp.name,
            caption=os.linesep.join(
                [
                    f"Количество воздуха: {int(space_rate * 100)}%",
                    f"Согласованность отступов: {100 * tabular_check // 4}%",
                ]
            ),
        )

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=tmp.name,
            caption=os.linesep.join(
                [
                    f"Количество воздуха: {int(space_rate * 100)}%",
                    f"Согласованность отступов: {100 * tabular_check // 4}%",
                ]
            ),
        )


async def check_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check(update=update, context=context, load_function=load_document)


async def check_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check(update=update, context=context, load_function=load_photo)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="test")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token", dest="token", type=str, help="Provide telegram bot token"
    )
    args = parser.parse_args()

    application = ApplicationBuilder().token(args.token).build()

    start_handler = CommandHandler("start", start)

    image_document_handler = MessageHandler(filters.Document.IMAGE, check_document)
    image_photo_handler = MessageHandler(filters.PHOTO, check_photo)

    application.add_handler(start_handler)
    application.add_handler(image_document_handler)
    application.add_handler(image_photo_handler)

    application.run_polling()
