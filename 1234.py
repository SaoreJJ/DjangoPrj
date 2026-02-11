import psycopg2

params = {
    'dbname': 'myproject_db',
    'user': 'myproject_user',
    'password': 'simple123',
    'host': 'localhost',
    'port': 5432,
}

print("Передаваемые параметры (repr):")
for k, v in params.items():
    print(f"{k}: {repr(v)}")

try:
    conn = psycopg2.connect(**params)
    print("✅ Подключение успешно!")
    conn.close()
except Exception as e:
    print("❌ Ошибка:", repr(e))