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
from docx2pdf import convert

OUTPUT_FOLDER = "output_files"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

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


title_page_handlers = [create_ask_and_save_handlers(title_page_code_blocks, question, key) for question, key
                       in title_page_questions]
tech_spec_handlers = [create_ask_and_save_handlers(tech_spec_code_blocks, question, key) for question, key in
                      tech_spec_questions]
explanatory_note_handlers = [create_ask_and_save_handlers(explanatory_note_code_blocks, question, key) for question, key
                             in explanatory_note_questions]


def next_step_handler(message, step=0):
    global last_chat_id
    last_chat_id = message.chat.id
    chat_steps[message.chat.id] = step + 1
    document_type = current_document_type[message.chat.id]
    if document_type == "title_page":
        if step < len(title_page_handlers):
            ask_handler, _ = title_page_handlers[step]
            ask_handler(message)
        elif step == len(title_page_handlers):
            send_format_choice(message)
    elif document_type == "technical_specifications":
        if step < len(tech_spec_handlers):
            ask_handler, _ = tech_spec_handlers[step]
            ask_handler(message)
        elif step == len(tech_spec_handlers):
            send_format_choice(message)
    elif document_type == "explanatory_note":
        if step < len(explanatory_note_handlers):
            ask_handler, _ = explanatory_note_handlers[step]
            ask_handler(message)
        elif step == len(explanatory_note_handlers):
            send_format_choice(message)


def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Титульный лист", callback_data="title_page")
    button2 = types.InlineKeyboardButton("Техническое задание", callback_data="technical_specifications")
    button3 = types.InlineKeyboardButton("Пояснительная записка", callback_data="explanatory_note")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    bot.send_message(message.chat.id, "Выберите тип документа:", reply_markup=keyboard)


def update_document_choice_to_inactive(chat_id, message_id, selected_document_type):
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("Титульный лист" + (" ✅" if selected_document_type == "title_page" else " ❌"),
                                         callback_data="ignore")
    button2 = types.InlineKeyboardButton(
        "Техническое задание" + (" ✅" if selected_document_type == "technical_specifications" else " ❌"),
        callback_data="ignore")
    button3 = types.InlineKeyboardButton(
        "Пояснительная записка" + (" ✅" if selected_document_type == "explanatory_note" else " ❌"),
        callback_data="ignore")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)

    bot.edit_message_text("Выберите тип документа:", chat_id=chat_id, message_id=message_id, reply_markup=keyboard)


def send_format_choice(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("DOCX", callback_data="format_docx")
    button2 = types.InlineKeyboardButton("PDF", callback_data="format_pdf")

    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(message.chat.id, "Выберите в каком формате вы хотите получить документ:", reply_markup=keyboard)


def send_restart_choice(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Создать новый документ", callback_data="restart")
    button2 = types.InlineKeyboardButton("Закончить", callback_data="finish")

    keyboard.add(button1)
    keyboard.add(button2)

    sent_message = bot.send_message(message.chat.id, "Что вы хотите сделать дальше?", reply_markup=keyboard)
    return sent_message.message_id


def update_buttons_to_inactive(chat_id, message_id, selected_button):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Создать новый документ" + (" ✅" if selected_button == "new_document" else " ❌"), callback_data="ignore")
    button2 = types.InlineKeyboardButton("Закончить" + (" ✅" if selected_button == "finish" else " ❌"), callback_data="ignore")

    button1.url = None
    button2.url = None

    keyboard.add(button1)
    keyboard.add(button2)

    bot.edit_message_text("Что вы хотите сделать дальше?", chat_id=chat_id, message_id=message_id, reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: call.data == "finish")
def finish_handler(call):
    update_buttons_to_inactive(call.message.chat.id, call.message.message_id, "finish")
    bot.send_message(call.message.chat.id,
                     "Благодарим Вас за использование нашего бота!\n\nC уважением, <b>Mentors Joy</b>.",
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: call.data.startswith("format_"))
def format_choice_handler(call):
    global last_chat_id
    last_chat_id = call.message.chat.id
    format_choice = call.data.split("_")[1]

    document_type = current_document_type[call.message.chat.id]
    if document_type == "technical_specifications":
        create_document(call.message, tech_spec_code_blocks, 'tech_spec_maket.docx', 'technical_specifications',
                        format_choice)
    elif document_type == "explanatory_note":
        create_document(call.message, explanatory_note_code_blocks, 'explanatory_note_maket.docx', 'explanatory_note',
                        format_choice)
    elif document_type == "title_page":
        create_document(call.message, title_page_code_blocks, 'title_page_maket.docx', 'title_page', format_choice)


def create_document(message, code_blocks, template_name, output_name, file_format):
    template = DocxTemplate(template_name)
    template.render(code_blocks)
    filename = os.path.join(OUTPUT_FOLDER, f'{output_name}_{message.from_user.id}.docx')
    pdf_filename = os.path.join(OUTPUT_FOLDER, f'{output_name}_{message.from_user.id}.pdf')
    template.save(filename)

    if file_format == "docx":
        with open(filename, 'rb') as file:
            bot.send_document(message.chat.id, file)
    elif file_format == "pdf":
        convert(filename, pdf_filename)

        with open(pdf_filename, 'rb') as file:
            bot.send_document(message.chat.id, file)
    send_restart_choice(message)

    # Удалить .docx и .pdf файлы после отправки?
    # os.remove(filename)
    # os.remove(pdf_filename)


@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart_handler(call):
    update_buttons_to_inactive(call.message.chat.id, call.message.message_id, "new_document")
    start(call.message)


def handle_stop(message):
    global last_chat_id
    last_chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Процесс создания документа прерван.')
    document_type = current_document_type[message.chat.id]
    if document_type == "technical_specifications":
        send_format_choice(message)
    elif document_type == "explanatory_note":
        send_format_choice(message)
    elif document_type == "title_page":
        send_format_choice(message)


@bot.callback_query_handler(func=lambda call: True)
def document_template_handler(call):
    global last_chat_id
    last_chat_id = call.message.chat.id
    document_type = call.data

    if document_type == "ignore":
        return  # Завершить обработчик, если callback_data равно "ignore"

    update_document_choice_to_inactive(call.message.chat.id, call.message.message_id, document_type)

    current_document_type[call.message.chat.id] = document_type
    if document_type == "technical_specifications":
        # bot.send_message(call.message.chat.id,
        #                  "<b>Приступим к созданию вашего технического задания.<b>\n Сейчас мы поэтапно пройдём по всем пунктам, начиная с титульного листа и заканчивая списком литературы. Следуйте дальнейшим указаниям и подсказкам. \n\nВ любом месте вы можете остановиться и отправить ответ позднее, а если захотите закончить и получить не док онца заполненный документ, введите /stop. \n\nЕсли вы хотите пропустить любой шаг, необходимо отправить в ответ любой символ, тогда вы сможете заполнить этот раздел самостоятельно в итоговом документе.",
        #                  parse_mode='HTML')
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