> python -m venv nazwa_venv
> Linux: source nazwa_venv/bin/activate
> Win : ./venv/Scripts/Activate.ps ( należy zmienić ustawienia powershell'a, aby akceptował wywoływanie skryptów za pom. komend )
> (nazwa_venv): pip install -r requirements.txt
> (nazwa_venv): pip install --upgrade pip
> (nazwa_venv): cd personal_blog
> (nazwa_venv): python manage.py runserver