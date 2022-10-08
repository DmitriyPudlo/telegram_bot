from random import choice
import telebot

token = '5359097635:AAGsjmkiJbmLfEtfFclA-prlkn2fH2Px2G8'

bot = telebot.TeleBot(token)


RANDOM_TASKS = ['Написать Гвидо письмо', 'Выучить Python', 'Записаться на курс в Нетологию', 'Посмотреть 4 сезон Рик и Морти']

todos = dict()


HELP = '''
Список доступных команд:
* show  - напечать все задачи на заданную дату
* add - добавить задачу
* random - добавить на сегодня случайную задачу
* help - Напечатать help
'''


def add_todo(date, task):
    date = date.lower()
    if todos.get(date) is not None:
        todos[date].append(task)
    else:
        todos[date] = [task]


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['random'])
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')


@bot.message_handler(commands=['add'])
def add(message):
    _, date, tail = message.text.split(maxsplit=2)
    task = ' '.join([tail])
    if len(task) < 3:
        bot.send_message(message.chat.id, 'Ошибка')
        return None
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')


@bot.message_handler(commands=['show'])
def print_(message):
    dates = [date.lower() for date in message.text.split()[1:]]
    for date in dates:
        if date in todos:
            tasks = f'На {date} запланипровано:'
            for task in todos[date]:
                tasks += f'''
[ ] {task}'''
        else:
            tasks = f'На {date} ничего не запланировано.'
        bot.send_message(message.chat.id, tasks)


bot.polling(none_stop=True)
