# 🧠 Hey-Compa – Backend MVP

Hey-Compa is your friendly backend assistant designed to help users (especially older or non-English speakers) manage and understand their bills. Built with Flask, SQLAlchemy, and OCR, Compa reads uploaded images, extracts key billing data, and guides users on how to pay — step-by-step.

---

## 🚀 MVP Features

- 🧾 Upload bill images (JPEG/PNG)
- 🔍 Extract vendor, due date, and amount using OCR
- 🧠 Match against user-trained payment guides
- 💬 Smart responses: “Ready to walk you through your PG&E bill?”
- 🗃️ Each user has their own secure data instance

---

## 🛠️ Tech Stack

- Python + Flask
- Flask-Login, SQLAlchemy, Flask-Migrate
- Tesseract OCR (`pytesseract`)
- PostgreSQL or SQLite
- JSON-based learning model via `PaymentGuide`

---

## 📁 Folder Structure (MVP)

Hey-Compa/
├── app/
│ ├── init.py
│ ├── api/
│ │ └── document_routes.py
│ ├── models/
│ │ ├── user.py
│ │ ├── document.py
│ │ └── payment_guide.py
│ ├── utils/
│ │ └── ocr_utils.py
├── run.py
├── config.py
├── requirements.txt
├── .flaskenv
└── Dockerfile\



## Future Upgrades

Voice input + voice step-by-step guidance

Shared guides across families or communities

Screenshot-based bill walkthroughs

Guide quality scoring based on usage/corrections
## 
