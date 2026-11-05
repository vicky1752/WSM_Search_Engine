# VKY Search Engine

A web-based document search application developed as part of the **Web
Search Mining** academic project. It demonstrates document
preprocessing, inverted indexing, information retrieval, relevance
ranking, and search enhancement techniques.

## Live Demo

**Live Website:** https://wsm-search-engine.onrender.com

## Repository

https://github.com/vicky1752/WSM_Search_Engine

## Project Overview

VKY Search Engine allows users to upload documents and search their
contents through a simple web interface.

The application extracts text from PDF, DOCX, and TXT files, processes
the extracted content, and builds an inverted index. When a user enters
a search query, the system retrieves relevant documents and ranks them
using TF-IDF and Cosine Similarity.

It also provides additional search features such as phrase search,
wildcard search, spelling suggestions, query expansion, and document
reading with highlighted search terms.

## Features

-   **Document Upload:** Supports PDF, DOCX, and TXT files.
-   **Text Preprocessing:** Performs lowercase conversion, tokenization,
    and stop-word removal.
-   **Inverted Indexing:** Creates an index mapping terms to their
    corresponding documents and positions.
-   **TF-IDF:** Calculates the importance of terms across documents.
-   **Vector Space Model:** Represents documents and queries as vectors.
-   **Cosine Similarity:** Measures query-document similarity for
    relevance ranking.
-   **Phrase Search:** Searches for complete phrases using positional
    information.
-   **Wildcard Search:** Supports wildcard-based term matching.
-   **Spelling Suggestions:** Provides alternative terms for misspelled
    queries.
-   **Query Expansion:** Expands queries using predefined related terms.
-   **Document Reader:** Displays extracted document content and
    highlights searched phrases.
-   **Compression:** Demonstrates gap encoding and variable-byte
    encoding.
-   **Retrieval Evaluation:** Includes Precision, Recall, and F1-score
    calculations.
-   **Link Analysis:** Demonstrates PageRank and HITS algorithms.
-   **Sentiment Analysis:** Includes basic lexicon-based sentiment
    analysis.

## Technology Stack

  Component               Technology
  ----------------------- -------------------------------
  Backend                 Python, Flask
  Frontend                HTML, CSS, JavaScript
  Document Processing     PyMuPDF, python-docx
  Information Retrieval   TF-IDF, Vector Space Model
  Indexing                Dictionary and Inverted Index
  Deployment              Render
  Version Control         Git and GitHub

## Running the Project Locally

### 1. Clone the repository

``` bash
git clone https://github.com/vicky1752/WSM_Search_Engine.git
cd WSM_Search_Engine
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

``` bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start the application

``` bash
python app.py
```

Open the local address displayed in the terminal (commonly
`http://127.0.0.1:5000`) in your browser.

## Project Structure

``` text
WSM_Search_Engine/
├── backend/
│   ├── algorithms/
│   │   ├── preprocessing.py
│   │   ├── inverted_index.py
│   │   ├── boolean_retrieval.py
│   │   ├── tfidf.py
│   │   ├── vector_space.py
│   │   ├── ranking.py
│   │   ├── phrase_search.py
│   │   ├── tolerant_retrieval.py
│   │   ├── query_expansion.py
│   │   ├── compression.py
│   │   ├── evaluation.py
│   │   ├── link_analysis.py
│   │   └── sentiment.py
│   ├── sample_documents/
│   ├── static/
│   ├── templates/
│   ├── uploads/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Project Objective

The objective is to develop a practical document retrieval system that
demonstrates the core concepts of Web Search Mining, including text
processing, indexing, query processing, and relevance-based ranking.

## Project Information

-   **Project Name:** VKY Search Engine
-   **Subject:** Web Search Mining
-   **Project Guide:** Prof. Rakesh Balbantaray
-   **Institution:** International Institute of Information Technology
-   **Department:** Computer Science and Engineering
-   **Programme:** Bachelor of Technology (B.Tech)
-   **Academic Session:** 2024--2028



  ## Project Team

| **Student Name** | **Student ID** |
|---|---|
| Vicky Kumar | B124153 |
| Subham Jyoti Sahu | B124136 |
| Om Saikrushna Behera | B124081 |
  
  

## Notes

-   Sample documents are stored in `backend/sample_documents/`.
-   User-uploaded files are stored in `backend/uploads/` during local
    execution.
-   On hosting platforms with ephemeral filesystems, uploaded files may
    not persist across service restarts or redeployments.
-   PageRank, HITS, and sentiment analysis are included as
    demonstrations of related Web Search Mining concepts; they are not
    presented as fully integrated production search features.

## Acknowledgement

This project was developed as part of the Web Search Mining academic
coursework under the guidance of **Prof. Rakesh Balbantaray**.
