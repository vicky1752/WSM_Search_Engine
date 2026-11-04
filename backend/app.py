
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pymupdf
from docx import Document

from algorithms.inverted_index import build_inverted_index
from algorithms.ranking import rank_documents
from algorithms.phrase_search import phrase_search
from algorithms.tolerant_retrieval import (
    wildcard_search,
    spelling_correction
)
from algorithms.query_expansion import expand_query

import re
import html
from markupsafe import Markup


app = Flask(__name__)
app.secret_key = "mini-search-engine-secret"

# Use absolute paths so the application works on Render too
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
SAMPLE_FOLDER = os.path.join(BASE_DIR, "sample_documents")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAMPLE_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Document collection and inverted index
documents = []
index = {}


# Check supported file formats
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Extract text from PDF
def extract_pdf(file_path):
    text = ""

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text() + "\n"

    return text


# Extract text from DOCX
def extract_docx(file_path):
    document = Document(file_path)
    return "\n".join(
        paragraph.text for paragraph in document.paragraphs
    )


# Extract text from TXT
def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()


# Load permanent sample documents and visitor uploads
def load_saved_documents():
    global index

    documents.clear()

    # Load sample documents first, then user uploads
    folders = [SAMPLE_FOLDER, UPLOAD_FOLDER]

    loaded_paths = set()

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

        for filename in sorted(os.listdir(folder)):

            if not allowed_file(filename):
                continue

            file_path = os.path.join(folder, filename)

            if not os.path.isfile(file_path):
                continue

            # Prevent loading the same physical file twice
            real_path = os.path.realpath(file_path)

            if real_path in loaded_paths:
                continue

            loaded_paths.add(real_path)

            extension = filename.rsplit(".", 1)[1].lower()

            try:
                if extension == "pdf":
                    text = extract_pdf(file_path)

                elif extension == "docx":
                    text = extract_docx(file_path)

                else:
                    text = extract_txt(file_path)

                documents.append({
                    "id": len(documents) + 1,
                    "name": filename,
                    "text": text
                })

                print(f"Loaded: {filename}")

            except Exception as error:
                print(f"Error loading {filename}: {error}")

    # Build one index containing all loaded documents
    index = build_inverted_index(documents)

    print(f"Loaded {len(documents)} documents successfully!")
    print(f"Indexed {len(index)} unique terms!")


# Home page
@app.route("/")
def home():
    return render_template(
        "index.html",
        documents=documents,
        index=index,
        results=[],
        query=""
    )


# Search route
@app.route("/search", methods=["GET"])
def search():

    query = request.args.get("query", "").strip()

    results = []
    search_type = "Search"
    suggestions = []

    if not query:
        return redirect(url_for("home"))

    # Phrase search
    if query.startswith('"') and query.endswith('"'):

        results = phrase_search(
            query[1:-1], index, documents
        )

        search_type = "Phrase Search"

    # Wildcard search
    elif "*" in query:

        results = wildcard_search(
            query, index, documents
        )

        search_type = "Wildcard Search"

    # Ranked search
    else:

        results = rank_documents(query, documents)

        search_type = "Ranked Search"

        if not results and len(query.split()) == 1:
            suggestions = spelling_correction(query, index)

    return render_template(
        "index.html",
        documents=documents,
        index=index,
        results=results,
        query=query,
        search_type=search_type,
        suggestions=suggestions
    )


# Query expansion route
@app.route("/expand", methods=["GET"])
def expand():

    query = request.args.get("query", "").strip()

    expanded = expand_query(query)

    expanded_query = " ".join(expanded)

    results = rank_documents(expanded_query, documents)

    return render_template(
        "index.html",
        documents=documents,
        index=index,
        results=results,
        query=query,
        expanded=expanded,
        search_type="Query Expansion"
    )



# Upload document route
@app.route("/upload", methods=["POST"])
def upload():

    if "file" not in request.files:
        flash("No file selected.")
        return redirect(url_for("home"))

    file = request.files["file"]

    if file.filename == "":
        flash("Please select a document.")
        return redirect(url_for("home"))

    if not allowed_file(file.filename):
        flash("Only PDF, DOCX and TXT files are supported.")
        return redirect(url_for("home"))

    filename = secure_filename(file.filename)

    if not filename:
        flash("Invalid filename.")
        return redirect(url_for("home"))

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(file_path)

        # Reload sample documents and all uploaded documents
        load_saved_documents()

        flash(f"{filename} uploaded and indexed successfully!")

    except Exception as error:
        flash(f"Could not process document: {error}")

    return redirect(url_for("home"))


# read the searched document

# Read document with highlighted search terms
@app.route("/read/<int:doc_id>")
def read_document(doc_id):

    document = next(
        (doc for doc in documents if doc["id"] == doc_id),
        None
    )

    if document is None:
        return "Document not found", 404

    query = request.args.get("query", "").strip()

    # Escape document text to prevent HTML injection
    safe_text = html.escape(document["text"])

    # Highlight the searched phrase
        # Highlight all occurrences of the searched phrase
    if query:
        pattern = re.escape(html.escape(query))

        first_match = True

        def highlight_match(match):
            nonlocal first_match

            if first_match:
                first_match = False
                return f'<mark id="first-highlight">{match.group(0)}</mark>'

            return f'<mark>{match.group(0)}</mark>'

        highlighted_text = re.sub(
            pattern,
            highlight_match,
            safe_text,
            flags=re.IGNORECASE
        )
    else:
        highlighted_text = safe_text

        
    return render_template(
        "read_document.html",
        document=document,
        highlighted_text=Markup(highlighted_text),
        query=query
    )



# Load documents when the application starts.
# This also runs when Gunicorn imports the app on Render.
load_saved_documents()


if __name__ == "__main__":
    app.run(debug=True)
