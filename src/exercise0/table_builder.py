import random
from prettytable import PrettyTable  


def create_Students_table(table_name, students_list):
    """
    Создаёт таблицу со студентами: их имена, статус и время сдачи.
    """
    table_name.field_names = ["Student_name", "Status", "Time"]
    
    # Порядок сортировки статусов
    status_order = {
        "Сдает": 1,      
        "Очередь": 2,    
        "Сдал": 3,       
        "Не сдал": 4     
    }
    
    # Сортируем студентов по порядку статусов
    sorted_students = sorted(students_list, key=lambda student: status_order[student.status])
    
    # Добавляем строки в таблицу
    for student in sorted_students:
        status_to_display = "Очередь" if student.status == "Сдает" else student.status
        table_name.add_row([student.name, status_to_display, student.time_of_exam])


def create_Examiners_table(table_name, examiners_list, students_list):
    """
    Создаёт таблицу с экзаменаторами: их данные и статистика.
    """
    table_name.field_names = ["Examiner_name", "Gender",
                              "Len_name", "Current_student", "Total_students",
                              "Failed_students", "Work_time", "Lunch_time"]
    
    for examiner in examiners_list:
        # Добавляем строку для каждого экзаменатора
        table_name.add_row([
            examiner.name,                     
            examiner.gender,                   
            examiner.len_name,                 
            random.choice(students_list).name, 
            examiner.total_students,           
            examiner.failed_students,          
            examiner.work_time,                
            examiner.lunch_time                
        ])


def create_question_table(table_name, question_list):
    """
    Создаёт таблицу с вопросами и их словами.
    """
    table_name.field_names = ["Line", "Words"]
    for line in question_list:
        table_name.add_row([line.text, line.words])


def create_final_table(table_name, examiner_list, student_list):
    """
    Создаёт финальную таблицу с результатами экзаменаторов.
    """
    table_name.field_names = ["Преподаватель", "Текущий студент",
                              "Всего студентов", "Провалило", "Время работы"]
    
    for examiner in examiner_list:
        table_name.add_row([
            examiner.name,                    
            examiner.current_student,         
            examiner.total_students,          
            examiner.failed_students,         
            examiner.work_time                
        ])


def reset_student_final_tables(student_table, final_table):
    """
    Очищает таблицы, чтобы при следующем обновлении не было старых данных.
    """
    student_table.clear_rows()
    final_table.clear_rows()