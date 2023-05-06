def fill_template(template_path, output_path, variables):
    with open(template_path, 'r', encoding='utf-8') as template_file:
        content = template_file.read()

    for key, value in variables.items():
        content = content.replace('{{' + key + '}}', value)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)


if __name__ == '__main__':
    variables = {
        'universityname': 'ВЫСШАЯ ШКОЛА ЭКОНОМИКИ',
        'facultyname': 'Факультет компьютерных наук',
        'departmentname': 'Кафедра теории функций и геометрии',
        'thesistitle': 'Генератор документации Радость научника',
        'thesisdirection': '010100 Математика',
        'programname': 'Вещественный, комплексный и функциональный анализ',
        'defenseDate': '27.05.2015',
        'studentName': 'Шаповалов А. С.',
        'supervisorName': 'Т.Я. Азизов',
        'supervisorDegree': 'д.физ.-мат.н., проф.',
        'departmentHeadName': 'Е.М. Семёнов',
        'departmentHeadDegree': 'д.физ.-мат.н.,  проф.',
        'yearOfCompletion': '2015',
    }

    fill_template('template.tex', 'output.tex', variables)
