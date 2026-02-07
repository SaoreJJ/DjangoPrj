import os
import sys
import subprocess

# Устанавливаем переменные окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Команды для выполнения
commands = [
    ['python', 'manage.py', 'makemigrations'],
    ['python', 'manage.py', 'migrate'],
    ['python', 'manage.py', 'createsuperuser'],
    ['python', 'manage.py', 'runserver']
]

print("Запуск свежей установки Django...")

# Выполняем команды
for i, cmd in enumerate(commands):
    print(f"\n[{i+1}/{len(commands)}] Выполняется: {' '.join(cmd)}")
    if i == 2:  # createsuperuser - запускаем в интерактивном режиме
        subprocess.run(cmd)
    else:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)