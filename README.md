# 🧠 Hey-Compa – Backend MVP

Hey-Compa is your friendly backend assistant designed to help users (especially older or non-English speakers) manage and understand their bills. Built with Flask, SQLAlchemy, OCR, and OpenAI, Compa reads uploaded images, extracts key billing data, and guides users on how to pay — step-by-step.

---

## 🚀 MVP Features

- 🧾 Upload bill images (JPEG/PNG)
- 🔍 Extract vendor, due date, and amount using OCR
- 🧠 Auto-generates step-by-step payment instructions with OpenAI
- 💬 Smart responses: “Ready to walk you through your PG&E bill?”
- 🗃️ Each user has their own secure data instance

---

## 🛠️ Tech Stack  (Backend)

- Python + Flask
- Flask-Login, SQLAlchemy, Flask-Migrate
- PaddleOCR (replacing pytesseract)
- OpenAI API (gpt-3.5-turbo) for step generation
- PostgreSQL or SQLite
- JSON-based learning model via `PaymentGuide`


## ⚙️ Tech Stack (Frontend)

- React (with Vite)
- Redux Toolkit for state management
- Tailwind CSS for styling
- React Router DOM for routing

---

## 📁 Folder Structure (MVP)

Hey-Compa/
├── app/
│   ├── uploads/ (temp saved images)    
│   ├── __init__.py
│   ├── api/
│   │   └── auth_routes.py
│       └── document_routes.py
│       └── payment_guide_routes.py
│       └── user_routes.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── payment_guide.py
│   │   └── guide_progress.py
│   ├── seeds/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── user.py
│   │   ├── document.py
│   │   └── payment_guide.py
│   ├── utils/
│   │   └── ocr_utils.py
│   │   └── test_ocr_standalone.py
│   ├── services/
├── client/
├── run.py
├── config.py
├── requirements.txt
├── .gitignore
├── .dockerignore
├── .flaskenv
└── Dockerfile

## 📌 Project Goals
- Make bill payment guidance accessible to anyone, especially underserved users
- Create a mobile-first experience that requires minimal technical knowledge
- Enable users to take a photo of their bill and instantly get guided steps
- Build a compassionate AI layer that remembers user struggles and adapts
- Keep Hey-Compa lightweight and privacy-friendly


## Future Upgrades

Voice input + voice step-by-step guidance

Shared guides across families or communities

Screenshot-based bill walkthroughs

Guide quality scoring based on usage/corrections
## 
