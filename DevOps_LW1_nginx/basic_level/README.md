# Лабораторная работа 1

Для того чтобы упростить себе жизнь, лабораторная выполнялась на виртуалке, конкретно использована Ubuntu (64-bit).
<div align="center">
    <img width="735" height="706" alt="image" src="https://github.com/user-attachments/assets/91bfd1bd-fcaa-49ad-866c-899788d0c410" />
</div>

## 1 шаг. Подготовка к работе

### 1) Установка пакетов

```sudo apt update``` - устанавливаем список пакетов.

```sudo apt install nginx -y``` - устанавливаем nginx.

```sudo systemctl start nginx```, ```sudo systemctl enable nginx``` - запускаем nginx и включаем автозапуск nginx при загрузке системы.

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
С такими правами владелец может читать/писать/выполнять, остальные - только читать/выполнять, это важно для безопасности веб-сервера.

## 2 шаг. Настройка виртуальных хостов
<b>Создаем конфиг для Project A:</b>
```
sudo nano /etc/nginx/sites-available/project_a
```
В него пишем следующий код:
```
server {
    listen 80;  #сервер будет слушать HTTP-запросы на порту 80
    server_name project-a.local;  #nginx будет использовать эту конфигурацию для запросов к указанному домену

    root /var/www/project_a;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;    #директива пытается найти запрашиваемый файл, если не находит - возвращает 404
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
Мы создаем символическую ссылку для активации сайта. Это позволит нам включать/выключать сайты без удаления конфигов.

Проверяем конфигурацию на ошибки (тестируем синтаксис):
```
sudo nginx -t
```
И перезагружаем nginx (сервер при такой перезагрузке не останавливается):
```
sudo systemctl reload nginx
```
<img width="1010" height="156" alt="image" src="https://github.com/user-attachments/assets/efa7f62b-2383-4f2b-9dae-7904a1f16ad7" />
На скрине видно что при проверке syntax is ok и test is successful, ура.

## 3 шаг. Настройка локальных доменов
Откроем файл hosts (он преобразует доменные имена в IP-адреса в обход DNS-серверов):
```
sudo nano /etc/hosts
```
Добавим в конец файла две строки, которые буду указывать, что домены должны вести на локальную машину:
```
127.0.0.1 project-a.local
127.0.0.1 project-b.local
```
Пингуем наши домены (отправляем 2 ICMP-пакета для проверки доступности хоста):
```
ping -c 2 project-a.local
ping -c 2 project-b.local
```
Результат:

<img width="708" height="210" alt="image" src="https://github.com/user-attachments/assets/7d30966a-f65a-4fa8-8898-90db9e1a781d" />

Нам отвечают, радуемся. Ну а вообще, результат показывает, что домен корректно преобразуется в IP-адрес 127.0.0.1, и пакеты успешно доходят до цели.

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
<b>Для понимания:</b>

```-x509``` - создание самоподписанного сертификата

```-nodes``` - сертификат без пароля (для автоматической загрузки)

```-days 365``` - срок действия сертификата (1 год)

```-newkey rsa:2048``` - генерация RSA-ключа длиной 2048 бит

```-subj``` - указание данных сертификата (страна, город, организация, домен)

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
    listen 443 ssl;   #добавление поддержки HTTPS на порту 443
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

Красота, все нормально, проект открывается, https работает, а браузер предупреждает о самоподписанном сертификате.

## 6 шаг. Настройка принудительного редиректа с HTTP на HTTPS
### 1) Опять изменим конфиг для Project A:
```sudo nano /etc/nginx/sites-available/project_a``` - открываем

И заменяем содержимое на:
```
# редирект с HTTP на HTTPS
server {
    listen 80;
    server_name project-a.local;
    return 301 https://$server_name$request_uri;
}

