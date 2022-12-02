import telebot
import subprocess
from diff import get_diff
from util import load_config, run_ansible
from Config import Config, ConfigType

config = load_config("")
API_KEY = config["telegram_key"]

bot = telebot.TeleBot(API_KEY)

err = lambda str: "\U00002755" + str


@bot.message_handler(commands=["help"])
def help(message):
    help_str = """
    Commands that are available:
        /help - get help message
        /diff_baseline {ip} - get the differences between the baseline configuration file and the startup configuration file of a device
        /diff_running {ip} - get the differences between the startup and running configurations of a device
        /write_mem {ip} - write running config to memory
    """

    bot.reply_to(message, help_str)


@bot.message_handler(commands=["write_mem"])
def write_mem(message):
    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(message.chat.id, err("Command needs an IP as an argument"))
        bot.send_message(message.chat.id, err("[!] Example: /diff_running 10.9.0.2"))
        return
    ip = message.text.split(" ")[1]
    if not ip:
        bot.reply_to(message, err("You need to specify an IP"))
        return
    subprocess.run(["ansible-playbook", "-i", f"{ip},", "playbooks/write_mem.yml"])

    bot.reply_to(message, "[*] Wrote to NVRAM")


@bot.message_handler(commands=["diff_running"])
def diff_running(message):
    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(message.chat.id, err("Command needs an IP as an argument"))
        bot.send_message(message.chat.id, err("[!] Example: /diff_running 10.9.0.2"))
        return
    ip = message.text.split(" ")[1]
    bot.send_message(message.chat.id, "[*] Wait just a sec :)")

    run_ansible()
    running_config = str(Config(ip=ip, type=ConfigType.RUNNING))
    startup_config = str(Config(ip=ip, type=ConfigType.STARTUP))

    bot.reply_to(message, str(get_diff(startup_config, running_config)))


@bot.message_handler(commands=["diff_baseline"])
def diff_ideal(message):
    args = message.text.split(" ")
    if len(args) < 2:
        bot.send_message(message.chat.id, err("Command needs an IP as an argument"))
        bot.send_message(message.chat.id, err("Example: /diff_ideal 10.9.0.2"))
        return
    ip = message.text.split(" ")[1]
    bot.send_message(message.chat.id, "[*] Wait just a sec :)")
    run_ansible()
    startup_config = str(Config(ip=ip, type=ConfigType.STARTUP))
    ideal_config = str(Config(ip=ip, type=ConfigType.IDEAL))
    bot.reply_to(message, str(get_diff(ideal_config, startup_config)))


@bot.message_handler(func=lambda _: True, content_types=["text"])
def command_default(message):
    bot.send_message(message.chat.id, err("Command unrecognized. Maybe try /help"))


bot.polling()
