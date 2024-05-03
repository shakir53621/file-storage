import os


def find_and_delete_file(directory: str, file_name: str):
    # Проходим по всем поддиректориям и файлам в директории
    for root, dirs, files in os.walk(directory):

        if file_name in files:
            # Путь к файлу
            file_path = os.path.join(root, file_name)
            # Удаляем файл
            os.remove(file_path)
            print(f"Файл '{file_name}' был найден и удален.")
            return True

    print(f"Файл '{file_name}' не найден.")
    return False
