# Создайте test_db.py в корне проекта
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="testdb",
        user="postgres",
        password="simple123",  # ваш пароль
        host="localhost",
        port="5432"
    )
    print("✅ PostgreSQL подключен успешно!")
    conn.close()
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    print("\nПроверьте:")
    print("1. Запущен ли PostgreSQL?")
    print("2. Правильный ли пароль?")
    print("3. Существует ли БД testdb?")