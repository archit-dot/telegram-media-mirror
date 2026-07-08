from aiogram import Bot, Dispatcher

from config.settings import BOT_TOKEN

# Create Bot instance
bot = Bot(token=BOT_TOKEN)

# Create Dispatcher
dp = Dispatcher()