# 🧠 Resilience-OS

Resilience-OS is a privacy-first emotional regulation system designed as a structured calming engine — not a chatbot.

It guides users through grounded, deterministic flows to help regulate distress, reflect safely, and build emotional resilience over time.

---

## 🌿 What This App Is

Resilience-OS is:

- A structured calming system
- A deterministic emotional regulation flow
- A privacy-first journaling and venting tool
- A state-driven resilience engine
- Offline-first and minimal by design

It does **not** rely on conversational AI for core behavior.

Instead, it uses clearly defined flows:

- Breathing
- Comfort prompts
- Grounding techniques
- Reflection and vent boards
- Safe storage with optional feature lock

---

## 🚫 What This App Is NOT

Resilience-OS is NOT:

- A therapy replacement
- A crisis intervention service
- A diagnostic tool
- An AI chatbot
- A mood tracker app

It does not attempt to interpret emotions or provide medical advice.

It simply provides structure, safety, and space.

---

## 🧭 Core Architecture Philosophy

The system is built around:

- Deterministic state flows
- A clear separation of responsibilities
- Privacy by default
- Offline-first design
- Minimal cognitive load for users

MainFlow acts purely as a traffic controller.
Engines handle behavior.
State stores user preferences.
Content managers handle storage.
Feature locks protect sensitive entries.

No component overreaches its responsibility.

---

## 🏗 Current Architecture

app/
│
├── engines/ # Behavioral engines (OS, rumination, vent, reflection)
├── flow/ # Main traffic controller
├── state/ # AppState (user state & preferences)
└── main.py # Entry point

---

## 🌊 Emotional Flow Design

### Distressed Flow

1. Breathing (mandatory)
2. Comfort message
3. Grounding action
4. Stability check
5. Rumination interruption (if needed)
6. Post-stable options:
   - Vent
   - Reach out
   - Continue

---

### OK Flow

User can:

- Run Resilience OS manually
- Practice calm
- Reflect
- Vent
- Personalize system tone
- View saved entries
- Manage feature lock

---

## 🔐 Privacy & Safety

- Vent and reflection entries are optional to save
- Feature lock uses hashed PIN (bcrypt)
- No content leaves the device (current CLI version)
- No AI dependency
- No forced reminders

The system only stores what the user explicitly agrees to store.

---

## 🛠 Tech Stack (Current Phase)

- Python
- SQLite (planned integration)
- bcrypt (feature lock security)

Planned:

- FastAPI backend
- React Native frontend
- Offline-first database layer

---

## 🚀 Roadmap

- [x] CLI state engine
- [x] Deterministic flow control
- [x] Vent & reflection boards
- [x] Feature lock protection
- [ ] SQLite persistence layer
- [ ] REST API layer
- [ ] Mobile frontend (React Native)
- [ ] Optional AI-assisted tag refinement (future phase)

---

## 🧠 Design Principles

- Calm > Complexity
- Structure > Conversation
- Privacy > Data collection
- Stability > Intelligence
- Determinism > Randomness

---

## 💛 Why This Exists

Resilience-OS was built to provide structure during emotional overload.

Not advice.
Not diagnosis.
Not chatter.

Just grounded steps.

---

## 👥 Team

Built as a collaborative backend + frontend architecture project.

Focused on clean modular design and long-term extensibility.

---

## 📜 License

(Choose your license here — MIT recommended for open source)
