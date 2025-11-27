# Лабораторная работа 1 со звездочкой
Для попытки взлома был выбран сайт школы 207 https://207school.spb.ru/

## Подготовка окружения

Лабораторная выполнена на виртуальной машине, на Ubuntu (64-bit)

Обновляем систему и устанавливаем инструмент ffuf для перебора веб-страниц
```
sudo apt update && sudo apt upgrade -y
sudo apt install ffuf curl wget -y
```

Проверим доступность сайта:

```curl -I http://207school.spb.ru```

<img width="1080" height="402" alt="image" src="https://github.com/user-attachments/assets/0f504bc8-e7b1-43af-baf2-6286622b67bb" />

## Проверка уязвимости Path Traversal

Сначала попробуем получить доступ к системным файлам

### Базовый path traversal:

```
curl "http://school207.ru/../../../etc/passwd"
curl "http://school207.ru/../../../../etc/passwd"
```
<img width="1212" height="688" alt="image" src="https://github.com/user-attachments/assets/ac8b5a64-06b7-4b63-82eb-af8c62f448f9" />

<img width="1220" height="662" alt="image" src="https://github.com/user-attachments/assets/133b52d3-3d78-436c-ace7-ec7b3ad4694b" />

### URL encoding:

```
curl "http://school207.ru/..%2f..%2f..%2fetc%2fpasswd"
curl "http://school207.ru/%2e%2e/%2e%2e/etc/passwd"
```
<img width="878" height="222" alt="image" src="https://github.com/user-attachments/assets/11f6f2d4-cf12-4b35-9991-bf6b4699e754" />

<img width="888" height="182" alt="image" src="https://github.com/user-attachments/assets/86bbc572-5b54-41d0-a0d5-9f6284215990" />

### Через параметры:

```
curl "http://school207.ru/?file=../../../etc/passwd"
curl "http://school207.ru/download?file=../../etc/passwd"
```
<img width="1216" height="684" alt="image" src="https://github.com/user-attachments/assets/1cb04706-b512-4b0e-9664-da3584758129" />
<img width="1204" height="712" alt="image" src="https://github.com/user-attachments/assets/618b0a9a-3e91-4aa0-9113-fef6833d8784" />

### Проверка конфигурационных файлов nginx:

```
curl "http://school207.ru/../nginx.conf"
curl "http://school207.ru/../../nginx/nginx.conf"
```

<img width="1212" height="710" alt="image" src="https://github.com/user-attachments/assets/271e0c6f-59a1-4c65-92c0-b9cf67ed3fb7" />
<img width="1204" height="632" alt="image" src="https://github.com/user-attachments/assets/93d662f6-5b99-4b91-9b96-c91ab01d5a3d" />

### Оценка результатов:

1. Все способы кроме URL-encoding возвращают главную страницу сайта, что значит что Nginx нормализует путь и игнорирует ../. Вместо попытки выйти из корневой директории, он просто показывает главную страницу (/). Это нормальное поведение правильно настроенного nginx.
  
2. URL-encoding возвращает 400 Bad Request, что значит что Nginx распознал это как попытку path traversal и заблокировал запрос. Код 400 означает "неверный запрос", то есть защите работает.


Тем не менее попытаемся найти еще что-нибудь.

## Проверка уязвимости перебора страниц через ffuf


```sudo apt install git -y``` - установим гит

```git clone https://github.com/danielmiessler/SecLists.git``` - скачаем популярную коллекцию вордлистов

Посмотрим что скачалось:

```
cd SecLists/Discovery/Web-Content/
ls -la
```
















```mkdir -p ~/lab/wordlists``` - создаем папку для словарей

```nano ~/lab/wordlists/dirs.txt``` - создаем словарь директорий

Пишем в файл набор самых частых директорий, которые встречаются на веб-серверах:

<img width="156" height="386" alt="image" src="https://github.com/user-attachments/assets/422de837-e3e0-4780-bd4b-880c99f2ef16" />

```nano ~/lab/wordlists/files.txt``` - создаем словарь файлов:

Записываем туда файлы, которые считаются типичными "скрытыми" находками на серверах:

<img width="164" height="292" alt="image" src="https://github.com/user-attachments/assets/9e236371-7d38-43e1-ba02-43ce79b7158a" />

```nano ~/lab/wordlists/extensions.txt``` - создаем словарь расширений

Записываем туда минимальный набор расширений:

<img width="102" height="172" alt="image" src="https://github.com/user-attachments/assets/27d97ca1-9bc2-4bf9-9b97-92c72b33af6e" />

### Перебор директорий и файлов

```ffuf -w ~/lab/wordlists/dirs.txt -u http://207school.spb.ru/FUZZ -mc all``` 

Параметры:
```-w``` - wordlist
```-u``` - URL, FUZZ - переменная
```-mc all``` - вывод всех кодов ответов

Результат:
<img width="1220" height="710" alt="image" src="https://github.com/user-attachments/assets/1e839725-2790-417c-b0c5-304ca9b7c1b5" />

При переборе директорий /tmp/ вернула код 301, что означает существование каталога и перенаправление на корректный URL. Это подтверждает, что ресурс существует, т.е. скрытый путь успешно обнаружен. Все остальные дериктории вернули код 404 что означает отсутствие данных директорий на сервере, либо вероятнее сокрытие путей.
