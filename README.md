# Personal Blog – Projekt Django

Prosty blog napisany w Django na potrzeby zajęć.

## Jak uruchomić projekt lokalnie?

### 1. Utwórz i aktywuj wirtualne środowisko

#### Linux / macOS:
```bash
python -m venv nazwa_venv
source nazwa_venv/bin/activate
```

#### Windows (PowerShell):
```powershell
python -m venv nazwa_venv
.\nazwa_venv\Scripts\Activate.ps1
```

> 💡 **Uwaga:** Jeśli pojawi się błąd dotyczący polityki uruchamiania skryptów, możesz tymczasowo zmienić ustawienia za pomocą:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

### 2. Zainstaluj zależności i zaktualizuj `pip`

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Przejdź do katalogu z projektem i uruchom serwer

```bash
cd personal_blog
python manage.py runserver
```

---

## Dostęp do strony

- Blog: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Panel administratora: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

> 🔐 **Login:** `admin`  
> 🔐 **Hasło:** `admin`
