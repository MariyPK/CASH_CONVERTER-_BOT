import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CashConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message:  telebot.types.Message):
    text = ('Для конвертации введите:\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n Указывайте название валюты в единственном числе!\nУвидеть список доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message:  telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text= '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message:  telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CashConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()

