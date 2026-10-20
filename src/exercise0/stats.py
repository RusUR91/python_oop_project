from collections import Counter  # Счётчик для подсчёта повторяющихся элементов


def best_students(student_list, exam):
    """
    Находит лучших студентов — тех, кто сдал экзамен быстрее всех.
    """
    if not student_list:
        return 0
    
    best_students = []
    
    # Если не все студенты провалили экзамен
    if exam.num_of_failes != exam.num_of_student:
        # Находим минимальное время среди сдавших
        min_time = min(student.time_of_exam for student in student_list if student.status == 'Сдал')
        
        # Собираем имена всех, кто сдал за минимальное время
        for student in student_list:
            if student.time_of_exam == min_time and student.status == 'Сдал':
                best_students.append(student.name)
    
    return ', '.join(best_students)


def worst_students(student_list, exam):
    """
    Находит худших студентов — тех, кто провалил экзамен и сделал это быстрее всех.
    """
    if not student_list:
        return 0
    
    worst_students = []
    
    # Если есть провалившие студенты
    if exam.num_of_failes > 0:
        # Находим минимальное время среди проваливших
        min_time = min(student.time_of_exam for student in student_list if student.status == 'Не сдал')
        
        # Собираем имена всех, кто провалил за минимальное время
        for student in student_list:
            if student.time_of_exam == min_time and student.status == 'Не сдал':
                worst_students.append(student.name)
    
    return ', '.join(worst_students)


def best_examiners(examiners_list):
    """
    Находит лучших экзаменаторов — тех, у кого наименьший процент проваливших студентов.
    """
    if not examiners_list:
        return 0
    
    best_examiners = []
    
    # Считаем процент провалов для каждого экзаменатора, округляем до целого числа
    failure_percentages = [
        round((examiner.failed_students * 100 / examiner.total_students))
        for examiner in examiners_list
    ]
    
    best = min(failure_percentages)  # Наименьший процент — лучший
    
    # Собираем имена экзаменаторов с наилучшим результатом
    for examiner in examiners_list:
        if round(examiner.failed_students * 100 / examiner.total_students) == best:
            best_examiners.append(examiner.name)
    
    return ', '.join(best_examiners)


def best_question(exam):
    """
    Находит лучшие вопросы — те, на которые студенты отвечали правильно чаще всего.
    """
    count = Counter(exam.best_answer)  # Считаем, сколько раз встретился каждый вопрос
    
    if not count:
        return ''
    
    max_count = max(count.values())     # Максимальное количество правильных ответов
    # Собираем вопросы с максимальным количеством правильных ответов
    most_common_elements = [element for element, cnt in count.items() if cnt == max_count]
    
    return ', '.join(most_common_elements)


def is_exam_success(exam):
    """
    Определяет, удался ли экзамен в целом.
    Экзамен считается удачным, если провалило меньше 15% студентов.
    """
    failure_rate = (100 * exam.num_of_failes / exam.num_of_student)
    
    if failure_rate < 15:
        return "Экзамен удался"
    else:
        return "Экзамен не удался"