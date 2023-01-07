from loader import bot
from handlers import default_heandlers
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
