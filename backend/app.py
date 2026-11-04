
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import pymupdf
from docx import Document
from algorithms.inverted_index import build_inverted_index
from algorithms.boolean_retrieval import boolean_search
from algorithms.ranking import rank_documents
from algorithms.phrase_search import phrase_search

from algorithms.tolerant_retrieval import (
    wildcard_search,
    spelling_correction
)

from algorithms.query_expansion import expand_query

from algorithms.evaluation import calculate_metrics

metrics = calculate_metrics(
    relevant_documents=[1, 2, 3],
    retrieved_documents=[1, 2, 4]
)

print(metrics)





app = Flask(__name__)
app.secret_key = "mini-search-engine-secret"

# Folder where uploaded documents will be stored
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Temporary document collection
documents = []

# Store inverted index
index = {}



def load_saved_documents():
    global index

    documents.clear()

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    for filename in sorted(os.listdir(app.config["UPLOAD_FOLDER"])):

        if not allowed_file(filename):
            continue

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"], filename
        )

        if not os.path.isfile(file_path):
            continue

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

        except Exception as error:
            print(f"Error loading {filename}: {error}")

    index = build_inverted_index(documents)

    print(f"Loaded {len(documents)} documents successfully!")
    print(f"Indexed {len(index)} unique terms!")



# Check whether the file format is supported
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Extract text from PDF
def extract_pdf(file_path):
    text = ""

    pdf = pymupdf.open(file_path)

    for page in pdf:
        text += page.get_text() + "\n"

    pdf.close()
    return text


# Extract text from DOCX
def extract_docx(file_path):
    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)


# Extract text from TXT
def extract_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        return file.read()


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


# search route

@app.route("/search", methods=["GET"])
def search():

    query = request.args.get("query", "").strip()

    results = []
    search_type = "Search"
    suggestions = []

    if query.startswith('"') and query.endswith('"'):

        results = phrase_search(
            query[1:-1], index, documents
        )
        search_type = "Phrase Search"

    elif "*" in query:

        results = wildcard_search(
            query, index, documents
        )
        search_type = "Wildcard Search"

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


    # expand route
    @app.route("/expand")
    def expand():

        query = request.args.get("query", "")

        expanded = expand_query(query)

        return render_template(
            "index.html",
            documents=documents,
            index=index,
            results=[],
            query=query,
            expanded=expanded,
            search_type="Query Expansion"
        )




# Upload document
@app.route("/upload", methods=["POST"])
def upload():
    global index

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
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(file_path)

    extension = filename.rsplit(".", 1)[1].lower()

    try:
        if extension == "pdf":
            extracted_text = extract_pdf(file_path)

        elif extension == "docx":
            extracted_text = extract_docx(file_path)

        else:
            extracted_text = extract_txt(file_path)

        documents.append({
            "id": len(documents) + 1,
            "name": filename,
            "text": extracted_text
        })

        # Rebuild inverted index after every upload
        index = build_inverted_index(documents)

        flash(f"{filename} uploaded and processed successfully!")

    except Exception as error:
        flash(f"Could not process document: {error}")

    return redirect(url_for("home"))



@app.route("/expand", methods=["GET"])
def expand():

    query = request.args.get("query", "").strip()

    expanded = expand_query(query)

    # Search using all expanded terms
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



if __name__ == "__main__":
    load_saved_documents()
    app.run(debug=True)
