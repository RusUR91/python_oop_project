import time
import threading
from prettytable import PrettyTable

from models import Students, Examiners, Questions, Exam
from exam_work import exam_work
from table_builder import (create_Students_table, create_final_table,
                           reset_student_final_tables)
from stats import best_students, worst_students, best_examiners, best_question, is_exam_success

# Глобальный флаг, который говорит, что все потоки закончили работу
all_threads_finished = threading.Event()


def read_students_file(file_name):
    """
    Читает файл со студентами.
    Каждая строка: "Имя Пол"
    Возвращает список студентов и объект со статистикой экзамена.
    """
    students = []
    exam = Exam()  # Создаём объект для статистики экзамена
    
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            name, gender = line.strip().split()
            student = Students(name, gender)
            students.append(student)
            exam.num_of_student += 1  # Считаем студентов
    
    return students, exam


def read_examiners_file(file_name):
    """
    Читает файл с экзаменаторами.
    Каждая строка: "Имя Пол"
    Возвращает список экзаменаторов.
    """
    examiners = []
    
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            name, gender = line.strip().split()
            examiner = Examiners(name, gender)
            examiners.append(examiner)
    
    return examiners


def read_questions_file(file_name):
    """
    Читает файл с вопросами.
    Каждая строка — это вопрос (предложение).
    Возвращает список вопросов.
    """
    questions = []
    
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            question = Questions(line.strip())
            questions.append(question)
    
    return questions


def update_tables_periodically(student_table, final_table, students_list, examiners_list, start_time):
    """
    Функция, которая работает в отдельном потоке.
    Каждые 3 секунды обновляет таблицы на экране, показывая текущий прогресс.
    """
    while not all_threads_finished.is_set():  # Пока экзамен не закончен
        current_time = time.time() - start_time  # Сколько времени прошло с начала
        
        # Создаём свежие таблицы
        create_Students_table(student_table, students_list)
        create_final_table(final_table, examiners_list, students_list)
        
        # Выводим всё на экран
        print(student_table)
        print(final_table)
        
        # Считаем, сколько студентов ещё не закончили
        waiting = sum(1 for student in students_list 
                     if student.status == "Очередь" or student.status == "Сдает")
        print(f'Осталось в очереди: {waiting} из {len(students_list)}')
        print(f'Время с момента начала экзамена: {current_time:.1f} секунд')
        
        # Очищаем таблицы для следующего обновления
        reset_student_final_tables(student_table, final_table)
        
        time.sleep(3)  # Ждём 3 секунды до следующего обновления


def main():
    """
    Главная функция.
    """
    # Пути к файлам с данными
    students_file = 'students.txt'
    examiners_file = 'examiners.txt'
    questions_file = 'questions.txt'
    
    # Загружаем данные из файлов
    students_list, exam = read_students_file(students_file)
    examiners_list = read_examiners_file(examiners_file)
    questions_list = read_questions_file(questions_file)
    
    # Создаём таблицы для отображения
    student_table = PrettyTable()
    final_table = PrettyTable()
    
    start_time = time.time()  # Запоминаем время начала экзамена
    
    # Запускаем фоновый поток для обновления таблиц на экране
    update_thread = threading.Thread(
        target=update_tables_periodically,
        args=(student_table, final_table, students_list, examiners_list, start_time),
        daemon=True  # daemon = True означает, что поток завершится, когда программа закончится
    )
    update_thread.start()
    
    # Запускаем отдельный поток для каждого экзаменатора
    threads = []
    for examiner in examiners_list:
        thread = threading.Thread(
            target=exam_work,
            args=(students_list, examiner, questions_list, exam)
        )
        thread.start()
        threads.append(thread)
    
    # Ждём, пока все экзаменаторы закончат работу
    for thread in threads:
        thread.join()
    
    # Сообщаем фоновому потоку, что экзамен закончен
    all_threads_finished.set()
    
    total_exam_time = time.time() - start_time  # Общее время экзамена
    
    # Ждём завершения фонового потока
    update_thread.join()
    
    # Создаём финальные таблицы с результатами
    create_Students_table(student_table, students_list)
    create_final_table(final_table, examiners_list, students_list)
    
    # Выводим финальные результаты
    print(student_table)
    print(final_table)
    
    print(f"Время с момента начала экзамена и до момента его завершения: {total_exam_time:.1f} секунд")
    print(f"Имена лучших студентов: {best_students(students_list, exam)}")
    print(f"Имена лучших экзаменаторов: {best_examiners(examiners_list)}")
    print(f"Имена студентов, которых после экзамена отчислят: {worst_students(students_list, exam)}")
    print(f"Лучшие вопросы: {best_question(exam)}")
    print(is_exam_success(exam))


# Запускаем программу
if __name__ == "__main__":
    main()