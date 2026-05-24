from telegram.ext import Application, MessageHandler, filters
from src.config.configuracion import config
from src.handlers import registrar_handlers
from src.utils.logger import config_logger


logger = config_logger(__name__)

class TGBuscador:

    def __init__(self) -> None:

        self.app = (
            Application.builder()
            .token(config.bot_token)
            .build()
        )

        registrar_handlers(self.app)

        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.REPLY, self.echo)
        )
    async def echo(self, update, context):

        await update.message.reply_text(
            f"Dijiste: {update.message.text}"
        )

    def run(self):

        logger.info("Bot iniciado")

        self.app.run_polling()


if __name__ == "__main__":

    bot = TGBuscador()

    logger.info("Aplicación iniciando")

    bot.run()

    logger.info("Aplicación finalizada")