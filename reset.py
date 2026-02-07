import sys
import os

# Добавьте путь проекта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Удалите все файлы .pyc для чистоты
import glob
for pyc in glob.glob("**/*.pyc", recursive=True):
    try:
        os.remove(pyc)
    except:
        pass

# Перезапустите процесс
print("Проект очищен. Теперь запустите команды вручную:")
print("1. python manage.py makemigrations")
print("2. python manage.py migrate")
print("3. python manage.py createsuperuser")