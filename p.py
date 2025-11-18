import os
import sys

output_file = './output.txt'
script_name = os.path.basename(sys.argv[0])
excluded_files = [output_file, script_name]
excluded_dirs = ['minio-data', 'clickhouse-data', 'logs']
root_dir = os.getcwd()


def is_hidden(filepath):
    """Проверяет, является ли файл/папка скрытой"""
    name = os.path.basename(filepath)

    # Для Windows: атрибут hidden
    if os.name == 'nt':
        try:
            import ctypes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(filepath)
            return attrs != -1 and (attrs & 2) != 0
        except:
            pass

    # Для Unix/Linux/MacOS: файлы/папки, начинающиеся с точки
    return name.startswith('.')


with open(output_file, 'w', encoding='utf-8') as f:
    # Записываем директорию запуска
    f.write(f"Скрипт запущен в папке: {root_dir}\n\n")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Пропускаем исключенные директории
        if any(excluded_dir in dirpath for excluded_dir in excluded_dirs):
            continue

        # Пропускаем скрытые директории
        if is_hidden(dirpath):
            continue

        # Фильтруем скрытые папки из dirnames (это также предотвращает рекурсивный обход)
        dirnames[:] = [d for d in dirnames if not is_hidden(os.path.join(dirpath, d))]

        # Формируем относительный путь
        relative_path = os.path.relpath(dirpath, root_dir)
        folder_name = os.path.basename(dirpath) if relative_path == '.' else relative_path

        # Записываем информацию о папке
        f.write(f"【 Папка: {folder_name} 】\n")
        f.write("Содержимое:\n")

        # Перечисляем подпапки (уже отфильтрованные)
        for d in dirnames:
            f.write(f"    {d}/\n")

        # Перечисляем файлы (исключая скрытые и исключенные)
        visible_files = [fname for fname in filenames
                         if not is_hidden(os.path.join(dirpath, fname))
                         and fname not in excluded_files]

        for file in visible_files:
            f.write(f"    {file}\n")

        f.write("\n")

        # Обрабатываем содержимое файлов (только видимые и неисключенные)
        for filename in visible_files:
            file_path = os.path.join(dirpath, filename)
            relative_file_path = os.path.relpath(file_path, root_dir)

            f.write(f"Файл: {relative_file_path} \n")

            try:
                with open(file_path, 'r', encoding='utf-8') as fc:
                    content = fc.read()
                    f.write(f"Содержимое:\n{content}\n\n")
            except UnicodeDecodeError:
                f.write("Содержимое: [Бинарные данные]\n\n")
            except PermissionError:
                f.write("Содержимое: [Нет доступа]\n\n")
            except Exception as e:
                f.write(f"Ошибка чтения: {str(e)}\n\n")

    f.write("\n" + "=" * 40 + "\n")
    f.write("Сканирование завершено успешно!")