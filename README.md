<h1 align="center">Adaptive Exam Preparation and Performance Analyzer</h1>

<p align="center">
  <strong>An intelligent platform designed to streamline student exam preparation using OCR, NLP, and adaptive learning algorithms.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
</p>

---

## 📖 Overview

The **Adaptive Exam Preparation and Performance Analyzer** eliminates the chaos of unorganized study materials. By allowing students to upload varied educational documents (PDFs, typed notes, and handwritten notes), the platform automatically extracts knowledge topics, generates personalized quizzes, and provides deep performance analytics. 

Instead of relying on heavy third-party AI APIs, the system utilizes an efficient, self-hosted machine learning extraction pipeline built on top of standard Python NLP/OCR libraries.

## ✨ Features

- **Robust API Layer**: Fully stateless RESTful API powered by Django REST Framework (DRF).
- **Secure Authentication**: JWT-based authentication using `Argon2/bcrypt` hashing, with robust token lifecycle management.
- **Wallet & Token System**: Built-in wallet functionality (`UserWallet`, `TokenTransactions`) tracking platform usage and limits.
- **Smart Workspaces**: Isolated workspaces for managing different subjects, files, and study schedules.
- **Asynchronous File Ingestion**: Upload validation, SHA-256 duplicate detection, and direct-to-blob storage designed for heavy concurrent usage.
- **Automated Processing Pipeline**: (In Progress) Converts PDFs, question banks, and handwritten notes to machine-readable objects using OCR and text-processing strategies.
- **Adaptive Assessments**: (In Progress) Dynamically creates quizzes based on extracted knowledge graphs and student proficiency.

## 🛠️ Tech Stack

- **Backend Framework**: Django & Django REST Framework
- **Database**: PostgreSQL
- **Caching & Broker**: Redis (for API acceleration and asynchronous task queues)
- **Infrastructure**: Docker & Docker Compose
- **Data Science/OCR Toolkit**: Camelot, Pandas, OpenCV, EasyOCR, RapidFuzz, pdf2image *(coming soon in the processing pipeline)*

---

## 📂 Project Structure

The Django application is heavily modularized into distinct, decoupled apps:

```text
backend/
├── authentication/  # JWT auth, custom user models, login/registration logic
├── common/          # Shared utilities, standardized API responses, base models
├── config/          # Django core settings and WSGI/ASGI entrypoints
├── files/           # File ingestion, hashing, and storage logic
├── processing/      # Asynchronous extraction and NLP/OCR pipelines
├── quiz/            # Assessment generation and attempts logic
├── schedule/        # Automated study schedule generation
├── wallet/          # User token balances and transaction ledgers
└── workspace/       # Subject/Workspace isolation for users
```

---

## 🚀 Getting Started

Follow these steps to get a development environment running locally.

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- `make` (for utilizing the Makefile commands)
- Python 3.10+ (if running the Django server locally outside of Docker)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/adaptive-exam-platform.git
cd adaptive-exam-platform
```

### 2. Configure Environment Variables
Copy the example environment variables file and configure your local secrets (like database credentials).
```bash
cp .env.example .env
```
*(Ensure `POSTGRES_DB`, `POSTGRES_USER`, and `POSTGRES_PASSWORD` are set in `.env`)*

### 3. Spin up the Infrastructure
Use the provided `Makefile` to quickly start the PostgreSQL and Redis containers in the background.
```bash
make up
```

### 4. Setup the Backend
Navigate to the backend directory, install requirements, and apply database migrations.
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

# Apply the normalized schema and indexes to PostgreSQL
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```
The API should now be accessible at `http://127.0.0.1:8000/`.

---

## 🧪 Makefile Commands

A handy `Makefile` is included in the root directory. Common commands include:

- `make up`: Starts Postgres and Redis containers.
- `make down`: Stops and removes the containers.
- `make logs`: Follows container logs.
- `make db-shell`: Opens an interactive `psql` shell into the Postgres database.
- `make clean`: Tears down containers and completely removes data volumes (Use with caution!).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
