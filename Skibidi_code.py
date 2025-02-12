import time, threading, schedule, random
from telebot import TeleBot
from bot_logic import gen_pass
skibididecayingitems = {
    "батарейка": "Батарейка разлагается от 100 до 1000 лет. Переработка важна!",
    "яблоко": "Яблоко разлагается за 2-4 недели.",
    "пластик": "Пластик разлагается от 100 до 1000 лет. Переработка важна!",
    "стекло": "Стекло разлагается более 1000 лет, но его можно перерабатывать бесконечно.",
    "алюминиевая банка": "Алюминиевая банка разлагается около 500 лет. Лучше сдать на переработку!",
    "бумага": "Бумага разлагается от нескольких недель до 2 лет.",
    "дерево": "Дерево разлагается от 2 до 10 лет в зависимости от условий.",
    "резина": "Резина разлагается более 100 лет. Шины лучше сдавать в переработку.",
    "полиэтиленовый пакет": "Полиэтиленовый пакет разлагается от 100 до 400 лет.",
    "жестяная банка": "Жестяная банка разлагается около 50 лет.",
    "кожура банана": "Кожура банана разлагается за 2-5 недель.",
    "картон": "Картон разлагается примерно за 2 месяца.",
    "фольга": "Фольга практически не разлагается, но может быть переработана.",
    "железо": "Железо разлагается около 10 лет, но может ржаветь быстрее."
}
API_TOKEN = '[REDACTED]'
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Используй '/hello' '/bye' '/gen' '/photo' и '/set <секунды>' с '/unset' чтобы поставить или убрать таймер")


def beep(chat_id) -> None:
    """Send the beep message."""
    bot.send_message(chat_id, text='Бип Бип Бип!')


@bot.message_handler(commands=['set'])
def set_timer(message):
    args = message.text.split()
    if len(args) > 1 and args[1].isdigit():
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)
    else:
        bot.reply_to(message, 'Usage: /set <seconds>')


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['gen'])
def gen(message):
    password = gen_pass(10) 
    bot.reply_to(message, password) 

@bot.message_handler(commands=['photo'])
def send_cat(message):
    images = ['images/cat.jpg', 'images/cat2.jpg', 'images/cat3.jpg']
    with open(random.choice(images), 'rb') as f:
        bot.send_photo(message.chat.id, f)

@bot.message_handler(commands=['decay'])
def send_decay(message):
    random_item = random.choice(list(skibididecayingitems.keys()))
    bot.reply_to(message, skibididecayingitems[random_item])

if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
