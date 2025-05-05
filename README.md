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
aaaaaaaa
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

# 🔁 Jak sforkować repozytorium, wprowadzić zmiany i wysłać Pull Request

## ✅ 1. Zrób **fork** repozytorium na GitHubie

1. Wejdź na repozytorium oryginalne (np. `https://github.com/mpolan/projekt_blog`)
2. Kliknij przycisk **Fork** (prawy górny róg)
3. Wybierz swój profil – GitHub utworzy **Twoją kopię repozytorium**

---

## ✅ 2. Sklonuj swojego forka lokalnie

```bash
git clone https://github.com/TWOJA_NAZWA/projekt_blog.git
cd projekt_blog
```

> 🔁 Zamień `TWOJA_NAZWA` na swoją nazwę użytkownika na GitHubie.

---

## ✅ 3. Utwórz nowy branch do zmian

```bash
git checkout -b dodaj-funkcje
```

---

## ✅ 4. Wprowadź zmiany w kodzie

Edytuj pliki, dodaj nowe funkcje, poprawki itp.

---

## ✅ 5. Zapisz zmiany (commit)

```bash
git add .
git commit -m "Dodano wyszukiwanie postów"
```

---

## ✅ 6. Wyślij zmiany do swojego repozytorium na GitHubie (push)

```bash
git push origin dodaj-funkcje
```

---

## ✅ 7. Otwórz **Pull Request** (PR)

1. Wejdź na swojego **forka** na GitHubie
2. Zobaczysz przycisk **"Compare & pull request"**
3. Kliknij, opisz co zrobiłeś, np.:
   > Dodano funkcję wyszukiwania postów po tytule i treści.
4. Kliknij **"Create Pull Request"**

---

## ✅ 8. Co dalej?

- Właściciel oryginalnego repo otrzyma Twój Pull Request
- Może go przejrzeć, skomentować i **zaakceptować (Merge)**

---

📌 Gotowe! Właśnie wysłałeś swój wkład do projektu Open Source 💪
