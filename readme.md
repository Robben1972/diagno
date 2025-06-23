```
git clone diagno.git
cd diagno
```

```
python3 -m venv venv
source venv/bin/activate
```

```
python3 manage.py makemigrations\
python3 manage.py migrate
```

```
python3 manage.py createsuperuser
```

```
python3 manage.py runserver
```