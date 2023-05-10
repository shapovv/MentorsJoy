# explanatory_note_code_blocks = {
#     'university': '',
#     'faculty': '',
#     'department': '',
#     'project_name': '',
#     'project_name_eng': '',
#     'number': '',
#     'supervisor_post': '',
#     'supervisor_name': '',
#     'akad_post': '',
#     'akad_name': '',
#     'student_name': '',
#     'group_number': '',
#     'year': '',
#     'month': '',
#     'day': '',
#     'grounds_for_development': '',
#     'functional_purpose': '',
#     'operational_purpose': '',
#     'brief_description': '',
#     'task_statement': '',
#     'description_architecture': '',
#     'justification_of_architecture': '',
#     'description_algorithm': '',
#     'rationale_algorithm': '',
#     'work_with_data_bases': '',
#     'input_output_data': '',
#     'composition_of_technical_means': '',
#     'justification_of_technical_means': '',
#     'economic_efficiency': '',
#     'perceived_need': '',
#     'advantages_over_analogues': '',
#     'sources': '',
#     'term_1': '',
#     'definition_1': ''
# }

explanatory_note_questions = [
    (
        '<b>Сначала заполним титульный лист.</b>\n\nВведите полное название ВУЗа, например "Национальный исследовательский университет Высшая Школа Экономики":',
        'university'),
    ('Введите факультет, например "Факультет компьютерных наук":', 'faculty'),
    ('Введите департамент, например "Департамент программной инженерии":', 'department'),
    ('Введите название работы, например «Генератор документации "Радость Научника"»:', 'project_name'),
    ('Введите название работы на английском языке, например «Documentation Constructor “Mentors Joy”»:',
     'project_name_eng'),
    (
        'Введите номер работы:\n\nПодсказка: в соответствии с ГОСТ 19.103-77 "Обозначения программ и программных документов", номер имеет вид RU.12345678.123456-01, где RU - код страны, 12345678 - код организации-разработчик, 123456-01 - регистрационный номер, который присваивается в соответствии с ОКП.:',
        'number'),
    (
        'Введите должность руководителя, согласовавшего документ, например "Научный руководитель, приглашенный преподаватель департамента программной инженерии":',
        'supervisor_post'),
    ('Введите ФИО научного руководителя в формате Фамилия И. О.:', 'supervisor_name'),
    (
        'Введите должность руководителя, утвердившего документ, например "Академический руководитель образовательной программы «Программная инженерия», кандидат технических наук":',
        'akad_post'),
    ('Введите ФИО академического руководителя в формате Фамилия И. О.:', 'akad_name'),
    ('Введите ФИО исполнителя в формате Фамилия И. О.:', 'student_name'),
    ('Введите номер группы, например "БПИ217":', 'group_number'),
    ('<b>Теперь заполнима дату, когда будет подписана пояснительная записка.</b>\n\nВведите год, например "2023":',
     'year'),
    ('Введите месяц в родительном падеже, например "Мая":', 'month'),
    ('Введите число, например "11":', 'day'),
    (
        '<b>Переходим к заполнению раздела "Введение".</b>\n\nВведите основания для разработки, это может быть, например, указ ректора или учебный план:',
        'grounds_for_development'),
    ('<b>Переходим к разделу "Назначение и область применения".</b>\n\nВведите функциональное назначение:',
     'functional_purpose'),
    ('Введите эксплуатационное назначение:', 'operational_purpose'),
    (
        'Напишите краткую характеристику области применения программы, например "«Генератор документации ‘‘Радость Научника’’» — прикладная программа, разрабатываемая с целью облегчения формирования и оформления документации.":',
        'brief_description'),
    ('<b>Переходим к разделу "Технические характеристики".</b>\n\nОпишите поставленные задачи на разработку программы:',
     'task_statement'),
    ('Опишите архитектуру программы:', 'description_architecture'),
    ('Обоснуйте выбор архитектуры программы:', 'justification_of_architecture'),
    ('Опишите алгоритм работы программы:', 'description_algorithm'),
    ('Обоснуйте выбор алгоритма работы программы:', 'rationale_algorithm'),
    ('Опишите работу с базами данных:', 'work_with_data_bases'),
    ('Опишите и обоснуйте выбор способа организации входных и выходных данных:', 'input_output_data'),
    ('Опишите состав технических и программных средств:', 'composition_of_technical_means'),
    ('Обоснуйте выбор технических и программных средств:', 'justification_of_technical_means'),
    (
        '<b>Переходим к разделу "Ожидаемые технико-экономические показатели".</b>\n\nОпишите ориентировочную экономическую эффективность:',
        'economic_efficiency'),
    ('Опишите предполагаемую потребность:', 'perceived_need'),
    ('Опишите экономические преимущества разработки по сравнению с отечественными и зарубежными аналогами:',
     'advantages_over_analogues'),
    (
        '<b>Переходим к разделу "Список использованных источников".</b>\n\nПо умолчанию в него включены 12 основных ГОСТ-ов, по которым оформляется пояснительная записка. Чтобы добавить свои источники, введите их через перевод строки в одном сообщении:',
        'sources'),
    (
        '<b>Наконец заполним одно из приложений в качестве примера.</b>\n\nНе забудьте дозаполнить таблицы, которые генерируются по умолчанию в приложениях. Вы сможете после сохранения документа в формате .docx.\n\nВведите любой технический термин из текста вашей пояснительной записки:',
        'term_1'),
    ('Введите определение введенного выше термина:', 'definition_1')
]
