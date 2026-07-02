# Adaptive Exam Preparation and Performance Analyzer

## Overview

Students often struggle to prepare effectively for exams because their study materials, such as question banks and notes, are unorganized and difficult to analyze manually. They face challenges in identifying weak topics, managing revision time, and tracking preparation progress.

This project aims to develop an adaptive exam preparation platform where students can upload PDFs or handwritten notes along with question banks. The system uses OCR and lightweight NLP techniques to extract topics and automatically generate quizzes. Based on quiz accuracy and time taken, the platform analyzes student performance, identifies weak areas, and generates personalized study schedules and recommendations.

## Tech Stack

The system focuses on efficient software engineering and lightweight machine learning instead of relying on external AI APIs.

- **Frontend**: React
- **Backend Framework**: Django REST Framework (DRF)
- **Database**: PostgreSQL (Primary Data Source)
- **Caching & Sessions**: Redis (For API-level acceleration and temporary caching)
- **Machine Learning & Extraction Pipeline**: Python-based OCR/NLP libraries
  - **Camelot & Pandas**: For structured question bank extraction from tabular PDFs
  - **pdf2image, OpenCV, EasyOCR**: For image preprocessing and handwritten notes recognition
  - **RapidFuzz**: For OCR correction and academic term recovery

## Core Features & Architecture

### 1. Authentication and Identity Management

The system uses a stateless authentication model using JSON Web Tokens (JWT), which eliminates the need for server-side session storage and improves horizontal scalability.

- Secure registration and authentication workflows with Argon2/bcrypt hashing.
- Short-lived Access Tokens (60 minutes) and longer-lived Refresh Tokens (24 hours).

### 2. File Ingestion and Validation

A robust pipeline designed around asynchronous processing to prevent long-running extraction and OCR operations from blocking API requests.

- **Supported Formats**: Question Bank PDFs, Typed Notes (PDF/TXT), Handwritten Notes (PDF/Image).
- **Validation**: Strict size limits (60MB) and MIME type whitelists.
- **Duplicate Detection**: Uses SHA-256 file hashing to prevent uploading the same file multiple times.
- **Storage**: Direct-to-blob storage for uploaded raw files.

### 3. Content Extraction Pipeline

Converts uploaded educational documents into machine-readable structured content.

- **Question Banks**: Processed as structured documents using table-based extraction (Camelot) and data normalization (Pandas).
- **Typed Notes**: Direct text extraction (No OCR needed).
- **Handwritten Notes**: Uses OCR-based extraction requiring preprocessing (OpenCV: Grayscale, Gaussian blur, Otsu thresholding) followed by GPU-accelerated OCR (EasyOCR).

### 4. Content Processing Pipeline

Transforms extracted content into structured educational data for downstream consumption.

- Generates a unique Workspace Signature based on file hashes and processing pipelines to avoid repeating computationally expensive operations.
- Outputs structured data: topics, extracted questions, classification results, and educational content normalization.

### 5. Adaptive Quiz Generation & Study Schedules

- Generates adaptive quizzes based on uploaded notes and extracted topics.
- Tracks performance (quiz accuracy, total time) to provide insights and pinpoint weak areas.
- Automatically generates optimized study schedules and tailored recommendations to streamline exam revision.

## Database Structure

The PostgreSQL database is heavily normalized and indexed (Primary Keys, B-Trees, and Unique Constraints) for performance. Key entities include:

- **User Management**: Users, User Wallets, Token Transactions, Refresh Tokens
- **Content Management**: Workspaces, Files
- **Processing Pipelines**: Extraction Jobs, Extraction Artifacts, Processing Jobs
- **Educational Data**: Topics, Questions, Question Options
- **Assessment**: Quizzes, Quiz Attempts, Study Schedules

## Caching Strategy (Redis)

Redis is utilized exclusively for API-level request acceleration and is carefully scoped to not interfere with deterministic processing pipelines. Workers rely solely on PostgreSQL and Blob Storage as their authoritative sources of truth.

Cached components include:

- User Session & Wallet Cache
- Workspace Lists & Metadata (30 minutes TTL)
- Workspace Files & Topics (15 minutes TTL)
- Quiz Cache (Questions and Options)

## Setup & Running

A standard `docker-compose.yml` and `Makefile` are provided to set up the PostgreSQL and Redis containers efficiently.

To start the underlying services, run:

```bash
make up
```

*(Refer to the `Makefile` for other helper commands like `make build`, `make logs`, and `make clean`)*
