📘 Документация: Запуск Python-приложения в Docker (Windows)

Этот проект использует Docker для запуска Python-приложения, которое работает с CSV-файлами и базой данных SQLite.
🔹 Установка Docker в Windows

    Скачайте и установите Docker Desktop с официального сайта:
    👉 https://www.docker.com/products/docker-desktop
    После установки перезагрузите компьютер.
    Убедитесь, что Docker работает (значок Docker в трее должен быть синим).

Проверить установку можно, открыв Командную строку (cmd) или PowerShell и введя:

docker --version
docker-compose --version

📂 Структура проекта

📦 project-root
├── 📂 input/             # Входные CSV-файлы
│   ├── input.csv         # Главный входной файл
├── 📂 db/                # База данных SQLite
│   ├── db.csv            # Исходный CSV-файл базы данных
│   ├── dataset.db        # База данных SQLite (создаётся автоматически)
├── 📂 log/               # Логи работы приложения
│   ├── logs.log          # Файл логов
├── 📂 scripts/           # Python-скрипты
│   ├── main.py           # Основной скрипт запуска
│   ├── init_db.py        # Инициализация базы данных
│   ├── utils.py          # Вспомогательные функции
├── .env                  # Файл с переменными окружения
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Инструкция по сборке контейнера
├── requirements.txt      # Список зависимостей Python

⚙️ Настройка переменных окружения

Перед запуском создайте (или отредактируйте) файл .env в корневой папке проекта. Пример содержимого:

INPUT_FILE_NAME=input.csv
OUTPUT_FILE_NAME=output.csv
DB_FILE_NAME=db.csv
SQLITE_DB=dataset.db
LOG_FILE=logs.log

🚀 Запуск проекта

Откройте Командную строку (cmd) или PowerShell в папке проекта (Shift + ПКМ → "Открыть окно команд").

1️⃣ Соберите Docker-образ:

docker-compose build

2️⃣ Запустите контейнер:

docker-compose up

При первом запуске скачиваются зависимости и создаются необходимые файлы.

3️⃣ Остановить контейнер:
Нажмите CTRL + C или выполните команду:

docker-compose down

📄 Просмотр логов

Логи записываются в файл log/logs.log. Чтобы посмотреть логи в реальном времени:

docker-compose logs -f

🛠 Полезные команды

✅ Проверить запущенные контейнеры:

docker ps

✅ Остановить и удалить все контейнеры:

docker-compose down --volumes

✅ Удалить неиспользуемые контейнеры и образы:

docker system prune -a
🎯 Файл docker-compose.yml

В разделе environment определяются переменные окружения, которые будут использоваться в контейнере Python. Эти переменные могут быть использованы для настройки работы приложения. В нашем случае определены следующие переменные:

    APPARTMENT_COLUMN_NAME=14 — имя колонки с номером квартиры в базе данных .
    ADDRESS_COLUMN_NAME=13 — имя колонки с адресом в базе данных.
    DB_NAME=db.csv — имя файла базы данных (move to db/ folder).
    INPUT_FILE_NAME=input.csv — имя входного CSV-файла (move to input/ folder).
    TABLE_NAME=table1 — имя таблицы в базе данных.