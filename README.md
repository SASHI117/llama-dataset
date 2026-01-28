# Llama4-maverick-17B – Dataset creator Backend

**Repository:** `llama-dataset`

This repository contains the **backend API** for collecting and managing high-quality agricultural Q&A datasets used to fine-tune **LLaMA-4 Maverick 17B** with **LoRA** for **Farm Vaidya AI**.

The system is designed to be **secure, scalable, intern-safe, and research-grade**, with clean **JSONL datasets stored in AWS S3**.

---

## 🚀 Project Overview

**Farm Vaidya AI** is an AI assistant for Indian farmers (AP & Telangana), providing:

* Crop-specific agricultural guidance
* Multilingual support (Telugu / Hindi / English)
* Behavior-controlled responses (theory, practice, diagnostics, etc.)

This backend enables **structured data collection** via a web UI and safely stores it for model training.

---

## 🧠 Core Design Principles

* ✅ **JSONL contains ONLY user–assistant pairs**
* ✅ **System prompts are NOT stored in JSONL**
* ✅ System prompts are injected **at training time**
* ✅ Append-only dataset (no accidental deletion)
* ✅ UTF-8 safe (Indian languages supported)
* ✅ Secure AWS IAM access (programmatic only)

---

## 📁 Backend Folder Structure

```
llama-dataset/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── s3_client.py
│   │   └── validators.py
│   │
│   ├── schemas/
│   │   └── submission.py
│   │
│   ├── services/
│   │   ├── s3_service.py
│   │   └── logging_service.py
│   │
│   └── main.py
│
├── railway.toml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🔧 Tech Stack

* **Backend Framework:** FastAPI
* **Cloud Storage:** AWS S3
* **Deployment:** Railway
* **Frontend:** Vercel (separate repo)
* **Language:** Python 3.10+

---

## 📦 API Endpoints

### Health Check

```
GET /
```

Response:

```json
{ "status": "ok" }
```

---

### List Behaviors

```
GET /behaviors
```

Returns:

```json
[
  "theoretical",
  "practical",
  "calculation",
  "diagnostic",
  "preventive",
  "safety"
]
```

---

### Submit Dataset Entries

```
POST /submit
```

#### Request Body

```json
{
  "crop": "Rice",
  "behavior": "theoretical",
  "qa_pairs": [
    {
      "question": "బియ్యం పంటకు యూరియా ఎంత వేయాలి?",
      "answer": "ఎకరాకు 45–50 కిలోల యూరియా రెండు విడతలలో వేయాలి."
    }
  ],
  "submitted_by": "intern_name"
}
```

#### Response

```json
{
  "status": "success",
  "inserted": 1
}
```

---

## 🪣 AWS S3 Structure

```
s3://llama4mav-dataset/
│
├── Rice/
│   ├── Rice_systemprompt_theoretical.txt
│   ├── Rice_theoretical.jsonl
│   └── ...
│
└── metadata/
    └── logs/
        └── submissions.jsonl
```

* 📌 System prompts → **read-only**
* 📌 JSONL files → **append-only**

---

## 🔐 Environment Variables (Railway)

Set these in **Railway → Variables**:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=llama4mav-dataset
```

⚠️ **Never commit `.env` to GitHub**

---

## 🧪 Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## 🚀 Deployment

* Backend is deployed via **Railway (GitHub integration)**
* Every push to `main` triggers auto-deployment
* Frontend (Vercel) communicates via public Railway URL

---
