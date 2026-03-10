# Resilience-OS

Resilience-OS is a **privacy-first emotional regulation system** designed as a structured calming engine — not a chatbot.

Instead of conversational AI, the system guides users through **deterministic flows** that support emotional grounding, reflection, and safe journaling.

The goal is to provide **structured support during emotional distress while maintaining user privacy and control**.

---

# What This App Is

Resilience-OS is:

• A **structured calming system**  
• A **deterministic emotional regulation flow**  
• A **privacy-first journaling and venting tool**  
• A **state-driven resilience engine**  
• **Offline-first by design**

Rather than interpreting emotions like an AI chatbot, the system provides **clear structured pathways** for emotional regulation.

Core components include:

- Breathing exercises
- Comfort prompts
- Grounding techniques
- Reflection and vent boards
- Secure storage with optional feature lock

---

# What This App Is NOT

Resilience-OS is **not**:

- A therapy replacement
- A crisis intervention service
- A diagnostic tool
- A medical system
- An AI therapist

The system does **not interpret mental health conditions or provide medical advice**.

It simply provides **structure, stability, and a safe private space**.

---

# Core Architecture Philosophy

The architecture follows several principles:

• **Deterministic flows** instead of AI conversation  
• **Clear separation of responsibilities**  
• **Privacy by default**  
• **Offline-first capability**  
• **Minimal cognitive load**

Each component performs a **single clear responsibility**.

| Layer    | Responsibility          |
| -------- | ----------------------- |
| Routes   | API endpoints           |
| Engines  | Core behavioral logic   |
| State    | User preference storage |
| Database | Persistent storage      |
| Security | Authentication & locks  |

---

# Backend Architecture

```
app/
│
├── api/
│   ├── auth/          # Authentication (JWT, login, register)
│   ├── routes/        # Vent, reflection, state, lock endpoints
│   ├── schemas.py     # API request/response models
│   └── dependencies.py
│
├── engines/           # Core behavior managers
│   └── file_content_manager.py
│
├── state/             # Application state engine
│   └── app_state.py
│
├── database/          # SQLite database layer
│   └── db.py
│
├── config/            # Environment configuration
│   └── settings.py
│
└── api/main.py        # FastAPI application entrypoint
```

---

# Privacy-First Design

Resilience-OS prioritizes **user control and data privacy**.

Features include:

• **Guest mode journaling (no login required)**  
• **Anonymous device identity (UUID)**  
• **Optional account login for data persistence**  
• **Secure password hashing (bcrypt)**  
• **JWT authentication**  
• **Soft-delete journaling system**

Guest users can write entries without an account.  
Logged-in users gain **cross-device persistence**.

---

# Journaling System

The system currently supports two journaling modes:

### Vent Board

A space to release thoughts safely.

### Reflection Board

A structured space for reflective writing.

Features include:

- entry locking with password
- secure storage
- soft delete
- ownership protection

---

# Authentication System

Authentication uses **JWT tokens**.

The backend supports:

• User registration  
• Login authentication  
• Access tokens  
• Refresh tokens  
• Guest session support  
• Anonymous ID tracking

Guest entries can later be **migrated to a registered account**.

---

# Tech Stack

Backend:

- **Python**
- **FastAPI**
- **SQLite**
- **bcrypt**
- **JWT authentication**

Planned frontend:

- **React Native**

---

# 🚀 Running the Backend

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/resilience-os.git
cd resilience-os
```

### 2️⃣ Create virtual environment

```bash
python -m venv myvenv
```

Activate:

Windows

```bash
myvenv\Scripts\activate
```

Mac/Linux

```bash
source myvenv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env`

```
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
```

### 5️⃣ Run server

```bash
uvicorn app.api.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

API docs:

```
http://127.0.0.1:8000/docs
```

---

# 📡 API Overview

| Endpoint                | Description             |
| ----------------------- | ----------------------- |
| `/auth/register`        | Create account          |
| `/auth/login`           | Login & receive JWT     |
| `/auth/refresh`         | Refresh access token    |
| `/vent`                 | Create vent entry       |
| `/vent/{id}/open`       | Open vent entry         |
| `/reflection`           | Create reflection entry |
| `/reflection/{id}/open` | Open reflection entry   |
| `/lock`                 | Feature lock management |
| `/state`                | User preference state   |

Full interactive documentation is available via **FastAPI Swagger**.

---

# Current Development Status

### Backend

✔ REST API architecture  
✔ JWT authentication  
✔ Guest mode journaling  
✔ Secure entry ownership  
✔ Password-protected entries  
✔ SQLite persistence

### In Progress

⬜ Mobile frontend  
⬜ Offline mobile storage  
⬜ UX flow integration

---

# Emotional Regulation Flow

### Distressed Flow

1. Breathing exercise
2. Comfort message
3. Grounding activity
4. Stability check
5. Rumination interruption

Post-stabilization options:

- Vent
- Reflect
- Reach out

---

### Stable Flow

Users may:

• Vent  
• Reflect  
• Practice grounding  
• Customize preferences  
• Review past entries

---

# 🌊 Emotional Regulation Flow

### Distressed Flow

1. Breathing exercise
2. Comfort prompt
3. Grounding action
4. Stability check
5. Rumination interruption

Post-stabilization options:

- Vent
- Reflect
- Reach out

---

### Stable Flow

Users may:

• Vent  
• Reflect  
• Practice grounding  
• Customize system preferences  
• Review saved entries

---

# Design Principles

Resilience-OS follows five core principles:

**Calm > Complexity**  
**Structure > Conversation**  
**Privacy > Data Collection**  
**Stability > Intelligence**  
**Determinism > Randomness**

---

# Why This Project Exists

Many emotional-support tools rely heavily on AI conversation.

Resilience-OS explores a different approach:

**structured emotional regulation flows rather than conversational AI.**

The goal is to provide **predictable, calming support during distress without overwhelming the user.**

---

# Team

Developed as a **research-driven emotional support system** with a modular backend architecture designed for long-term extensibility.

---

# License

MIT License

---

# Future Research Directions

Possible research extensions include:

- Behavioral flow optimization
- Optional AI-assisted reflection tagging
- Long-term emotional resilience modeling
- Offline-first mental health infrastructure
