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

### 1) Создание структуры

Создаем корневые папки для проектов:
```
sudo mkdir -p /var/www/project_a
sudo mkdir -p /var/www/project_b
```
Создает html-файлы (сейчас простые, наполним их чуть-чуть попозже):
<b>Для проекта a:</b>
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
<b>Для проекта b:</b>
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
