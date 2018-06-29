import telepot

def handler(msg):
    chat_id = msg['chat']['id']
    chat_message = msg['text']

    main_keyboard = [['Option #1', 'Option #2'], ['Option #3', 'Option #4']]
    sub_keyboard = [['Sub option #1_1', 'Sub option #1_2'], ['Sub option #1_3', 'Sub option #1_4'],['Back to Main menu']]

    if chat_message=='/start':
        bot.sendMessage(chat_id, 'Main options', reply_markup={'keyboard': main_keyboard})
    elif chat_message in [j for i in main_keyboard for j in i]:
        # an option from Main keyboard is chosen:

        # Ex: Option #1 > You selected Option #1
        bot.sendMessage(chat_id, 'Main selected: %s' %chat_message)

        if chat_message == 'Option #1':
            sub_buttons = {'keyboard': sub_keyboard}
            bot.sendMessage(chat_id, 'Sub options', reply_markup=sub_buttons)

    elif chat_message in [j for i in sub_keyboard for j in i]:
        # an option from Sub keyboard is chosen:
        if chat_message == 'Sub option #1_1':
            bot.sendMessage(chat_id, 'Sub selected %s' %chat_message)
        if chat_message == 'Back to Main menu':
            bot.sendMessage(chat_id, 'Main options', reply_markup={'keyboard': main_keyboard})

    else:
        bot.sendMessage(chat_id, 'Invalid Message. please select an option from keyboard')

bot = telepot.TeleBot('528744932:AAEPt-yfHBZbNQ9aMIlAUyuMSTz-QilXM6M')
bot.message_loop(handler, run_forever=True)