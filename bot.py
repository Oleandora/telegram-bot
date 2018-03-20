from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, ephem, datetime, os

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    key = os.environ.get('MY_COOL_BOT_KEY')
    updater = Updater(key)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler('planet', planet_answer))
    dp.add_handler(CommandHandler('wordcount', word_count))

    updater.start_polling()
    updater.idle()


def calculate(operand1, operand2, sign):
    try:
        operand1, operand2 = float(operand1), float(operand2)
        calculation = {'+': lambda x, y: x + y,
                       '-': lambda x, y: x - y,
                       '*': lambda x, y: x * y,
                       '/': lambda x, y: x / y}
        result = calculation[sign](operand1, operand2)
        return result
    except ValueError as e:
        return 'Некорректный ввод, нет одного или двух чисел: {}'.format(e.args[0])
    except ZeroDivisionError as e:
        return 'Ай-яй-яй! Деление на ноль! Фу быть таким!: {}'.format(e.args[0])


def talk_to_me(bot, update):
    user_text = update.message.text
    if user_text.endswith('='):
        sign_tuple = ('+', '-', '/', '*')
        evaluation = user_text
        evaluation = evaluation.strip().replace('=', '')
        for operation in sign_tuple:
            if operation in evaluation:
                operand1, operand2 = evaluation.split(operation)
                update.message.reply_text(calculate(operand1, operand2, operation))
                break
        else:
            update.message.reply_text('Некорректный ввод, нет математического оператора')
    else:
        update.message.reply_text(user_text)


def greet_user(bot, update):
    update.message.reply_text('Hello!')


def planet_answer(bot,update):
    planets = { 'mercury': ephem.Mercury, 'venus': ephem.Venus,
                'mars': ephem.Mars, 'jupiter': ephem.Jupiter,
                'saturn': ephem.Saturn, 'uranus': ephem.Uranus,
                'neptune': ephem.Neptune, 'pluto': ephem.Pluto}

    planet = update.message.text
    planet = planet.lower().replace('/planet ','')
    now = datetime.date.today()

    get_method = planets.get(planet)
    get_constellation = get_method(now)
    const = ephem.constellation(get_constellation)
    update.message.reply_text(const[1])


def word_count(bot,update):
    input_date = update.message.text
    input_date = input_date.lower().replace('/wordcount ','')
    special_char = ('@', '#', '$', '%', '^', '&', '*', '-', '+', '/', '=', '!', '?')

    if input_date:
        if input_date.startswith('"') and input_date.endswith('"'):
            words = input_date.replace('"','')
            words = words.strip()
            words = words.split()
            number_of_words = len(words)
            for word in words:
                if word in special_char:
                    number_of_words -= 1
                try:
                    # проверяется, является ли слово числом
                    if float(word):
                        number_of_words -= 1
                    elif int(word):
                        number_of_words -= 1
                except ValueError: 
                    # если не преобразуется в число, значит это слово
                    pass 
        else:
            update.message.reply_text('Вы не написали слова в кавычках')
            number_of_words = 0         
    else:
        update.message.reply_text('Вы ничего не написали')
        number_of_words = 0
    update.message.reply_text('Количество слов: {0}'.format(number_of_words))    


main()
