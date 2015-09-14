# atf-eregs
Container and styles for an ATF eRegs instance

## Local Development

Use pip to download the required libraries:

```bash
$ pip install -r requirements.txt
```

Then initialize the database and run the server:

```bash
$ python manage.py migrate --fake-initial
$ python manage.py runserver
```

## TODO

* Database config
* Port config
