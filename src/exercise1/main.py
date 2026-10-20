import asyncio         
import aiohttp          
import os               
from prettytable import PrettyTable  
from urllib.parse import urlparse, unquote  


class ImageDownloader:
    """
    Класс, который управляет процессом скачивания картинок.
    Он запоминает все ссылки и результаты загрузки.
    """
    
    def __init__(self, save_dir: str):
        """
        Конструктор — вызывается при создании объекта.
        save_dir — папка, куда будут сохраняться картинки.
        """
        self.save_dir = save_dir           
        self.urls: list = []               # Список ссылок в том порядке, как их ввели
        self.results: dict = {}            

    def add_url(self, url: str) -> None:
        """
        Добавляет новую ссылку в список на скачивание.
        Сначала ставим статус 'Загрузка...'.
        """
        self.urls.append(url)                     # Добавляем ссылку в конец списка
        self.results[url] = 'Загрузка...'         # Помечаем, что загрузка началась

    async def download(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Асинхронная функция, которая скачивает одну картинку.
        'async' означает, что функция может выполняться параллельно с другими.
        """
        try:
            # Ставим таймаут 30 секунд — если картинка не скачается за 30 секунд, будет ошибка
            timeout = aiohttp.ClientTimeout(total=30)
            
            # Делаем GET-запрос к интернету, просим сервер отдать файл
            async with session.get(url, timeout=timeout) as response:
                
                # Если сервер ответил не "200", значит ошибка
                if response.status != 200:
                    self.results[url] = 'Ошибка'
                    return
                
                # Определяем имя файла из ссылки
                path_part = urlparse(url).path                   
                filename = unquote(os.path.basename(path_part))   
                
                # Если имя файла пустое, придумываем своё имя
                if not filename:
                    filename = f'image_{abs(hash(url)) % 100000}.bin'  # Создаём имя из хеша ссылки
                
                # Полный путь - папка + имя файла
                save_path = os.path.join(self.save_dir, filename)
                
                # Читаем содержимое картинки
                content = await response.read()
                
                # Сохраняем файл на диск
                with open(save_path, 'wb') as f:  # 'wb' — запись в двоичном режиме, для картинок
                    f.write(content)
                
                # Всё хорошо — помечаем как успех
                self.results[url] = 'Успех'
                
        except Exception:   # Если произошла любая ошибка (нет интернета, неверная ссылка и т.д.)
            self.results[url] = 'Ошибка'

    def print_summary(self) -> None:
        """
        Выводит красивую таблицу со всеми ссылками и их статусами (успех/ошибка).
        """
        print('\nСводка об успешных и неуспешных загрузках')
        
        # Создаём таблицу с двумя колонками: Ссылка и Статус
        table = PrettyTable(['Ссылка', 'Статус'])
        table.align['Ссылка'] = 'l'   # Выравнивание ссылок по левому краю
        table.align['Статус'] = 'c'   # Выравнивание статусов по центру
        
        # Добавляем в таблицу все ссылки и их статусы
        for url in self.urls:
            table.add_row([url, self.results.get(url, 'Ошибка')])
        
        print(table)


async def ainput(prompt: str = '') -> str:
    """
    Асинхронная версия обычного input().
    Нужна, чтобы программа могла принимать ввод от пользователя,
    НО при этом не блокировать скачивание картинок.
    Пока пользователь думает и вводит ссылку, картинки уже качаются!
    """
    loop = asyncio.get_running_loop()                     # Получаем главный цикл событий
    return await loop.run_in_executor(None, lambda: input(prompt))  # Запускаем обычный input в отдельном потоке


async def get_valid_save_dir() -> str:
    """
    Спрашивает у пользователя путь для сохранения файлов.
    Проверяет, есть ли доступ к этой папке.
    Если папки нет — создаёт её.
    Если доступа нет — просит ввести другой путь.
    """
    while True:
        # Просим пользователя ввести путь
        path = (await ainput('Введите путь для сохранения изображений: ')).strip()
        
        try:
            # Создаём папку, если её нет
            os.makedirs(path, exist_ok=True)
            
            # Проверяем, можем ли мы писать в эту папку
            test_path = os.path.join(path, '.write_access_check')
            with open(test_path, 'w') as f:   # Пробуем создать временный файл
                f.write('')
            os.remove(test_path)              # Удаляем временный файл
            
            # Если дошли до сюда — всё хорошо, возвращаем путь
            return path
            
        except (PermissionError, OSError, ValueError) as e:
            # Если произошла ошибка (нет прав, диск полный и т.д.)
            print(f"Ошибка: нет доступа к пути '{path}' → {e}")
            print('Пожалуйста, введите другой путь.\n')


async def main() -> None:
    """
    Главная функция.
    """
    # Спрашиваем у пользователя, куда сохранять картинки
    save_dir = await get_valid_save_dir()
    
    # Создаём объект, который будет управлять загрузками
    downloader = ImageDownloader(save_dir)
    
    # Список для хранения задач, каждая задача — это скачивание одной картинки
    tasks: list = []
    
    print('\nВводите ссылки на изображения (пустая строка — завершить ввод):')
    
    # Открываем одну сессию для всех запросов
    async with aiohttp.ClientSession() as session:
        
        # Бесконечный цикл — пока пользователь вводит ссылки
        while True:
            # Спрашиваем ссылку
            url = (await ainput('Ссылка: ')).strip()
            
            # Если пользователь ничего не ввёл (пустая строка) — выходим из цикла
            if not url:
                break
            
            # Добавляем ссылку в загрузчик
            downloader.add_url(url)
            
            # Создаём задачу на скачивание, начнётся сразу, параллельно с другими
            task = asyncio.create_task(downloader.download(session, url))
            tasks.append(task)
        
        # Проверяем, остались ли незавершённые загрузки
        pending = [t for t in tasks if not t.done()]
        if pending:
            print(f'\nЕщё загружается {len(pending)} файл(ов), подождите...')
        
        # Ждём завершения всех задач, даже если были ошибки
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    # Печатаем итоговую таблицу
    downloader.print_summary()

if __name__ == '__main__':
    asyncio.run(main())