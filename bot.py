import logging
import tomllib
from pathlib import Path

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

CONFIG_PATH = Path(__file__).parent / "config.toml"

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def load_config(path: Path = CONFIG_PATH) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    logger.info("Message from chat ID %s", chat_id)
    await update.message.reply_text("You said: " + update.message.text)


async def ignore_stranger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning("Ignored message from unknown chat ID %s", update.effective_chat.id)


def main() -> None:
    config = load_config()
    token = config["telegram"]["token"]
    owner_chat_id = config["telegram"]["owner_chat_id"]

    app = Application.builder().token(token).build()
    owner = filters.Chat(chat_id=owner_chat_id)
    app.add_handler(MessageHandler(owner & filters.UpdateType.MESSAGE & filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(~owner, ignore_stranger))
    app.run_polling()


if __name__ == "__main__":
    main()