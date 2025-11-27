# Лабораторная работа 1 со звездочкой
Для попытки взлома был выбран сайт школы 207 https://207school.spb.ru/

## 1 Уязвимость: перебор страниц через ffuf

### Подготовка окружения

Лабораторная выполнена на виртуальной машине, на Ubuntu (64-bit)

Обновляем систему и устанавливаем инструмент ffuf для перебора веб-страниц
```
sudo apt update && sudo apt upgrade -y
sudo apt install ffuf -y
```

### Создание словарей для перебора

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
