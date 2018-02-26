from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging, ephem, datetime

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    updater = Updater("546330958:AAF5Ah2_KBeZ8T83USCJUc2Rhe1IDiGsuwE")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet_answer))
    dp.add_handler(CommandHandler("wordcount", word_count))

    updater.start_polling()
    updater.idle()


def talk_to_me(bot, update):
    user_text = update.message.text 
    if user_text.endswith('='):
        oper_tuple = ('+','-', '/', '*')
        evaluation = user_text

        def calc(a, b, oper):
            try:
                a, b = float(a), float(b)
            except ValueError:
                update.message.reply_text('Некорректный ввод, нет одного или двух чисел')    
            try:
                op = {'+': (a+b), '-': (a-b),
                      '*': (a*b), '/': (a/b)}
                result = op[oper]
                return result
            except ZeroDivisionError:
                return 'Ай-яй-яй! Деление на ноль!'

            

        evaluation = evaluation.strip().replace('=','')
        f = 1
        for operation in oper_tuple:
            if evaluation.find(operation) != -1:
                a, b = evaluation.split(operation)
                update.message.reply_text(calc(a, b, operation))
                f = 0
                break    
        if f:
            update.message.reply_text('Нет математического оператора')
    else:
        update.message.reply_text(user_text)
    

def greet_user(bot, update):    
    update.message.reply_text('Hello!')


def planet_answer(bot,update):
    planets = { "mercury": ephem.Mercury, "venus": ephem.Venus,
            "mars": ephem.Mars, "jupiter": ephem.Jupiter, 
            "saturn": ephem.Saturn, "uranus": ephem.Uranus,
            "neptune": ephem.Neptune, "pluto": ephem.Pluto}
    
    planet = update.message.text 
    planet = planet.lower().replace('/planet ','')
    now = datetime.date.today()
    
    get_method = planets.get(planet)
    get_constellation = get_method(now)
    const = ephem.constellation(get_constellation)
    update.message.reply_text(const[1])


def word_count(bot,update):
    stroka = update.message.text
    stroka = stroka.lower().replace('/wordcount ','')
    special_char = ('@','#','$','%','^','&','*','-','+','/','=','!','?')

    if stroka:
        if stroka.startswith('"') and stroka.endswith('"'):
            words = stroka.replace('"','')
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

