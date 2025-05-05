1) `python -m venv nazwa_venv`
2) Linux: `source nazwa_venv/bin/activate`
2) Win : `.\nazwa_venv\Scripts\Activate.ps1` ( należy zmienić ustawienia powershell'a, aby akceptował wywoływanie skryptów za pom. komend )
2) Tymczasowa zmiana polityki PowerShella: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`
3) (nazwa_venv): `pip install -r requirements.txt`
4) (nazwa_venv): `pip install --upgrade pip`
5) (nazwa_venv): `cd personal_blog`
6) (nazwa_venv): `python manage.py runserver`
<hr>
Strona jest pod adresem: http://127.0.0.1:8000, <br>
a admin-panel: http://127.0.0.1:8000/admin/ <br>
<br>
<i>login i hasło to admin</i>
