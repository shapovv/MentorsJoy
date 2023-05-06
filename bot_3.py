import telebot
from telebot import types
from docxtpl import DocxTemplate
from dictionaries_for_technical_task import get_code_blocks_for_user, questions

API_TOKEN = "6260404903:AAEU0Ax58ULUNvM9rBva_NR4cEIdTelM7OI"

bot = telebot.TeleBot(API_TOKEN)


chat_steps = {}


def create_ask_and_save_handlers(question, code_block_key):
    def ask_handler(message):
        msg = bot.send_message(message.chat.id, question)
        bot.register_next_step_handler(msg, save_handler)

    def save_handler(message):
        if message.text.startswith("/stop"):
            handle_stop(message)
            return
        code_blocks = get_code_blocks_for_user(message.from_user.id)
        code_blocks[code_block_key] = message.text
        next_step_handler(message, chat_steps[message.chat.id])

    return ask_handler, save_handler


handlers = [create_ask_and_save_handlers(question, key) for question, key in questions]


def next_step_handler(message, step=0):
    chat_steps[message.chat.id] = step + 1
    if step < len(handlers):
        ask_handler, _ = handlers[step]
        ask_handler(message)
    elif step == len(handlers):
        create_document(message)


def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническое задание", callback_data="technical_specifications")
    button2 = types.InlineKeyboardButton("Пояснительная записка", callback_data="explanatory_note")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите тип документа:", reply_markup=keyboard)


def create_document(message):
    template = DocxTemplate('maket.docx')
    code_blocks = get_code_blocks_for_user(message.from_user.id)
    template.render(code_blocks)
    filename = f'result_{message.from_user.id}.docx'
    template.save(filename)
    bot.send_message(message.chat.id, 'Документ успешно создан!')
    with open(filename, 'rb') as file:
        bot.send_document(message.chat.id, file)


def handle_stop(message):
    bot.send_message(message.chat.id, 'Процесс создания документа прерван.')
    create_document(message)


@bot.callback_query_handler(func=lambda call: True)
def document_template_handler(call):
    document_type = call.data
    if document_type == "technical_specifications":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)
    elif document_type == "explanatory_note":
        # Здесь можно добавить шаги для работы с пояснительной запиской
        pass


@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)


@bot.message_handler(commands=['stop'])
def handle_stop_command(message):
    handle_stop(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
