# 🧠 Anki Flashcard Generator (Node.js + FastAPI)

This is a **full-stack backend system** for automatically generating Anki-compatible flashcard decks (`.apkg`) from educational content using Node.js, Prisma, PostgreSQL, and FastAPI (Python). It allows you to input structured topic content via REST APIs and generate downloadable Anki decks using the official Anki source code.

---

## 🚀 Tech Stack

| Layer        | Tech                                 |
| ------------ | ------------------------------------ |
| API Gateway  | Node.js + Express                    |
| Database     | PostgreSQL (hosted on Neon)          |
| ORM          | Prisma                               |
| Deck Builder | Python (FastAPI + genanki/Anki repo) |
| Hosting      | Render (for both Node.js & Python)   |
| Uptime Pings | UptimeRobot                          |

---

## 🏗️ Architecture Overview

```
                ┌────────────────────────┐
                │  User / Postman Client│
                └────────────┬───────────┘
                             │
                      [POST /api/flashcards/content]
                             │
        ┌─────────────▶ Node.js Backend (Express)
        │                  - Stores content
        │                  - Sends ID to FastAPI
        │                  - Returns metadata & cards
        │
[GET /api/flashcards/content/:id/generate]
        │
        └─────────────▶ FastAPI Python Microservice
                           - Generates .apkg using Anki
                           - Returns download link

```

---

## 📦 How to Set Up Locally

### 1. Clone the Repository

```bash
git clone git@github.com:Kraken57/anki.git
cd node-backend
```

### 2. Install Node & Python Dependencies

```bash
npm install         # For Node.js (Express + Prisma)

# This in cd python-microservice
pip install -r requirements.txt  # For FastAPI microservice
```

### 3. Environment Variables

**Node.js Backend (`.env`)**

```
DATABASE_URL=postgresql://<user>:<password>@<host>/<db>
PYTHON_SERVICE_URL=https://anki-python-microservice.onrender.com
```

**FastAPI Python Microservice**

```
# (Optional) Add anything needed for Anki source integration
```

### 4. Start Servers Locally

```bash
# Terminal 1
node src/index.js

# Terminal 2 (in /python-service)
uvicorn main:app --reload --port 8080
```

---

## 🔌 Public API Endpoints

### ➕ 1. Create Flashcard Content

**POST** `https://anki-node-backend.onrender.com/api/flashcards/content`

#### Request:

```json
{
  "subject": "Quantum-Computing",
  "title": "Qubits and Quantum Superposition",
  "content": "Quantum computing harnesses quantum-mechanical phenomena to perform calculations..."
}
```

#### Response:

```json
{
  "topic": {
    "id": "cmbar85f00000kk0102g9ab00",
    "title": "Qubits and Quantum Superposition",
    "subject": "Quantum-Computing",
    "content": "Quantum computing harnesses...",
    "createdAt": "2025-05-30T12:03:27.467Z"
  }
}
```

---

### 🎴 2. Generate Flashcards

**POST** `https://anki-node-backend.onrender.com/api/flashcards/content/:id/generate`

#### Response:

```json
{
  "metadata": {
    "deck_id": "Quantum-Computing_cmbar85f00000kk0102g9ab00",
    "download_link": "https://anki-python-microservice.onrender.com/download/Quantum-Computing_cmbar85f00000kk0102g9ab00",
    "file_path": "/app/anki/Quantum-Computing_cmbar85f00000kk0102g9ab00.apkg"
  },
  "flashcards": [
    {
      "id": "card_1",
      "front": "Question 1: About Qubits and Quantum Superposition",
      "back": "Quantum computing harnesses...",
      "tags": ["quantum-computing"]
    }
    // more cards...
  ],
  "status": "success"
}
```

---

### 📥 3. Python Card Generator (Direct)

**POST** `https://anki-python-microservice.onrender.com/create_card`

#### Request:

```json
{
  "id": "cmbar85f00000kk0102g9ab00",
  "subject": "Quantum-Computing",
  "title": "Qubits and Quantum Superposition",
  "content": "Quantum computing harnesses..."
}
```

#### Response:

Same structure as above.

---

## 🧪 How to Test With Postman

### Example: Generate Deck

1. `POST` to `https://anki-node-backend.onrender.com/api/flashcards/content`
2. Copy `topic.id` from response
3. `POST` to `https://anki-node-backend.onrender.com/api/flashcards/content/<topicId>/generate`
4. Visit `download_link` to fetch `.apkg` -->  Will only work at localhost

---

## 🧱 Issues Faced & Solutions

| Issue                                        | Solution                                                                 |
| -------------------------------------------- | ------------------------------------------------------------------------ |
| 💤 Render sleeps free services after 15 mins | Used [UptimeRobot](https://uptimerobot.com) with `/healthz` GET endpoint |
| ❌ UptimeRobot 405 error                      | Added `@app.get("/healthz")` route in FastAPI                            |
| 📦 genanki too limited                       | Switched to official Anki source repo for better .apkg parsing           |
| 🐍 Communication between Node and Python     | Used `axios` in Express to call the Python service                       |

---

## 📝 Future Improvements

* Add user authentication for deck history
* Improve flashcard chunking
* Optimize deck generation speed

---

## 📂 Folder Structure

```
project-root/
├── backend-node/
│   ├── routes/flashcards.js
│   ├── prisma/
│   ├── .env
├── python-service/
│   ├── main.py
│   ├── card_creator.py
│   ├── anki/
```

---

## ✨ Credits

* [genanki](https://github.com/kerrickstaley/genanki)
* [Anki Source](https://github.com/ankitects/anki)
* [Render](https://render.com)
* [Neon Database](https://neon.tech)
* [UptimeRobot](https://uptimerobot.com)

---

