#### Подключиться к серверу 
    ssh -i path_to_public_key server_user@server_ip

#### Создать пользователя 
    *username - имя будущего пользователя сервером
    
    adduser username
    usermod -aG sudo username
    
#### Перейти на новосозданного пользователя
    su - username
        
#### Обновить пакеты системы, и если нет python, установить, установить другие пакеты
 
    sudo add-apt-repository ppa:deadsnakes/ppa
    
    sudo echo 'deb http://www.rabbitmq.com/debian testing main' \
    | sudo tee /etc/apt/sources.list.d/rabbitmq.list
    wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
    sudo apt update
    
    sudo apt install rabbitmq-server
    sudo systemctl enable rabbitmq-server
    sudo systemctl start rabbitmq-server
    
    sudo apt install python3.number_version 
    sudo apt install postgresql postgresql-contrib
    sudo apt install git
    sudo apt install nginx
 
#### Установить модуль python -  virtualenv
 
    python3 -m pip install virtualenv
 
#### Cоздать папку , в которой будет содержимое сайта 
    mkdir -p ~/sites/news_board
#### Kлонировать репозиторий с содержимым сайта, в новосозданную папку
    cd ~/sites/news_board
    git https://github.com/M0rqpEy/news_board.git .
#### Создать виртуальное окружение, и зайти в него
    python3 -m virtualenv venv
    source venv/bin/activate
   
#### Cобрать статику
    python manage.py collectstatic
#### Создать базу данных, пользователя postgresql
    sudo -u postgres psql
    
    CREATE DATABASE news_board;
    CREATE ROLE news_board WITH PASSWORD 'news_board';
    ALTER ROLE news_board CREATEDB;
    ALTER ROLE news_board SET client_encoding to 'utf8';
    ALTER ROLE news_board SET default_transaction_isolation to 'read committed';
    ALTER ROLE news_board SET timezone to 'UTC+3';
    GRANT ALL PRIVILEGES ON DATABASE news_board to news_board;

#### Создать миграции
    при активируваном вируальном окружении 
    python manage.py makemigrations
    python manage.py migrate

#### Переключить DEBUG = False, и добавить доменное имя в ALLOWED_HOSTS

#### Создать файл с настройками сайта для nginx, по такому адресу
    /etc/nginx/sites-available/news_board
    
    c таким содержимым
    
    server {
        listen 80;
        server_name ВАШЕ_ДОМЕННОЕ_ИМЯ_ИЛИ_АПИ_АДРЕС_СЕРВЕРА;

        location /static {
                alias /home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/sites/news_board/staticfiles;
        }
        location / {
                proxy_set_header Host $host;
                proxy_pass http://unix:/tmp/news_board.socket;
        }
    }
    
#### Создать символьную ссылку
    sudo ln -s /etc/nginx/sites-available/news_board \
    /etc/nginx/sites-enabled/news_board
#### Cоздать файл с автоматической загрузкой гуникорна,
#### по такому адресу
    /etc/systemd/system/gunicorn-news_board.service
    
    c таким содержимым
    
    [Unit]
    Description=Gunicorn server for news_board

    [Service]
    Restart=on-failre
    User=ubuntu
    WorkingDirectory=/home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/sites/news_board
    ExecStart=/home/ИМЯ_ПОЛЬЗОВАТЕЛЯ/sites/news_board/venv/bin/gunicorn \
    --bind unix:/tmp/news_board.socket \
    config.wsgi:application

    [Install]
    WantedBy=multi-user.target
   
#### Запуск новосозданной службы
    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn-news_board.service
    sudo systemctl start gunicorn-news_board.service
 
#### Запуск селери
celery -A config worker -B



#### Postman collection
https://www.getpostman.com/collections/07488e4fec4018436fb6


#### Задеплоено туть!
    http://3.134.100.95:9999/api/v0/posts/