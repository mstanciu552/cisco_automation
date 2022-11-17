import os
import telebot
from dotenv import load_dotenv
from cisco import get_diff_ideal_startup, get_diff_startup_running

load_dotenv()

API_KEY = os.getenv("TELEGRAM_KEY") or ""

bot = telebot.TeleBot(API_KEY)

err = lambda str: "\U00002755" + str


@bot.message_handler(commands=["help"])
def help(message):
    help_str = """
    Commands that are available:
        /help - get help message
        /diff_ideal - get the differences between the ideal configuration file and the startup configuration file of a device
        /diff_running - get the differences between the startup and running configurations of a device

    Commands that are in development:
        /get_running - specify by IP 
        /get_startup - specify by IP 
        /get_ideal - get the ideal config from the tftp server
        /copy running startup
        /copy ideal startup
        /reload - Reload the device
    """

    bot.reply_to(message, help_str)


@bot.message_handler(commands=["diff_running"])
def diff_running(message):
    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(message.chat.id, err("Command needs an IP as an argument"))
        bot.send_message(message.chat.id, err("[!] Example: /diff_running 10.9.0.2"))
        return
    arg = message.text.split(" ")[1]
    bot.send_message(message.chat.id, "[*] Wait just a sec :)")
    bot.reply_to(message, str(get_diff_startup_running(ip=arg)))


@bot.message_handler(commands=["diff_ideal"])
def diff_ideal(message):
    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(
            message.chat.id, err("Command needs an IP as an argument")
        )
        bot.send_message(message.chat.id, err("Example: /diff_ideal 10.9.0.2"))
        return
    arg = message.text.split(" ")[1]
    bot.send_message(message.chat.id, "[*] Wait just a sec :)")
    bot.reply_to(message, str(get_diff_ideal_startup(ip=arg)))


@bot.message_handler(func=lambda _: True, content_types=["text"])
def command_default(message):
    bot.send_message(message.chat.id, err("Command unrecognized. Maybe try /help"))


bot.polling()
