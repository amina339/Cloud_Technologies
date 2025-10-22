## Дисклеймер 
Прочитав в интернете, для каких сервисов применяется докер-композ, мы поняли, что часто он нужен в таких системах, где есть несколько серверов, например, бэк, фронт, базы данных и т.д. 

Очень удачно на курсе программирования мы делали сайт, который:
- парсит habr.ru
- собранные данные хранит в базе данных
- позволяет на отдельной страницы разметить их
- используя написанный с нуля наивный байесовский классификатор, создает рекомендательную систему
  
Сайт немного сухой в плане передвижения (надо самим вписывать путь в ссылке) и дизайна, но для данной лабораторной работы - вполне достаточно.

Единственная вещь, которуя мы поменяли, была база данных. Изначально использовался SQLite и данные хранились в файле .bd, а мы для большей практики и хардкора захотели создавать базу PostgreSQL, поэтому просто пришлось добавить +1 бибилиотеку в requirements.txt и изменить ссылку, по которой создается engine.

#### Здесь также хочу отметить, что я писала композ для dev, а не prod, то есть по-хорошему важно было иметь возможность вносить изменения без ненужных rebuildов 

## Плохой docker-compose.yml
1. Укажем старую версию docker-compose.yml.
```
version: '1'
```
Почему это не очень хорошо? Потому что, начиная со 2 версии Docker-compose этот параметр указывать не нужно, то есть это лишняя строка, которая может потом вызвать конфликты, если в файле писать то, чего в данной версии еще не было
2. Дадим сервисам длинные нечитаемые названия, которые поймём только мы. Опять же другим разработчикам будет трудно понять, за что отвечает этот сервис, а также если еспользовать эти названия в других местах, это будет занимать больше времени и может возникнуть путаница.
```
services:
  a_very_long_and_cool_creation_of_the_best_data_base_in_the_world:
  this_is_the_part_when_we_are_initializing_and_filling_our_precious_database:
  this_thing_takes_data_from_habr_ru_and_shows_it_when_you_open_your_local_host:
```
### Часть a_very_long_and_cool_creation_of_the_best_data_base_in_the_world
1. Берем тяжелый и самый последний образ. По аналогии с докерфайлом - такая практика просто занимает лишнюю память и время при сборке
```
image: postgres:latest
```
2. Все пароли, ключи и т.п. поставим сразу в .yml, что небезопасно и неудобно при использовании их например продакшаном и разработкой (у них могут быть разные данные)
```
environment:
      POSTGRES_DB=newsdb
      POSTGRES_USER=admin
      POSTGRES_PASSWORD=secret123
      PYTHONPATH=/app
```
3. Порты напишем нормально 
```
ports:
      - "5432:5432"
```
4. Не будем встраивать том, то есть данные базы данных не будут храниться, что по очевидным причинам не есть хорошо
Для эксперимента решено было добавить искуственную задержку в инициализацию базы данных, чтобы потом показать пример еще одного bad practice (отсутствие depends_on)
### Часть this_is_the_part_when_we_are_initializing_and_filling_our_precious_database:
1. Из хорошего - инициализируем сборку образа из докерфайла и ставим команду запуска нужного файла (заполнение бд данными)
```
this_is_the_part_when_we_are_initializing_and_filling_our_precious_database:

    build: .   

    command: python bd_filling.py
```
2. Точно так же раскрываем все секреты
```
environment:
      DATABASE_URL=postgresql://admin:secret123@postgres-db:5432/newsdb
      PYTHONPATH=/app
```
3. Не прописываем working_dir, несмотря на то, что по докерфайлу все файлы скопировались в /app
4. Не прописываем порядок запуска контейнеров (нет depends_on), надеемся на удачу
5. Не встраиваем тома, которые будут содержать программный код. Для разработки это плохо тем, что при изменении кода каждый раз надо делать связку down + build + up
### Часть this_thing_takes_data_from_habr_ru_and_shows_it_when_you_open_your_local_host
Все так же как и в предыдущей части, но с другой командой и прописыванием портов
```
this_thing_takes_data_from_habr_ru_and_shows_it_when_you_open_your_local_host:

  build: .   

  command: python habrnews.py   
  environment:
    DATABASE_URL=postgresql://admin:secret123@postgres-db:5432/newsdb
    PYTHONPATH=/app

  ports:
    - "8000:8080"
```
В итоге получается такой файл
```
version: '1'
services:
  a_very_long_and_cool_creation_of_the_best_data_base_in_the_world:
    image: postgres:latest
    environment:
      POSTGRES_DB: newsdb
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
      PYTHONPATH: /app

    ports:
      - "5432:5432"

  this_is_the_part_when_we_are_initializing_and_filling_our_precious_database:

    build: .   

    command: python bd_filling.py
    environment:
      DATABASE_URL: postgresql://admin:secret123@postgres-db:5432/newsdb
      PYTHONPATH: /app      

  this_thing_takes_data_from_habr_ru_and_shows_it_when_you_open_your_local_host:

    build: .   

    command: python habrnews.py   
    environment:
      DATABASE_URL: postgresql://admin:secret123@postgres-db:5432/newsdb
      PYTHONPATH: /app

    ports:
      - "8000:8080" 
```
Также в данном случае мы не писали .dockerignore и копируем все возможные файлы в образ
## Работа плохого композа
Во-первых вышло предупреждение 
```
the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion
```
В глаза сразу бросаются наши длинные названия, которые делают чтение логов почти невозможными. Даже нам нужно несколько раз перечитать только лишь названия, чтобы понять, что происходит, хотя, казалось бы, ямы сами придумали названия

