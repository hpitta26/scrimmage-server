# scrimmage

FIU Pokerbots Scrimmage Server, released under the MIT License

- Create .env and copy content from .env.example into it

To run locally, do:
- `brew install rabbitmq scons boost postgres`
- `python -m venv venv`
- `source venv/bin/activate`
- `initdb --username=postgres ~/pbots; pg_ctl -D ~/pbots -l logfile start; createdb -U postgres pbots`
- `pip install -r requirements.txt`
- Run `from scrimmage import db; db.create_all()` from a python3 shell

If the last command doesn't work run this in the Python Shell instead:
```bash
from scrimmage import app, db 
with app.app_context(): 
	db.create_all()
```

then do

To run the server and worker, run in four separate tabs:

```bash
rabbitmq-server

# http://localhost:15672/ --> Admin Panel
```

```bash
flask run

# http://localhost:8000/ --> frontend and backend
```

```bash
celery -A scrimmage.celery_app worker --loglevel=info --concurrency=1
```

```bash
celery -A scrimmage.celery_app flower

# http://localhost:5555/ --> Admin Panel
```

---
Additional Debugging commands:
```bash
# Drop DB in case of issues
dropdb -U postgres pbots

# Status of the DB
pg_ctl -D ~/pbots status

rabbitmqctl stop # stop process

rabbitmqctl status

rabbitmq-plugins enable rabbitmq_management # enable rabbitmq Admin Panel in case you get 403 errors
```
---

Production
----------

1. We use [Convox](https://convox.com/) for deploys. Once you make a change, simply run `convox deploy`.

Setting up convox is a little bit of a pain - you have to create the necessary resources and set the required environment variables. Once you have a successful deploy, however, you need to run `convox run web python manage.py shell` and then run `from scrimmage import db; db.create_all()` on the first time.


Development
-----------

When you add new database features, do `python manage.py db migrate` and `python manage.py db upgrade`.
