# file-storage

    ███████╗██╗██╗     ███████╗    ███████╗████████╗ ██████╗ ██████╗  █████╗  ██████╗ ███████╗
    ██╔════╝██║██║     ██╔════╝    ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝ ██╔════╝
    █████╗  ██║██║     █████╗      ███████╗   ██║   ██║   ██║██████╔╝███████║██║  ███╗█████╗  
    ██╔══╝  ██║██║     ██╔══╝      ╚════██║   ██║   ██║   ██║██╔══██╗██╔══██║██║   ██║██╔══╝  
    ██║     ██║███████╗███████╗    ███████║   ██║   ╚██████╔╝██║  ██║██║  ██║╚██████╔╝███████╗
    ╚═╝     ╚═╝╚══════╝╚══════╝    ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Development](#development)
    - [How to start a project](#how-to-start-a-project)
    - [Dependencies management](#dependencies-management)
    - [How to add new tables](#adding-new-tables)
    - [Linter](#linter)

## About
    Тестовое задание:

    Реализовать сервис, который предоставит HTTP API для загрузки (upload), скачивания (download) и удаления файлов.

    Upload:
        1. авторизованный пользователь загружает файл;
        2. файл сохраняется на диск в следующую структуру каталогов:
        
        store/ab/abcdef12345...
        
        где "abcdef12345..." - имя файла, совпадающее с его хэшем.
        
        /ab/ - подкаталог, состоящий из первых двух символов хэша файла.
        
        Алгоритм хэширования - на ваш выбор.
        
        3. возвращает хэш загруженного файла;
    Delete:
        авторизованный пользователь передает хэш файла, который необходимо удалить;
        если по хешу файл удалось найти в локальном хранилище, и `файл принадлежит пользователю`, то файл пользователя удаляется;
    - Download:
        1. любой пользователь передаёт параметр - хэш файла;
        2. если по хешу файл удалось найти в локальном хранилище, то возвращаем файл;

    Тип авторизации пользователей: Token.

    Регистрация пользователей в сервисе не предусмотрена.

## Getting Started
    
### Prerequisites

    - Python v3.12 (https://www.python.org/downloads/)
    - Any other specific software or libraries

### Installation

    1. Download and install python v3.12 (https://www.python.org/downloads/)
    2. Install pdm to your os (or use another dependencies manage tool)
        2.1. Install pdm:
            - (Invoke-WebRequest -Uri https://pdm-project.org/install-pdm.py -UseBasicParsing).Content | python -
            - pip install pdm
    3. Install requirements from lock.file (tested package version)
        pdm sync -v
    4. Active project venv
    5. You need to get .env config files for run project

## Development

### How to start a project:

    Back-end on local machine
        - Up db in docker
            docker-compose up
        - Up uvicorn server
            uvicorn app.main:app (use --reload if you coding now)
    Follow the link 'http://127.0.0.1:8000/docs'
        - To log in, click 'Authorize'
          
        Data for user_1: 
          login: user
          password: userPassword
        
        Data for user_2: 
          login: admin
          password: adminPassword
        
    

### Dependencies management:
    1. Adding new packages:
        pdm add <package_name>
    2. Updating all dependencies in the lock file, use (not recommended):
        pdm update
        Note: prefere use updating one package: pdm update <package_name>
    3. If you want to install newest package versions, use (from pyproject.toml):
        pdm install
    4. If you want to remove package, use:
        pdm remove <package_name>
    5. Show all installed packages, use:
        pdm list or pdm list --tree

### Adding new tables:

    1. Up db and apply migrations
    2. Create new table models
    3. Import models file into env.py.
        Path to env.py: app/db/migrations/env.py
        Add noqa ignore in import string for disable warning about unused imports
    4. Create new migration
        Use command 'alembic revision --autogenerate -m "Migration message"'
    5. Apply migration to db
        Use command 'alembic upgrade head' for applying migration
    6. Insert data into table
        Use command 'python .\sql\script_filling_data.py'

### Linter:

    1. To check your project for formatting errors in terminal enter "ruff check ."
    2. Instead of a dot, you can specify the path to the file
    3. To fix problems use the --fix option (the main command does not change)
    4. ATTENTION: locally modify the ruff.toml configuration file to ignore (only if you are sure) some types of errors or, conversely, enable new checks depending on your needs