<img width="1492" height="66" alt="Снимок экрана 2025-10-20 151401" src="https://github.com/user-attachments/assets/64c13850-df53-4e05-b01e-796158acbf00" />

Далее на этой же фотографии видно, что файлы найдены не были, так как мы не прописали рабочие директории, ну и следовательно остальные наши bad practices особо проверить тоже не получится
Исправим это, чтобы хотя бы минимально посмотреть на работу композа. Пропишем пути (листинг кода в такие моменты будет в части хорошего композ-файла) и опять все запустим

<img width="1525" height="223" alt="Снимок экрана 2025-10-20 152955" src="https://github.com/user-attachments/assets/defad2fc-11a0-4d72-92c9-1d48ef4887dc" />

Так как мы не указали порядок поднятия сервисов, то вначале запустился сам сайт, а потом заполнение бд, но тут и возникли проблемы, так как мы даже еще не создали бд, а также название было слишком длинным и 'could not translate host name'. В конце концов логи перестали появляться и все застыло, потому что дальнейших инструкций не было прописано
Исправим и это, пропишем все порядки в виде depends_on, исправим имя, а чтобы избежать проблемы на картинке ниже 

<img width="1529" height="66" alt="Снимок экрана 2025-10-20 160024" src="https://github.com/user-attachments/assets/fd7b0ac7-dd55-4a5d-ab8f-5d0ca3163208" />

Пропишем еще и 
```
condition: service_healthy
```
то есть, что мы запускаем следующий контейнер, когда подключимся к бд
и 
```
healthcheck: 
      test: ["CMD-SHELL", "pg_isready -U admin -d newsdb"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 10s
```
чтобы все ждали создания бд максимум 5 раз, а не просто запуска контейнера 

также я заодно решила сразу написать и для части сайта такие состояния (проверка того, что таблица в бд имеет хотя бы 1 строку)
```
condition: service_completed_successfully
```
```
command: >
      sh -c "
          python bd_filling.py
          
          if psql -h postgres-db -U admin -d newsdb -c 'SELECT COUNT(*) FROM news' | grep -q '0'; then
            exit 1
          else
            exit 0
          fi
        "
```

И все сработало 

<img width="673" height="120" alt="Снимок экрана 2025-10-20 160847" src="https://github.com/user-attachments/assets/eafe75d8-101e-470c-bfaa-e93bef511159" />

Теперь посмотрим, сможем ли мы как разработчики менять какие-то фичи без новых rebuildов. Например, захотелось поменять главную страницу на страницу рекомендаций 
```
@route('/')
def index():
    redirect("/news_recommedations")
```
```
docker-compose -f docker-compose-bad.yml restart
```
<img width="673" height="120" alt="Снимок экрана 2025-10-20 160847" src="https://github.com/user-attachments/assets/d34bca74-e252-4128-afb4-0a93d5ef344f" />

