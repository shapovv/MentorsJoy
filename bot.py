import telebot
from telebot import types
from docxtpl import DocxTemplate

API_TOKEN = "6260404903:AAEU0Ax58ULUNvM9rBva_NR4cEIdTelM7OI"

bot = telebot.TeleBot(API_TOKEN)

code_blocks = {
    'university': '',
    'faculty': '',
    'department': '',
    'project_name': '',
    'project_name_eng': '',
    'number': '',
    'student_name': '',
    'group_number': '',
    'year': '',
    'supervisor_name': '',
    'akad_name': '',
    'brief_description': '',  # Краткая характеристика области применения программы
    'annotation': '',
    'grounds_for_development': '',  # Основания для разработки
    'functional_purpose': '',  # Функциональное назначение
    'operational_purpose': '',  # Эксплуатационное назначение

}


def start(message):
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Техническое задание", callback_data="technical_specifications")
    button2 = types.InlineKeyboardButton("Пояснительная записка", callback_data="explanatory_note")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Выберите тип документа:", reply_markup=keyboard)


def ask_university(message):
    msg = bot.send_message(message.chat.id, 'Введите ВУЗ:')
    bot.register_next_step_handler(msg, save_university)


def save_university(message):
    code_blocks['university'] = message.text
    ask_faculty(message)


def ask_faculty(message):
    msg = bot.send_message(message.chat.id, 'Введите факультет:')
    bot.register_next_step_handler(msg, save_faculty)


def save_faculty(message):
    code_blocks['faculty'] = message.text
    ask_department(message)


def ask_department(message):
    msg = bot.send_message(message.chat.id, 'Введите департамент:')
    bot.register_next_step_handler(msg, save_department)


def save_department(message):
    code_blocks['department'] = message.text
    ask_project_name(message)


def ask_project_name(message):
    msg = bot.send_message(message.chat.id, 'Введите название работы:')
    bot.register_next_step_handler(msg, save_project_name)


def save_project_name(message):
    code_blocks['project_name'] = message.text
    ask_project_name_eng(message)


def ask_project_name_eng(message):
    msg = bot.send_message(message.chat.id, 'Введите название работы на английском языке:')
    bot.register_next_step_handler(msg, save_project_name_eng)


def save_project_name_eng(message):
    code_blocks['project_name_eng'] = message.text
    ask_number(message)


def ask_number(message):
    msg = bot.send_message(message.chat.id, 'Введите номер работы:')
    bot.register_next_step_handler(msg, save_number)


def save_number(message):
    code_blocks['number'] = message.text
    ask_student_name(message)


def ask_student_name(message):
    msg = bot.send_message(message.chat.id, 'Введите ФИО исполнителя в формате (Иванов И. И.) :')
    bot.register_next_step_handler(msg, save_student_name)


def save_student_name(message):
    code_blocks['student_name'] = message.text
    ask_group_number(message)


def ask_group_number(message):
    msg = bot.send_message(message.chat.id, 'Введите номер группы в формате (БПИ217) :')
    bot.register_next_step_handler(msg, save_group_number)


def save_group_number(message):
    code_blocks['group_number'] = message.text
    ask_year(message)


def ask_year(message):
    msg = bot.send_message(message.chat.id, 'Введите год:')
    bot.register_next_step_handler(msg, save_year)


def save_year(message):
    code_blocks['year'] = message.text
    ask_supervisor_name(message)


def ask_supervisor_name(message):
    msg = bot.send_message(message.chat.id, 'Введите ФИО научного руководителя в формате (Иванов И. И.):')
    bot.register_next_step_handler(msg, save_supervisor_name)


def save_supervisor_name(message):
    code_blocks['supervisor_name'] = message.text
    ask_akad_name(message)


def ask_akad_name(message):
    msg = bot.send_message(message.chat.id, 'Введите ФИО академического руководителя в формате (Иванов И. И.):')
    bot.register_next_step_handler(msg, save_akad_name)


def save_akad_name(message):
    code_blocks['akad_name'] = message.text
    ask_brief_description(message)


def ask_brief_description(message):
    msg = bot.send_message(message.chat.id, 'Введите краткую характеристику области применения программы:')
    bot.register_next_step_handler(msg, save_brief_description)


def save_brief_description(message):
    code_blocks['brief_description'] = message.text
    ask_annotation(message)


def ask_annotation(message):
    msg = bot.send_message(message.chat.id, 'Введите аннотацию:')
    bot.register_next_step_handler(msg, save_annotation)


def save_annotation(message):
    code_blocks['annotation'] = message.text
    ask_grounds_for_development(message)


def ask_grounds_for_development(message):
    msg = bot.send_message(message.chat.id, 'Введите основания для разработки:')
    bot.register_next_step_handler(msg, save_grounds_for_development)


def save_grounds_for_development(message):
    code_blocks['grounds_for_development'] = message.text
    ask_functional_purpose(message)


def ask_functional_purpose(message):
    msg = bot.send_message(message.chat.id, 'Введите функциональное назначение:')
    bot.register_next_step_handler(msg, save_functional_purpose)


def save_functional_purpose(message):
    code_blocks['functional_purpose'] = message.text
    ask_operational_purpose(message)


def ask_operational_purpose(message):
    msg = bot.send_message(message.chat.id, 'Эксплуатационное назначение:')
    bot.register_next_step_handler(msg, save_operational_purpose)


def save_operational_purpose(message):
    code_blocks['operational_purpose'] = message.text
    create_document(message)


def create_document(message):
    template = DocxTemplate('maket.docx')
    template.render(code_blocks)
    filename = f'result_{message.from_user.id}.docx'  # Изменение названия файла
    template.save(filename)
    bot.send_message(message.chat.id, 'Документ успешно создан!')
    with open(filename, 'rb') as file:
        bot.send_document(message.chat.id, file)


@bot.callback_query_handler(func=lambda call: True)
def document_template_handler(call):
    document_type = call.data
    if document_type == "technical_specifications":
        ask_university(call.message)
    elif document_type == "explanatory_note":
        # Здесь можно добавить шаги для работы с пояснительной запиской
        pass


# Здесь можно добавить код для обработки других типов документов
@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)