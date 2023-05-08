import telebot
from telebot import types
from docxtpl import DocxTemplate
from dotenv import load_dotenv
import os
import logging
import time
from tech_spec_data import tech_spec_code_blocks, tech_spec_questions
from explanatory_note_data import explanatory_note_code_blocks, explanatory_note_questions
from title_page_data import title_page_code_blocks, title_page_questions

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
last_chat_id = None

chat_steps = {}

current_document_type = {}


def create_ask_and_save_handlers(code_blocks, question, code_block_key):
    def ask_handler(message):
        msg = bot.send_message(message.chat.id, question, parse_mode='HTML')
        bot.register_next_step_handler(msg, save_handler)

    def save_handler(message):
        if message.text.startswith("/stop"):
            handle_stop(message)
            return
        code_blocks[code_block_key] = message.text
        next_step_handler(message, chat_steps[message.chat.id])

    return ask_handler, save_handler


tech_spec_handlers = [create_ask_and_save_handlers(tech_spec_code_blocks, question, key) for question, key in
                      tech_spec_questions]
explanatory_note_handlers = [create_ask_and_save_handlers(explanatory_note_code_blocks, question, key) for question, key
                             in explanatory_note_questions]
title_page_handlers = [create_ask_and_save_handlers(title_page_code_blocks, question, key) for question, key
                       in title_page_questions]


def next_step_handler(message, step=0):
    global last_chat_id
    last_chat_id = message.chat.id
    chat_steps[message.chat.id] = step + 1
    document_type = current_document_type[message.chat.id]
    if document_type == "technical_specifications":
        if step < len(tech_spec_handlers):
            ask_handler, _ = tech_spec_handlers[step]
            ask_handler(message)
        elif step == len(tech_spec_handlers):
            create_document(message, tech_spec_code_blocks, 'tech_spec_maket.docx', 'technical_specifications')
    elif document_type == "explanatory_note":
        if step < len(explanatory_note_handlers):
            ask_handler, _ = explanatory_note_handlers[step]
            ask_handler(message)
        elif step == len(explanatory_note_handlers):
            create_document(message, explanatory_note_code_blocks, 'explanatory_note_maket.docx', 'explanatory_note')
    elif document_type == "title_page":
        if step < len(title_page_handlers):
            ask_handler, _ = title_page_handlers[step]
            ask_handler(message)
        elif step == len(title_page_handlers):
            create_document(message, title_page_code_blocks, 'title_page_maket.docx', 'title_page')


def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническое задание", callback_data="technical_specifications")
    button2 = types.InlineKeyboardButton("Пояснительная записка", callback_data="explanatory_note")
    button3 = types.InlineKeyboardButton("Титульный лист", callback_data="title_page")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    bot.send_message(message.chat.id, "Выберите тип документа:", reply_markup=keyboard)


def create_document(message, code_blocks, template_name, output_name):
    template = DocxTemplate(template_name)
    template.render(code_blocks)
    filename = f'{output_name}_{message.from_user.id}.docx'
    template.save(filename)
    bot.send_message(message.chat.id, 'Документ успешно создан!')
    with open(filename, 'rb') as file:
        bot.send_document(message.chat.id, file)


def handle_stop(message):
    global last_chat_id
    last_chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Процесс создания документа прерван.')
    document_type = current_document_type[message.chat.id]
    if document_type == "technical_specifications":
        create_document(message, tech_spec_code_blocks, 'tech_spec_maket.docx', 'technical_specifications')
    elif document_type == "explanatory_note":
        create_document(message, explanatory_note_code_blocks, 'explanatory_note_maket.docx', 'explanatory_note')
    elif document_type == "title_page":
        create_document(message, title_page_code_blocks, 'title_page_maket.docx', 'title_page')


@bot.callback_query_handler(func=lambda call: True)
def document_template_handler(call):
    global last_chat_id
    last_chat_id = call.message.chat.id
    document_type = call.data
    current_document_type[call.message.chat.id] = document_type
    if document_type == "technical_specifications":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)
    elif document_type == "explanatory_note":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)
    elif document_type == "title_page":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)


@bot.message_handler(commands=['start'])
def handle_start(message):
    global last_chat_id
    last_chat_id = message.chat.id
    start(message)


@bot.message_handler(commands=['stop'])
def handle_stop_command(message):
    handle_stop(message)


@bot.message_handler(commands=['raise_error'])
def handle_raise_error_command(message):
    global last_chat_id
    last_chat_id = message.chat.id
    raise ValueError("Тестовое исключение")


def send_error_message(error_message, chat_id=None, user_id=None):
    global last_chat_id
    if chat_id is None and last_chat_id is not None:
        chat_id = last_chat_id

    if chat_id is not None:
        try:
            bot.send_message(chat_id, error_message)
        except Exception as e:
            logging.error(f"Failed to send error message: {e}")
    else:
        if user_id is None:
            user_id_str = "unknown"
        else:
            user_id_str = str(user_id)
        logging.error(f"Cannot send error message, chat_id is missing (user_id: {user_id_str}): {error_message}")


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            user_id = None
            if last_chat_id is not None:
                try:
                    user_id = bot.get_chat(last_chat_id).id
                except Exception:
                    pass
            logging.error(f"Error: {e}")
            send_error_message(f"Произошла ошибка: {e}", user_id=user_id)
            time.sleep(10)
