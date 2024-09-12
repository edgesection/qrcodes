# qrcodes
## Перевод ссылок в QR-код
![Картинка](start.PNG)

Данная программа генерирует из ссылки QR-код

При этом программа заносит факт создания QR-кода в базу данных SQLite для составления списка данных, который поможет использовать данные для коммерческой аналитики.
Данные состоят из самой ссылки, количества попыток повторной генерации QR-кода, времени последнего обращения и времени первого внесения ссылки в БД.
Это позволит создать топ сайтов по количеству обращений, при этом понять, каким компаниям больше всего необходима данная программа.

Программа удобна тем, что после установки библиотеки БД, вам больше ничего не нужно с ней делать, так как программа сама создаст файл БД, таблицы и записи в ней.
Программу можно запустить на любом устройству, где можно установить Python.
Также ссылка форматируется так, чтобы при добавлении допустим протокола безопасности, программа не создаёт повторную запись, а отбрасывает незначительные параметры в ссылке.

![Картинка](top10.PNG)

> [!IMPORTANT]
> Перед запуском программы, выполните команду в консоли: python3 -m pip install qrcode pillow
> 
> Эта команда устанавливает библиотеку QRCode с пакетом pillow на 3 версию Python
>
> После установите SQLite, ведя команду: python3 -m pip install sqlite3-api

- [x] Создание репозитория и проекта
- [x] Создание презентации
- [x] Создание кода

> [!NOTE]
> .

> [!TIP]
> .

> [!WARNING]
> .

> [!CAUTION]
> .