Главная страница осталась прежней(

Еще отметим, что после связки down + build + up, данные не сохранялись (очевидно из-за отсутствия соотвествующего тома) и приходилось по новой размечать данные
## Хороший docker-compose.yml
1. Мы в целом не указываем version, потому что, начиная с какой-то версии, это делать не нужно и все и так работает
2. Ставим нормальные и понятные названия сервисов, в моем случае
```
services:
  postgres-db: #база данных
  ...
  database-init: #заполнение базы данных
  ...
  web-app: #бэк и фронт сайта 
  ...
```
### Основные изменения части postgres-db
- Берем образ полегче
- Встраиваем том, чтобы данные где-то хранились (named volume) даже после docker-compose down
- Важные данные конфингурации БД и пути пишем в переменные окружения и создаем файл .env, в котором они хранятся (удобнее для безопасности (если вдруг пойдет в прод) и для внесения изменений, то есть не надо переписывать docker-compose.yaml)
- Остальное было уже сделано в части плохого файла
```
postgres-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PYTHONPATH: ${PYTHONPATH}
    healthcheck: 
        test: ["CMD-SHELL", "pg_isready -U admin -d newsdb"]
        interval: 5s
        timeout: 5s
        retries: 5
        start_period: 10s

    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data 
```
### Основные изменения части database-init
- Определяю зависимость между серверами, чтобы все запускалось в правильном порядке
- Встраиваю тома: один для общих модулей, другой - для самой директории, чтобы при изменении кода не пересобирать все, а просто, собственно, добавить изменение и сделать рестарт
- То же самое про переменные окружения 
```
database-init:
    depends_on:
      postgres-db:
        condition: service_healthy

    build: .   

    command: >
      sh -c "
          python bd_filling.py
          
          if psql -h postgres-db -U admin -d newsdb -c 'SELECT COUNT(*) FROM news' | grep -q '0'; then
            exit 1
          else
            exit 0
          fi
        "
    working_dir: /app/database
    environment:
      DATABASE_URL: ${DATABASE_URL}
      PGPASSWORD:: ${POSTGRES_PASSWORD}
      PYTHONPATH: ${PYTHONPATH}       

    volumes:
      - ./shared:/app/shared
      - ./database:/app/database
```
### Основные изменения части web-app
Тут все так же как и в части database-init, но:
- волюм сделан для нужной директории
- зависимости от серверов 2 штуки
- порты прописаны корректно (локальный порт перебрасывается на порт в контейнере)
```
    depends_on:
          postgres-db:
            condition: service_healthy
          database-init:
            condition: service_completed_successfull

    build: .   

    command: python habrnews.py         
    working_dir: /app/backend 
    environment:
      DATABASE_URL: ${DATABASE_URL} 
      PYTHONPATH: ${PYTHONPATH} 

    ports:
      - "8000:8080" 
    volumes:
      - ./shared:/app/shared  
      - ./backend:/app/backend
```

Ну и в конце, так как у нас Named volume, мы его объявляем

```
volumes:
  postgres_data:
```
## Работа хорошего композа

Запустим все 
```
docker-compose up
```

Это некоторые логи из кода, которые говорят, что страницы парсятся (логи загрузки именно образа и сборки всей системы слишком большой)

<img width="910" height="352" alt="Снимок экрана 2025-10-17 211626" src="https://github.com/user-attachments/assets/c9c554df-84ea-4a23-9efc-d540b1a2daeb" />

После всех загрузок мы видим это

<img width="937" height="102" alt="Снимок экрана 2025-10-17 211740" src="https://github.com/user-attachments/assets/5d12e3ac-fb14-4ba1-bd37-939c53430e41" />

Зашли на сайт и потыкали что-то (по факту, разметили данные и дали Байесу на кушанье)

<img width="1759" height="959" alt="Снимок экрана 2025-10-17 203547" src="https://github.com/user-attachments/assets/a571a309-66ff-44f2-8b86-bf24cb7953dd" />
  
Зашли на рекомендации, которые подобрал Байес

<img width="1740" height="967" alt="Снимок экрана 2025-10-17 203642" src="https://github.com/user-attachments/assets/770b22f6-b7ec-40c4-96cd-7e658815739b" />

А это кусок логов, когда размечали данные

<img width="974" height="87" alt="Снимок экрана 2025-10-17 211752" src="https://github.com/user-attachments/assets/a56e009f-3887-4d16-a6ec-4cec7f62b02c" />

Теперь мне захотелось изменить часть кода, чтобы начальная страница была не с разметкой данных, а с рекомендациями. Изначально она стоит на разметке, т.к. без этого этапа не будет рекомендаций :/

<img width="566" height="104" alt="Снимок экрана 2025-10-17 212148" src="https://github.com/user-attachments/assets/70d2fabc-c286-413d-b17c-a834d9521680" />

Так что я просто меняю эту строку в коде без остановки композа, а потом, сохранив изменения, пишу
```
docker-compose restart web-app
```

<img width="692" height="48" alt="Снимок экрана 2025-10-17 212719" src="https://github.com/user-attachments/assets/2add3b2b-203b-4560-85bf-464385722d06" />

И вот я снова зашла на сайт, где меня приветствует уже страница рекомендаций 

<img width="1716" height="294" alt="Снимок экрана 2025-10-17 212727" src="https://github.com/user-attachments/assets/ad926f8f-47aa-482e-922b-7042eeabfb45" />

А тут еще я захотела посмотреть на табличку в БД

<img width="1898" height="497" alt="Снимок экрана 2025-10-17 204152" src="https://github.com/user-attachments/assets/5e25bcc4-1ac4-4163-83e2-64820b46e617" />

В какой-то момент была написана связка down + build + up и было видно, что данные остались 
```
PostgreSQL Database directory appears to contain a database; Skipping initialization
```
Это очень удобно в плане разработки, так как в нашем контексте не нужно каждый раз заново размечать данные для работы рекомендательной системы
Ну и напоследок:
- был написан .dockerignore
- в dockerfile отсуствует строка
```
COPY . .
```
так как мы все равно встраиваем тома с данными файлами 
в плохом докер-композе эта строка была вписана в докерфайл


