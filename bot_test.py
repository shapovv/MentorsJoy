import telebot
from telebot import types
from docxtpl import DocxTemplate

API_TOKEN = "6260404903:AAEU0Ax58ULUNvM9rBva_NR4cEIdTelM7OI"

bot = telebot.TeleBot(API_TOKEN)

tech_spec_code_blocks = {
    'university': '',
    'faculty': '',
    'department': '',
    'project_name': '',
    'project_name_eng': '',
    'number': '',
    'student_name': '',
    'group_number': '',
    'year': ''
}

explanatory_note_code_blocks = {
    'university': '',
    'faculty': '',
    'department': '',
    'project_name': '',
    'project_name_eng': '',
    'number': '',
    'student_name': '',
    'group_number': '',
    'year': '',
    'supervisor': ''
}

tech_spec_questions = [
    ('Введите ВУЗ:', 'university'),
    ('Введите факультет:', 'faculty'),
    ('Введите департамент:', 'department'),
    ('Введите название работы:', 'project_name'),
    ('Введите название работы на английском языке:', 'project_name_eng'),
    ('Введите номер работы:', 'number'),
    ('Введите ФИО исполнителя в формате (Иванов И. И.) :', 'student_name'),
    ('Введите номер группы в формате (БПИ217) :', 'group_number'),
    ('Введите год:', 'year')
]

explanatory_note_questions = [
    ('Введите ВУЗ:', 'university'),
    ('Введите факультет:', 'faculty'),
    ('Введите департамент:', 'department'),
    ('Введите название работы:', 'project_name'),
    ('Введите название работы на английском языке:', 'project_name_eng'),
    ('Введите номер работы:', 'number'),
    ('Введите ФИО исполнителя в формате (Иванов И. И.) :', 'student_name'),
    ('Введите номер группы в формате (БПИ217) :', 'group_number'),
    ('Введите год:', 'year'),
    ('Введите ФИО руководителя в формате (Петров П. П.) :', 'supervisor')
]

chat_steps = {}

current_document_type = {}


def create_ask_and_save_handlers(code_blocks, question, code_block_key):
    def ask_handler(message):
        msg = bot.send_message(message.chat.id, question)
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


def next_step_handler(message, step=0):
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


def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническое задание", callback_data="technical_specifications")
    button2 = types.InlineKeyboardButton("Пояснительная записка", callback_data="explanatory_note")
    keyboard.add(button1, button2)
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
    bot.send_message(message.chat.id, 'Процесс создания документа прерван.')
    document_type = current_document_type[message.chat.id]
    if document_type == "technical_specifications":
        create_document(message, tech_spec_code_blocks, 'tech_spec_maket.docx', 'technical_specifications')
    elif document_type == "explanatory_note":
        create_document(message, explanatory_note_code_blocks, 'explanatory_note_maket.docx', 'explanatory_note')


@bot.callback_query_handler(func=lambda call: True)
def document_template_handler(call):
    document_type = call.data
    current_document_type[call.message.chat.id] = document_type
    if document_type == "technical_specifications":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)
    elif document_type == "explanatory_note":
        chat_steps[call.message.chat.id] = 0
        next_step_handler(call.message, step=0)


@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)


@bot.message_handler(commands=['stop'])
def handle_stop_command(message):
    handle_stop(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
