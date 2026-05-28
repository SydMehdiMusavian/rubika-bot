import logging
from logging.handlers import RotatingFileHandler
import contextvars

bot_token_var = contextvars.ContextVar('bot_token', default='unknown')
class BotTokenFilter(logging.Filter):
    def filter(self, record):
        record.bot_token = bot_token_var.get()
        return True

def setup_logger(name="RubikaBot", log_file="rubika_bot.log", level=logging.INFO):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger
    
    formatter = logging.Formatter(
        "%(asctime)s - [%(bot_token)s] - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    file_handler = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.addFilter(BotTokenFilter())
    return logger

bot_logger = setup_logger()
