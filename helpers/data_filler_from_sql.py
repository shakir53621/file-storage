import os

import psycopg2

from app.config import settings


def execute_sql_script(sql_script_file: str) -> None:
    """Функция чтения sql файла, и запуска данного скрипта для БД"""
    with open(sql_script_file, encoding='windows-1251') as file:
        sql_script = file.read()

    connection = psycopg2.connect(
        host=settings.DB_HOST,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT
    )

    cursor = connection.cursor()

    try:
        cursor.execute(sql_script)
        connection.commit()
    except Exception as e:
        print(f"Error executing script {sql_script_file}: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


# Директория с SQL скриптами
sql_directory = "./helpers/sql"

# Получаем список файлов в директории
script_files = [os.path.join(sql_directory, filename) for filename in os.listdir(sql_directory) if
                filename.endswith(".sql")]

print(script_files)
# Выполняем каждый SQL скрипт
for script_file in script_files:
    execute_sql_script(script_file)

print("All SQL scripts executed successfully.")
