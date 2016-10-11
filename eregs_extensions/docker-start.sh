#!/bin/sh
pip install -e /app/extensions
./manage.py migrate
eregs pipeline 27 447 http://web:8000/api
eregs pipeline 27 478 http://web:8000/api
eregs pipeline 27 479 http://web:8000/api
eregs pipeline 27 555 http://web:8000/api
eregs pipeline 27 646 http://web:8000/api
