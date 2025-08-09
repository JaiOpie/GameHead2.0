# 🎮 Gaming Matchmaking Platform

A Django-based web application that allows gamers to create, join, and manage competitive events or matches. Users can sign up, host games, compete in head-to-head matches, and track their match history through a user dashboard.

---

## 🚀 Features

- 🔐 User authentication (Sign Up / Sign In / Logout)
- 🧑‍💼 Profile system for tracking match history
- 🎯 Create custom game events with match types and entry amounts
- 👫 Join events created by others
- 🏁 Complete matches and declare winners
- 🧾 Match history: View upcoming and completed matches
- 💻 Clean, modern UI with dark mode styling

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Dark-themed UI)
- **Database:** PostgreSQL
- **Authentication:** Django’s built-in auth system

---

## 🧪 How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/JaiOpie/GameHead2.0.git
cd GameHead2.0
```
### 2. Set up Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```
### 5. Create superuser (admin access)
```bash
python manage.py createsuperuser
```
### 6. Start development server
```bash
python manage.py runserver
```
### 7. Open in browser using the URL

[http://localhost:8000](http://localhost:8000)

### 🕹️ Start your gaming battle now on the ultimate matchmaking platform!