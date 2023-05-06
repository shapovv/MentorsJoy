import telebot
from telebot import types
from docxtpl import DocxTemplate

API_TOKEN = "6260404903:AAEU0Ax58ULUNvM9rBva_NR4cEIdTelM7OI"

bot = telebot.TeleBot(API_TOKEN)

# Изменение 1
user_code_blocks = {}


# Изменение 2
def get_code_blocks_for_user(user_id):
    if user_id not in user_code_blocks:
        user_code_blocks[user_id] = {
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
            'brief_description': '',
            'grounds_for_development': '',
            'functional_purpose': '',
            'operational_purpose': '',
            'requirements_functions_performed': '',
            'organization_input_data': '',
            'organization_output_data': '',
            'requirements_time': '',
            'interface_requirements': '',
            'control_input_information': '',
            'control_output_information': '',
            'recovery_time': '',
            'climatic_conditions': '',
            'types_services': '',
            'number_and_qual_personnel': '',
            'parameters_technical_means': '',
            'programming_languages': '',
            'software': '',
            'protection_information': '',
            'labeling_and_packaging': '',
            'transportation_and_storage': '',
            'special_requirements': '',
            'special_requirements_for_documentation': '',
            'economic_efficiency': '',
            'estimated_need': '',
            'analogue_1': '',
            'analogue_2': '',
            'analogue_3': '',
            'characteristic_1': '',
            'characteristic_2': '',
            'characteristic_3': '',
            'characteristic_4': '',
            'characteristic_5': '',
            'types_of_tests': '',
            'general_requirements_acceptance_of_work': '',
            'sources': ''
        }
    return user_code_blocks[user_id]


questions = [
    (
        'Сначала заполним титульный лист.\n\nВведите полное название ВУЗа, например "Национальный исследовательский университет Высшая Школа Экономики":',
        'university'),
    ('Введите факультет, например "Факультет компьютерных наук":', 'faculty'),
    ('Введите департамент, например "Департамент программной инженерии":', 'department'),
    ('Введите название работы, например "Генератор документации "Радость Научника""::', 'project_name'),
    ('Введите название работы на английском языке, например «Documentation Constructor “Mentors Joy”»:',
     'project_name_eng'),
    (
        'Введите номер работы:\n\n Подсказка: в соотретствии с ГОСТ 19.103-77 "Обозначения программ и программных документов", номер имеет вид RU.12345678.123456-01, где RU - код страны, 12345678 - код организации-разработчик, 123456-01 - регистрационный номер, который присваивается в соответствии с ОКП.:',
        'number'),
    ('Введите ФИО исполнителя в формате Фамилия И. О.:', 'student_name'),
    ('Введите номер группы, например "БПИ217":', 'group_number'),
    ('Введите год::', 'year'),
    ('Введите ФИО научного руководителя в формате Фамилия И. О.:', 'supervisor_name'),
    ('Введите ФИО академического руководителя в формате Фамилия И. О.:', 'akad_name'),
    (
        'Переходим к заполнению раздела "Введение".\n\nНапишите краткую характеристику области применения программы, например "«Генератор документации ‘‘Радость Научника’’» — прикладная программа, разрабатываемая с целью облегчения формирования и оформления документации.":',
        'brief_description'),
    (
        'Переходим к разделу "Основания для разработки".\n\nВведите основания для разработки, это может быть, например, указ ректора или учебный план:',
        'grounds_for_development'),
    ('Переходим к разделу "Назначение разработки".\n\nВведите функциональное назначение:', 'functional_purpose'),
    ('Введите эксплуатационное назначение:', 'operational_purpose'),
    ('Переходим к разделу "Требования к программе".\n\nВведите требования к составу выполняемых функций:',
     'requirements_functions_performed'),
    ('Введите требования к организации входных данных:', 'organization_input_data'),
    ('Введите требования организация выходных данных:', 'organization_output_data'),
    ('Введите требования к временным характеристикам:', 'requirements_time'),
    ('Введите требования к интерфейсу:', 'interface_requirements'),
    ('Введите требования к контролю входной информации:', 'control_input_information'),
    ('Введите требования к контролю выходной информации:', 'control_output_information'),
    ('Введите требования к восстановлению после отказа:', 'recovery_time'),
    ('Введите требования к климатическим условиям эксплуатации:', 'climatic_conditions'),
    ('Введите требования к видам обсулживания:', 'types_services'),
    ('Введите требования к численности и квалификации персонала:', 'number_and_qual_personnel'),
    ('Введите требования к составу и параметрам технических средств:', 'parameters_technical_means'),
    ('Введите требования к исходным кодам и языкам программирования:', 'programming_languages'),
    ('Введите требования к программным средствам, используемым программой:', 'software'),
    ('Введите требования к защите информации и программ:', 'protection_information'),
    ('Введите требования к маркировке и упаковке:', 'labeling_and_packaging'),
    ('Введите требования к транспортированию и хранению:', 'transportation_and_storage'),
    ('Введите специальные требования:', 'special_requirements'),
    ('Переходим к разделу "Требования к документации".\n\nВведите специальные требования к программной документации:',
     'special_requirements_for_documentation'),
    ('Следующий раздел "Техникоэкономические показатели"\n\nОпишите ориентировочную экономическую эффективность:',
     'economic_efficiency'),
    ('Опишите предполагаемую потребность:', 'estimated_need'),
    (
        'Заполним сравнительную таблицу с аналогами. По умолчанию она имеет вид таблицы с тремя аналогами и пятью сравнительными характеристиками. В итоговом файле вы сможете изменить их количество.\n\nВведите название первого аналога:',
        'analogue_1'),
    ('Введите название второго аналога:', 'analogue_2'),
    ('Введите название третьего аналога:', 'analogue_3'),
    ('Введите первую сравнительную характеристику:', 'characteristic_1'),
    ('Введите вторую сравнительную характеристику:', 'characteristic_2'),
    ('Введите третью сравнительную характеристику:', 'characteristic_3'),
    ('Введите четвертую сравнительную характеристику:', 'characteristic_4'),
    ('Введите пятую сравнительную характеристику:', 'characteristic_5'),
    ('Седующий раздел "Порядок контроля и приемки".\n\nВведите виды испытаний:', 'types_of_tests'),
    ('Введите общие требования к приемке работы:', 'general_requirements_acceptance_of_work'),
    (
        'Заключительный раздел "Список использованных источников".\n\nПо умолчанию в него включены 10 основных ГОСТ-ов, по которым оформляется техническое задание. Чтобы добавить свои источники, введите их через перевод строки в одном сообщении:',
        'sources'),
]

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
