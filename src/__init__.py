import logging
import uuid
import tempfile

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.ext import Application, MessageHandler, filters

from PIL import Image

from tqdm import tqdm

from criteria import space, tabular


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def downloader(update, context):
    source = None
    with tempfile.NamedTemporaryFile() as tmp_in, tempfile.NamedTemporaryFile() as tmp_out:
        file = await context.bot.get_file(update.message.document)
        await file.download_to_drive(tmp_in.name)

        source = Image.open(tmp_in).convert('RGB')

        space_rate, space_mask = space(source)

        Image.blend(source, space_mask, alpha=0.7).save(tmp_out.name, "JPEG")
        
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=tmp_out.name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{int(space_rate * 100)}% of space")


        tabular_check, tabular_mask = tabular(source)
        Image.blend(source, tabular_mask, alpha=0.7).save(tmp_out.name, "JPEG")

        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=tmp_out.name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Tabular {'OK' if tabular_check else 'FAIL'}")
    

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="test")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    token = None
    with open('resources/token', 'r') as f:
        token = f.read()

    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    # test_handler = CommandHandler('test', test)

    message_handler = MessageHandler(filters.Document.ALL, downloader)

    application.add_handler(start_handler)
    # application.add_handler(test_handler)
    application.add_handler(message_handler)
    
    application.run_polling()
