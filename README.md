# CurrencyConverter
Clone repository
___
$ git clone https://github.com/Zloichist83361/CurrencyConverter_Qmobi.git

How does it work
___
You need to send a POST request in JSON format:

{"currency":[currency into which we convert], "value":[sum in numeric data type (not string)]}

Moreover, JSON keys cannot be different, the value of the "currency" key can only be "USD" or "RUB", and the value of the "value" key can only be Numeric.

A similar request can be made through a test:
___
 python test.py [ADDRESS]:[PORT]
 
Response:
___
If the format conditions are met - 200 OK and JSON of the form: {"value": 15}

Else - 400 Bad Request.
