# TriAgeRAG 🚑📄

## 📌 Overview

**TriAgeRAG** is a ticket triage system that classifies and processes support requests using a **Retrieval-Augmented Generation (RAG)** pipeline.

It combines:

* Vector search (for context retrieval)
* LLM-based classification (for decision making)
* Multi-step processing (index → retrieve → triage)

---

## ⚙️ Tech Stack

* **Python**
* **ChromaDB** (Vector Database)
* **Sentence Transformers** (Embeddings)
* **Google GenAI API**
* **Pandas** (Data handling)
* **dotenv** (Environment management)

---

## 📂 Project Structure

```
├── indexer.py        # Builds vector database from documents
├── main.py           # Runs the triage pipeline
├── retriever.py      # Retrieves relevant context using embeddings
├── agent.py          # Triage logic (LLM-based classification)
├── data/             # Input documents / tickets
├── .env              # API keys
├── requirements.txt
```

---

## 🔄 How It Works

### Step 1: Indexing

* Reads documents from dataset
* Converts text into embeddings using Sentence Transformers
* Stores embeddings in ChromaDB

### Step 2: Retrieval

* Given a query/ticket
* Finds most relevant documents from vector DB

### Step 3: Triage

* Uses retrieved context
* Sends it to LLM (Google GenAI)
* Classifies ticket (e.g., valid / escalated / category)

---

## ▶️ How to Run

### 1. Clone the repo

```
git clone https://github.com/Khanwajahath/TriAgeRAG.git
cd TriAgeRAG
```

---

### 2. Install dependencies

```
pip install -r requirements.txt
```

---

### 3. Setup environment variables

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

### 4. Run Indexer (IMPORTANT)

Before running the system, you must build the vector database:

```
python indexer.py
```

---

### 5. Run Main Pipeline

```
python main.py
```

---

## 📦 Key Imports Used

```python
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from google import genai

from retriever import retrieve

import chromadb
from sentence_transformers import SentenceTransformer

import pandas as pd
from agent import triage

import time
```

---

## ✨ Features

* ✅ Retrieval-Augmented Generation (RAG)
* ✅ Vector similarity search with ChromaDB
* ✅ Modular pipeline (Indexer → Retriever → Agent)
* ✅ Multi-model triage capability (extendable)
* ✅ Logging & structured outputs (optional extension)

---

## 🚀 Future Improvements

* Add UI (Streamlit / Web App)
* Add multiple LLM fallback system
* Improve retrieval accuracy (hybrid search)
* Add evaluation metrics for triage accuracy

---

## 🧠 Key Insight

> The system separates **knowledge retrieval** from **decision making**, making it scalable and extensible for real-world support systems.

---
 

## 👨‍💻 Author

**Mohammed Wajahathulla Khan**

* GitHub: https://github.com/Khanwajahath
