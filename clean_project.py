import os
import shutil
import sys


def clean_project():
    print("Очистка проекта...")

    # Удаляем базу данных
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("✓ Удалена db.sqlite3")

    # Удаляем миграции products
    mig_dir = 'products/migrations'
    if os.path.exists(mig_dir):
        for f in os.listdir(mig_dir):
            if f != '__init__.py':
                try:
                    os.remove(os.path.join(mig_dir, f))
                except:
                    pass
        print("✓ Очищены миграции products")

    # Удаляем миграции users
    mig_dir = 'users/migrations'
    if os.path.exists(mig_dir):
        for f in os.listdir(mig_dir):
            if f != '__init__.py':
                try:
                    os.remove(os.path.join(mig_dir, f))
                except:
                    pass
        print("✓ Очищены миграции users")

    # Удаляем __pycache__
    for root, dirs, files in os.walk('.'):
        for d in dirs:
            if d == '__pycache__':
                try:
                    shutil.rmtree(os.path.join(root, d))
                except:
                    pass

    print("✓ Удалены __pycache__")

    print("\nТеперь выполните:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser")
    print("4. python manage.py runserver")


if __name__ == '__main__':
    clean_project()