
class Students:
    """Класс для хранения данных о студенте"""
    def __init__(self, name, gender):
        self.name = name              
        self.gender = gender          
        self.status = "Очередь"       
        self.time_of_exam = 0         
        self.question = []            


class Examiners:
    """Класс для хранения данных о экзаменаторе"""
    def __init__(self, name, gender):
        self.name = name              
        self.gender = gender          
        self.status = 'free'          
        self.len_name = len(name)     
        self.current_student = None   
        self.total_students = 0       
        self.failed_students = 0      
        self.work_time = 0            
        self.lunch_time = 0           


class Questions:
    """Класс для хранения вопроса и его слов"""
    def __init__(self, text):
        self.text = text              
        self.words = text.split()     


class Exam:
    """Класс для хранения общей статистики экзамена"""
    def __init__(self):
        self.num_of_student = 0       
        self.num_of_failes = 0        
        self.best_answer = []         