# test_password.py
import psycopg2

# Пробуем разные варианты паролей
test_passwords = [
    'simple123',    # только цифры и латиница
    '123456',       # только цифры
    'password',     # только латиница
    '',             # пустой пароль
]

for password in test_passwords:
    try:
        print(f"Пробуем пароль: '{password}'")
        conn = psycopg2.connect(
            dbname="postgres",  # пробуем подключиться к системной БД
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        print(f"✅ Успешно! Пароль: '{password}'")
        conn.close()
        break
    except Exception as e:
        print(f"❌ Не удалось: {str(e)[:100]}")