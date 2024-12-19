import os
import shutil
import socket

PORT = 9090
WORKING_DIRECTORY = "./server_files"


def process(request):
    try:
        command, *args = request.split()

        if command == "ls":
            return "; ".join(os.listdir(WORKING_DIRECTORY))

        elif command == "pwd":
            return os.path.abspath(WORKING_DIRECTORY)

        elif command == "mkdir":
            if not args:
                return "Ошибка: не указано имя папки."
            folder_name = os.path.join(WORKING_DIRECTORY, args[0])
            os.makedirs(folder_name, exist_ok=True)
            return f"Папка '{args[0]}' создана."

        elif command == "rmdir":
            if not args:
                return "Ошибка: не указано имя папки."
            folder_name = os.path.join(WORKING_DIRECTORY, args[0])
            if os.path.isdir(folder_name):
                shutil.rmtree(folder_name)
                return f"Папка '{args[0]}' удалена."
            return f"Папка '{args[0]}' не найдена."

        elif command == "rm":
            if not args:
                return "Ошибка: не указано имя файла."
            file_name = os.path.join(WORKING_DIRECTORY, args[0])
            if os.path.isfile(file_name):
                os.remove(file_name)
                return f"Файл '{args[0]}' удален."
            return f"Файл '{args[0]}' не найден."

        elif command == "rename":
            if len(args) < 2:
                return "Ошибка: требуется указать старое и новое имя."
            src = os.path.join(WORKING_DIRECTORY, args[0])
            dest = os.path.join(WORKING_DIRECTORY, args[1])
            if os.path.exists(src):
                os.rename(src, dest)
                return f"'{args[0]}' переименован в '{args[1]}'."
            return f"Файл или папка '{args[0]}' не найдены."

        elif command == "upload":
            if len(args) < 2:
                return "Ошибка: требуется указать имя файла и его содержимое."
            file_name = os.path.join(WORKING_DIRECTORY, args[0])
            with open(file_name, "w") as f:
                f.write(" ".join(args[1:]))
            return f"Файл '{args[0]}' создан с содержимым."

        elif command == "download":
            if not args:
                return "Ошибка: не указано имя файла."
            file_name = os.path.join(WORKING_DIRECTORY, args[0])
            if os.path.isfile(file_name):
                with open(file_name, "r") as f:
                    return f.read()
            return f"Файл '{args[0]}' не найден."

        elif command == "exit":
            return "Выход."

        else:
            return "Неправильная команда."

    except Exception as e:
        return f"Ошибка: {str(e)}"


def start_server():
    if not os.path.exists(WORKING_DIRECTORY):
        os.makedirs(WORKING_DIRECTORY)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на порту {PORT}. Ожидаем подключения...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Подключение от {addr}")
            request = conn.recv(1024).decode()
            print(f"Запрос: {request}")
            response = process(request)
            conn.send(response.encode())
            conn.close()
            if request.startswith("exit"):
                break
    except KeyboardInterrupt:
        print("\nСервер завершает работу...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
