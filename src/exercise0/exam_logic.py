import random
from models import Exam

# Золотое сечение, нужно для того чтобы одни слова выбирались чаще, чем другие
PHI = (1 + 5 ** 0.5) / 2


def calculate_golden_ratio_probabilities(words_count):
    """
    Создаёт список вероятностей для каждого слова.
    Первое слово получает самый большой вес (~62%), второе — меньше, и так далее.
    
    """
    probabilities = []
    remaining_probability = 1  # Начинаем со 100% вероятности
    
    for i in range(words_count):
        if i != words_count - 1: 
            # Каждый следующий вес в 1.618 раз меньше предыдущего
            result = remaining_probability / PHI
            probabilities.append(result)
            remaining_probability -= result
        else:  # Последнее слово получает всё, что осталось
            probabilities.append(remaining_probability)
    
    return probabilities


def examiner_choice(words, probabilities, q=1 / 3):
    """
    Экзаменатор выбирает "правильные" ответы на вопрос.
    Он обязательно выбирает первое слово, а потом с вероятностью 1/3 добавляет ещё слова.
    """
    chosen_words = []
    
    # Сначала выбираем первое слово (с учетом вероятностей)
    first_word = random.choices(words, weights=probabilities, k=1)[0]
    chosen_words.append(first_word)
    
    # С вероятностью 1/3 добавляем ещё слова, пока не надоест
    while random.random() <= q:
        # Остались слова, которые ещё не выбрали
        remaining_words = [word for word in words if word not in chosen_words]
        remaining_probs = [prob for word, prob in zip(words, probabilities) if word not in chosen_words]
        
        if not remaining_words:
            break  # Слова кончились
        
        # Выбираем следующее слово
        next_word = random.choices(remaining_words, weights=remaining_probs, k=1)[0]
        chosen_words.append(next_word)
    
    return chosen_words


def calculate_exam_probabilities(student, questions_list, exam):
    """
    Главная функция проверки знаний студента.
    Возвращает количество правильных ответов (0, 1, 2 или 3).
    """
    result = 0
    
    # У экзаменатора может быть разное настроение (вероятности из задания)
    # 1/8 = 12.5% — плохое (сразу провал)
    # 2/8 = 25% — хорошее (сразу успех)
    # 5/8 = 62.5% — нейтральное (честная проверка)
    mood_probabilities = [1 / 8, 1 / 4, 5 / 8]
    mood = random.choices(['bad', 'good', 'neutral'], weights=mood_probabilities, k=1)[0]
    
    if mood == 'good':
        # Хорошее настроение — студент автоматически сдал (3 балла)
        result = 3
        
    elif mood == 'neutral':
        # Нейтральное настроение — проверяем 3 вопроса
        for i in range(3):
            # Берём случайный вопрос из списка
            question = random.choice(questions_list)
            words_count = len(question.words)
            
            # Считаем вероятности для слов (по золотому сечению)
            probabilities = calculate_golden_ratio_probabilities(words_count)
            
            # Студент выбирает слово (какой ответ даёт)
            student_answer = random.choices(question.words, weights=probabilities, k=1)[0]
            
            # Экзаменатор выбирает "правильные" ответы
            examiner_answer = examiner_choice(question.words, probabilities)
            
            # Если ответ студента совпал с одним из правильных — плюс балл
            if student_answer in examiner_answer:
                result += 1
                exam.best_answer.append(question.text)  # Запоминаем хороший вопрос
    else:
        # Плохое настроение — студент сразу провалил (0 баллов)
        result = 0
    
    return result