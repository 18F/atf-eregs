# atf-eregs
Container and styles for an ATF eRegs instance

## Local Development

Use pip and npm to download the required libraries:

```bash
$ pip install -r requirements.txt
$ npm install -g grunt-cli bower
```

Then initialize the database, build the frontend, and run the server:

```bash
$ python manage.py migrate --fake-initial
$ python manage.py compile_frontend
$ python manage.py runserver
```

## Ports

For the time being, this application, which cobbles together
[regulations-core](https://github.com/18F/regulations-core) and
[regulations-site](https://github.com/18F/regulations-site), makes HTTP calls
to itself. The server therefore needs to know which port it is set up to
listen on.

We default to 8000, as that's the standard for django's `runserver`, but if
you need to run on a different port, either export an environmental variable
or create a local_settings.py as follows:

```bash
$ export VCAP_APP_PORT=1234
```

OR

```bash
$ echo "API_BASE = 'http://localhost:1234'" >> local_settings.py
```

## TODO

* Database config
* Search config
