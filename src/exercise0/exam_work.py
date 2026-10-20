import time
import random
from exam_logic import calculate_exam_probabilities


def exam_work(student_list, examiner, questions_list, exam):
    """
    Функция, которую выполняет каждый экзаменатор в отдельном потоке.
    Принимает студентов одного за другим.
    """
    
    # Проверяем, не пора ли на обед (после 30 секунд работы)
    if examiner.work_time >= 30 and examiner.lunch_time == 0:
        examiner.lunch_time = random.randint(12, 18)  # Обед от 12 до 18 секунд
        time.sleep(examiner.lunch_time)               # Спим (отдыхаем)
    
    # Проходим по всем студентам
    for student in student_list:
        # Если студент ещё в очереди (не сдал и не провалил)
        if student.status == 'Очередь':
            start = time.time()  # Запоминаем время начала
            
            # Экзаменатор берёт студента
            examiner.current_student = student.name
            student.status = 'Сдает'  # Меняем статус на "сдаёт"
            
            # Время ответа зависит от длины имени экзаменатора (плюс-минус 1 секунда)
            time.sleep(len(examiner.name) + random.randint(-1, 1))
            
            # Проверяем знания студента
            if calculate_exam_probabilities(student, questions_list, exam) >= 2:
                student.status = 'Сдал'          # 2+ правильных ответа — сдал
            else:
                student.status = 'Не сдал'       # Меньше 2 — провал
                examiner.failed_students += 1    # Увеличиваем счётчик провалов
                exam.num_of_failes += 1          # Общий счётчик провалов
            
            finish = time.time()  # Запоминаем время окончания
            
            # Обновляем статистику экзаменатора
            examiner.total_students += 1
            examiner.work_time += round(finish - start, 2)   # Добавляем время работы
            student.time_of_exam = round(finish - start, 2)  # Запоминаем время студента