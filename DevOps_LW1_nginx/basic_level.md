# Лабораторная работа 1

Для того чтобы упростить себе жизнь, лабораторная выполнялась на виртуалке, конкретно использована Ubuntu (64-bit).

## 1 шаг. Подготовка к работе

### 1) Установка пакетов

```sudo apt update``` - устанавливаем список пакетов.

```sudo apt install nginx -y``` - устанавливаем nginx.

```sudo systemctl start nginx```, ```sudo systemctl enable nginx``` - запускаем nginx.

```sudo systemctl status nginx``` - проверяем статус.

Результат:
<img width="1204" height="556" alt="image" src="https://github.com/user-attachments/assets/fd572f3b-1edc-42d5-ab16-655f07afe7db" />
У нас все active, супер.

### 2) Создание структуры

Создаем корневые папки для проектов:
```
sudo mkdir -p /var/www/project_a
sudo mkdir -p /var/www/project_b
```
Создает html-файлы (сейчас простые, наполним их чуть-чуть попозже):
<b>Для проекта A:</b>
```
sudo nano /var/www/project_a/index.html
```
В него пишем следующий код:
```
<!DOCTYPE html>
<html>
<head>
    <title>Project A</title>
</head>
<body>
    <h1>Hello Project A!</h1>
    <p>This is our first pet project on Ubuntu.</p>
</body>
</html>
```
<b>Для проекта B:</b>
```
sudo nano /var/www/project_b/index.html
```
В него пишем следующий код:
```
<!DOCTYPE html>
<html>
<head>
    <title>Project B</title>
</head>
<body>
    <h1>Hello Project B!</h1>
    <p>This is our second pet project on Ubuntu.</p>
</body>
</html>
```
Теперь надо дать правильные права на эти папки:
```
sudo chown -R www-data:www-data /var/www/project_a
sudo chown -R www-data:www-data /var/www/project_b
sudo chmod -R 755 /var/www/
```

## 2 шаг. Настройка виртуальных хостов
<b>Создаем конфиг для Project A:</b>
```
sudo nano /etc/nginx/sites-available/project_a
```
В него пишем следующий код:
```
server {
    listen 80;
    server_name project-a.local;

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

<b>Создаем конфиг для Project B:</b>
```
sudo nano /etc/nginx/sites-available/project_b
```
В него пишем следующий код:
```
server {
    listen 80;
    server_name project-b.local;

    root /var/www/project_b;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Теперь активируем сайты:
```
sudo ln -s /etc/nginx/sites-available/project_a /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/project_b /etc/nginx/sites-enabled/
```
Проверяем конфигурацию на ошибки:
```
sudo nginx -t
```
И перезагружаем nginx:
```
sudo systemctl reload nginx
```
<img width="1010" height="156" alt="image" src="https://github.com/user-attachments/assets/efa7f62b-2383-4f2b-9dae-7904a1f16ad7" />
На скрине видно что при проверке syntax is ok и test is successful, ура.

## 3 шаг. Настройка локальных доменов
Откроем файл hosts:
```
sudo nano /etc/hosts
```
Добавим в конец файла две строки:
```
127.0.0.1 project-a.local
127.0.0.1 project-b.local
```
Пингуем наши домены:
```
ping -c 2 project-a.local
ping -c 2 project-b.local
```
Результат:
<img width="708" height="210" alt="image" src="https://github.com/user-attachments/assets/7d30966a-f65a-4fa8-8898-90db9e1a781d" />
Нам отвечают, радуемся.

## 4 шаг. Создание SSL-сертификатов
Создадим самоподписанные SSL-сертификаты для обоих проектов.

Создаем папку для сертификатов:
```
sudo mkdir -p /etc/nginx/ssl
```
Генерируем SSL-сертификат для Project A:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/project-a.key \
    -out /etc/nginx/ssl/project-a.crt \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=IT/CN=project-a.local"
```
Генерируем SSL-сертификат для Project B:
```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/project-b.key \
    -out /etc/nginx/ssl/project-b.crt \
    -subj "/C=RU/ST=Moscow/L=Moscow/O=IT/CN=project-b.local"
```
Проверяем, что сертификаты созданы:
```
sudo ls -la /etc/nginx/ssl/
```
Результат:
<img width="1214" height="712" alt="image" src="https://github.com/user-attachments/assets/3591c134-682e-45ac-9e4f-620c3455a138" />
Мы увидели все файлы которые создали, супер, идем дальше.

## 5 шаг. Настройка HTTPS
### 1) Обновим конфиг для Project A с поддержкой HTTPS:
```sudo nano /etc/nginx/sites-available/project_a``` - открываем
И меняем содержимое на:
```
server {
    listen 80;
    listen 443 ssl;
    server_name project-a.local;

    # SSL сертификаты
    ssl_certificate /etc/nginx/ssl/project-a.crt;
    ssl_certificate_key /etc/nginx/ssl/project-a.key;

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```
### 2) Обновим конфиг для Project B с поддержкой HTTPS:
```sudo nano /etc/nginx/sites-available/project_b``` - открываем
И меняем содержимое на:
```
server {
    listen 80;
    listen 443 ssl;
    server_name project-b.local;

    # SSL сертификаты
    ssl_certificate /etc/nginx/ssl/project-b.crt;
    ssl_certificate_key /etc/nginx/ssl/project-b.key;

    root /var/www/project_b;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```
```sudo nginx -t``` - проверяем конфигурацию

```sudo systemctl reload nginx``` - перезагружаем nginx

Результат:
<img width="700" height="114" alt="image" src="https://github.com/user-attachments/assets/a3835c9a-4b34-4581-b79c-97842484050c" />
Все опять хорошо.

Теперь проверим как работают наши сертификаты и настроен ли https.

Откроем в браузере наши проекты:
```
https://project-a.local
https://project-b.local
```
<b>Project A:</b>
<img width="900" height="502" alt="image" src="https://github.com/user-attachments/assets/ac8ec77f-eafd-43fe-b710-2694ff5c9e7f" />
<img width="436" height="232" alt="image" src="https://github.com/user-attachments/assets/02fa3156-cb75-43f6-a621-00f4d5a924d1" />

<b>Project B:</b>
<img width="870" height="506" alt="image" src="https://github.com/user-attachments/assets/475669b4-2609-4664-af2d-7617bb1460d1" />
<img width="450" height="218" alt="image" src="https://github.com/user-attachments/assets/7a37939c-fa1b-44f4-8943-17382524594e" />

Красота, все нормально, проект открывается, https работает, а браузер браузер предупреждает о самоподписанном сертификате.

## 6 шаг. Настройка принудительного редиректа с HTTP на HTTPS

