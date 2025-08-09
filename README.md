# 🎮 Gaming Matchmaking Platform

A Django-based competitive gaming platform where players can create, join, and manage events, track their wallet transactions, and compete in matches with a transparent credit/debit system.

---

## 🚀 Features

- 🔐 **User Authentication** (Sign Up / Sign In / Logout)
- 💰 **Wallet System**
  - Automatic **₹100 sign-up bonus** for new users
  - Credit/Debit transactions with live transaction history
  - Entry fee deduction on joining matches
  - Refund on event deletion
  - Winner gets credited when an event is completed
- 🧑‍💼 **Profile Dashboard**
  - View upcoming matches
  - View completed matches
  - View and search/sort transaction history
- 🎯 **Event Management**
  - Create custom game events with match types and entry amounts
  - Join events if wallet balance is sufficient (low balance warning in popup)
  - Refund wallet balance when event is deleted
- 🏁 **Match Management**
  - Complete matches and credit winnings to the selected winner
- 🧾 **Match & Transaction History**
  - Search and sort transactions (server-side filtering via API)
  - Transaction table with clean dark-mode design
- 💻 **UI Improvements**
  - Dark-mode themed responsive layout
  - Popup warnings and notifications
  - Transaction history in a modern table layout

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Dark-themed UI), JavaScript (fetch API)
- **Database:** PostgreSQL
- **Authentication:** Django’s built-in auth system
- **API:** Django REST Framework (DRF) for match & transaction management

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
