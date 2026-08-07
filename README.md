# ☕ Coffee Shop AI Barista

A serverless Retrieval-Augmented Generation (RAG) application built using the **Google Agent Development Kit (ADK)** and **Gemini**, deployed on **Google Cloud Run**.

The application acts as an AI coffee barista capable of answering menu-related questions by retrieving relevant menu items from **Google Firestore** using **vector embeddings** and **cosine similarity search** before generating grounded responses with Gemini.

---

## Demo
<p align="center">
<img width="1363" height="665" alt="image" src="https://github.com/user-attachments/assets/942347d0-64f2-4817-9835-1f60f777f416" />
</p>

---

## Features

* 🤖 Google Agent Development Kit (ADK)
* 🧠 Gemini-powered reasoning
* 🔍 Retrieval-Augmented Generation (RAG)
* 📄 Firestore document store
* 📈 Embedding-based semantic search
* 📐 Cosine similarity retrieval
* 🌐 Streamlit frontend
* ☁️ Google Cloud Run deployment
* ⚡ Streaming responses

---

# System Flow

```text
User
 │
 ▼
Streamlit Web UI
 │
 ▼
Google Cloud Run
 │
 ▼
Google ADK Agent
 │
 ▼
Custom Retrieval Tool
 │
 ▼
Generate Query Embedding
 │
 ▼
Firestore
(Menu Documents + Stored Embeddings)
 │
 ▼
Cosine Similarity Search
 │
 ▼
Top-K Relevant Menu Items
 │
 ▼
Gemini
 │
 ▼
Grounded Response
```

---

# Tech Stack

| Layer           | Technology                     |
| --------------- | ------------------------------ |
| Frontend        | Streamlit                      |
| Agent Framework | Google ADK                     |
| LLM             | Gemini                         |
| Database        | Firestore                      |
| Retrieval       | Embeddings + Cosine Similarity |
| Deployment      | Google Cloud Run               |
| Language        | Python                         |

---

# Project Structure

```text
.
├── agent.py              # ADK agent and retrieval tool
├── app.py                # Streamlit frontend
├── seed.py               # Seeds Firestore with menu items and embeddings
├── requirements.txt
├── menu.json             # Deprecated (used only for initial local development)
└── README.md
```

> **Note:** `menu.json` is retained only as a reference from the initial prototype. The production implementation retrieves menu documents directly from Firestore and no longer depends on this local file.

---

# Retrieval Pipeline

1. User submits a query.
2. The ADK agent invokes the retrieval tool.
3. An embedding is generated for the user query.
4. Firestore documents containing stored embeddings are retrieved.
5. Cosine similarity is computed between the query embedding and document embeddings.
6. The most relevant menu items are selected.
7. Retrieved context is supplied to Gemini.
8. Gemini generates a grounded response.

---

# Firestore Data Model

Each menu item is stored as a Firestore document containing fields similar to:

```text
name
description
price
category
tags
embedding (vector)
```

The embedding field enables semantic retrieval instead of exact keyword matching.

<img width="1365" height="677" alt="image" src="https://github.com/user-attachments/assets/df15cb70-55ae-40d9-91f5-d18723d8dc70" />

---

# Deployment

The application is fully serverless.

```text
Python Application
        │
        ▼
Docker Container
        │
        ▼
Google Cloud Run
        │
        ▼
HTTPS Endpoint
```

---

# Running Locally

```bash
git clone https://github.com/<username>/<repository>

cd <repository>

pip install -r requirements.txt

streamlit run app.py
```

---

# Future Improvements

* Hybrid Search (Keyword + Vector)
* Firestore Vector Search API
* Metadata filtering
* Multi-agent workflow
* Conversation memory
* Vertex AI integration
* Authentication & IAM

---
