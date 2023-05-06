from docxtpl import DocxTemplate

# Загрузите шаблон .docx
template = DocxTemplate('maket.docx')

# Создайте словарь с кодом для замены
code_blocks = {
    'vuz': 'ВШЭ',
    'faculty': 'Факультет комп наук',
    'department': 'департаментик',
    'name': 'Радость научника!!!!',
    'number': '1234567890987654321'
}

# Замените текст-заполнители данными из словаря
template.render(code_blocks)

# Сохраните изменения в новом файле
template.save('result.docx')
