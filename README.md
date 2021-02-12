# CurrencyConverter
Установка
___
$ git clone https://github.com/Zloichist83361/CurrencyConverter_Qmobi.git

Как работает
___
Необходимо отправить POST запрос в формате JSON:

{"currency":[валюта В которую конвертируем], "value":[сумма в числовом типе данных (не строка)]}

Причем ключи JSON-а не могут быть другими, значение ключа "currency" может быть только "USD" или "RUB", а значение ключа "value" только Numeric.

Подобный запрос можно составить через тест:
___
 python test.py [АДРЕС]:[ПОРТ]
 
Ответ:
___
Если условия формата соблюдены - 200 OK и JSON вида: {"value": 15}

Иначе - 400 Bad Request.
