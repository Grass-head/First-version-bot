CatBot
=====
CatBot это бот для Telegram созданный с целью развлечь Вас в ваше свободное время.

Installing
----------
Создайте виртуальное окружение и активируйте его, потом в виртуальном окружении выполните, используя `pip`_:

.. code-block:: text
    pip install -r requirements.txt

Положите картинки с котиками в папку images.
Названия файлов должныначинаться с cat, а заканчиваться .jpg

Настройка
---------
Создайте файл settings.py и добавьте туда следующие настройки:
.. code-block:: python
    PROXY = {'proxy_url': 'socks5://ВАШ_SOCKS5_ПРОКСИ.ru:1080',
            'urllib3_proxy_kwargs': {'username': 'ЛОГИН', 'password': 'ПАРОЛЬ'}}

    API_KEY = "API ключ, полученый вами у BotFather"

    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

Запуск
------
В активированном виртуальном окружении выполните:
.. code-block:: text
    python bot.py