# основной сервер HTTPS
server {
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
<b>Немного подробнее про редирект:</b>

```listen 80``` - прослушивание HTTP-запросов на порту 80

```return 301 https://$server_name$request_uri;``` - перенаправление 301 (постоянное):

```301``` - код постоянного перемещения, сообщает браузерам и поисковым системам, что страница перемещена
    
```https://$server_name``` - подстановка доменного имени (project-a.local)
    
```$request_uri``` - сохранение полного пути запроса (например, /index.html)
    
### 2) Опять изменим конфиг для Project B:
```sudo nano /etc/nginx/sites-available/project_b``` - октрываем

И заменяем содержимое на:
```
# редирект с HTTP на HTTPS
server {
    listen 80;
    server_name project-b.local;
    return 301 https://$server_name$request_uri;
}

# основной сервер HTTPS
server {
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

<img width="676" height="92" alt="image" src="https://github.com/user-attachments/assets/479bfc54-1ec0-4ce4-8195-d9639de3b733" />

Все ок.

Теперь надо проверить, работает ли наш редирект, или мы его по фану создали.

Откроем в браузере наши проекты <b>(http без s!!!)</b>:
```
http://project-a.local
http://project-b.local
```
<b>Project A:</b>

<img width="446" height="212" alt="image" src="https://github.com/user-attachments/assets/426682a5-a9b0-40d7-84b8-45cfff73cc02" />

<b>Project B:</b>

<img width="490" height="220" alt="image" src="https://github.com/user-attachments/assets/33439e91-5cce-451b-9fc9-370af045d47e" />

Ура! Редирект работает.

## 7 шаг. Перед тем, как настроить alias, добавим немного текста и картинок в наши проекты, и как нибудь их назовем

### 1) Настроим Project A:

<b>Первый проект - сорта гранатов и краткое их описание с картинками</b>

Изменим доменное имя на pomegranate.

```sudo nano /etc/nginx/sites-available/project_a``` - открываем конфиг

```server_name pomegranate.local;``` - заменяем строчку с server_name

```sudo nano /etc/hosts``` - открываем hosts

```127.0.0.1 pomegranate.local``` - меняем строчку где был project-a

Создадим папку для картинок в Project A
```
sudo mkdir -p /var/www/project_a/static/images
sudo chown -R www-data:www-data /var/www/project_a/static
```
За кадром скачаем и поместим туда фото разных сортов граната.

```sudo nano /var/www/project_a/index.html``` - открываем файл проекта

Полный код файла можно посмотреть [здесь](project_a.html), однако там будет финальная версия и будет использован alias, а сейчас для вставки картинок используется полный путь и код выглядит, на примере первой картинки, вот так:

```
<img src="/static/images/peru.jpg" alt="Pomegranate of Peru">
```
### 2) Настроим Project B:

<b>Второй проект - сорта помело и краткое их описание с картинками</b>

Изменим доменное имя на pomelo.

```sudo nano /etc/nginx/sites-available/project_b``` - открываем конфиг

```server_name pomelo.local;``` - заменяем строчку с server_name

```sudo nano /etc/hosts``` - открываем hosts

```127.0.0.1 pomelo.local``` - меняем строчку где был project-b

Создадим папку для картинок в Project B
```
sudo mkdir -p /var/www/project_b/static/images
sudo chown -R www-data:www-data /var/www/project_b/static
```
За кадром скачаем и поместим туда фото разных сортов помело.

```sudo nano /var/www/project_b/index.html``` - открываем файл проекта

Полный код файла можно посмотреть [здесь](project_b.html), однако там будет финальная версия и будет использован alias, а сейчас для вставки картинок используется полный путь и код выглядит, на примере первой картинки, вот так:
```
<img src="/static/images/sweety.jpg" alt="Pomelo Sweetie">
```
## 8 шаг. Настройка alias

Вообще, Alias (псевдоним) - это механизм nginx для создания виртуальных путей, которые указывают на реальные директории на сервере. Он позволяет создавать короткие и понятные URL вместо длинных реальных путей.

### 1)Для Project A:

```sudo nano /etc/nginx/sites-available/project_a``` - открываем конфиг

Добавляем alias для картинок - псевдоним пути
```
location /pics_a/ {
        alias /var/www/project_a/static/images/;
    }
```

### 2)Для Project B:

```sudo nano /etc/nginx/sites-available/project_b``` - открываем конфиг

Добавляем alias для картинок - псевдоним пути
```
location /pics_b/ {
        alias /var/www/project_b/static/images/;
    }
```

```sudo nginx -t ``` - проверяем конфигурацию

```sudo systemctl reload nginx``` - перезагружаем nginx

Результат:

<img width="690" height="122" alt="image" src="https://github.com/user-attachments/assets/67aca661-eafc-4d14-a5c1-d9ee5421c570" />

Все нормик, дальше идем.

Теперь в html-файле для проектов A и B заменяем пути к картинкам, которые у нас были на новые, используя псевдонимы:

<b>Например:</b>

```<img src="/static/images/peru.jpg" alt="Pomegranate of Peru">``` <b>меняем на</b> ```<img src="/pics_a/peru.jpg" alt="Pomegranate of Peru">```

## 9 Шаг. Теперь посмотрим на наши готовенькие проекты:
### Project A:
<img width="1220" height="724" alt="image" src="https://github.com/user-attachments/assets/50d744da-2280-4d37-923e-0317fb494ba8" />
<img width="1200" height="730" alt="image" src="https://github.com/user-attachments/assets/13a7dc36-9ef7-4876-a3bb-22dda5a9823a" />
<img width="1212" height="732" alt="image" src="https://github.com/user-attachments/assets/f586c2b8-8f98-450c-9a90-8f8fbba87413" />

### Poject B:
<img width="1216" height="730" alt="image" src="https://github.com/user-attachments/assets/4e7598c7-2614-4a93-a9c5-2d35f369ea24" />
<img width="1196" height="730" alt="image" src="https://github.com/user-attachments/assets/0e007aac-dff1-4462-a73f-53b3b3b1e800" />
<img width="1218" height="726" alt="image" src="https://github.com/user-attachments/assets/694283af-0284-4df6-a0ff-5d7be63d5242" />

## На этом все!
<div align="center">
    <img width="685" height="500" alt="image" src="https://github.com/user-attachments/assets/d7c6ef91-5f5b-43bd-a37c-bcac1778a0d1" />
</div>
