# Бот-магазин для продажи в Telegram

Telegram-бот для продажи рыбы.

Все данные хранятся в сервисе CMS Strapi

Бот сохраняет в Redis текущее состояние каждого пользователя в целях анализа воронки продаж.

<img src="screenshots/1.gif" height="400">


### Как установить

Python 3.12 или новее должен быть уже установлен. Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:

```sh
pip install -r requirements.txt
```

Для работы бота нужен запущенный [Strapi](https://strapi.io/) версии 5. Его адрес указывается в переменной `STRAPI_URL`.

В Strapi должны быть созданы коллекции:

- **Fish**: `Name` - текст, `Description` - текст, `Picture` - медиафайл.
- **Cart**: `tg_id` - текст, `fish_items` - связь с Fish_item, `client` - связь с Client.
- **Fish_item**: `fish` - связь с Fish, `cart` - связь с Cart.
- **Client**: `Email` - текст, `Name` - текст, `cart` - связь с Cart.

Также нужен Redis для хранения состояния пользователей. Сервис доступен для Linux или виртуальной машины WSL, устанавливается командами:

```sh
sudo apt install redis-server
sudo service redis-server start
```

API-ключ бота в телеграме можно получить у [@BotFather](https://t.me/BotFather).

Все переменные окружения указываются в файле `.env` в корне проекта:
```
TG_API_KEY=[API] 
STRAPI_API=[API] 
STRAPI_URL=http://localhost:1337
```
Переменные окружения представляют собою:

- TG_API_KEY - API ключ для обращения к боту в Телеграме.
- STRAPI_API - API ключ для запросов к Strapi.
- STRAPI_URL - адрес, по которому будет запущен Strapi

### Как использовать

Запустите Strapi и Redis, затем бота из корня проекта (папки, в которой лежит `tg_bot`):

```sh
python -m tg_bot.bot
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
