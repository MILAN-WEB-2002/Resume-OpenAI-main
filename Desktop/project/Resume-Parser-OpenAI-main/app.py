# -------- app.py --------
import os
import json
import sys
from flask import Flask, request, render_template
from pypdf import PdfReader
from resumeparser import ats_extractor   # ← now uses the refactored code above

sys.path.insert(0, os.path.abspath(os.getcwd()))

UPLOAD_DIR = "__DATA__"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", data=None)


@app.route("/process", methods=["POST"])
def process_pdf():
    pdf_file = request.files.get("pdf_doc")
    if not pdf_file or pdf_file.filename == "":
        return render_template("index.html", data={"error": "No file uploaded."})

    local_path = os.path.join(UPLOAD_DIR, "uploaded.pdf")
    pdf_file.save(local_path)

    # extract text → parse via OpenRouter
    resume_text = _extract_text(local_path)
    json_result = ats_extractor(resume_text)

    return render_template("index.html", data=json.loads(json_result))


def _extract_text(path: str) -> str:
    reader, content = PdfReader(path), []
    for page in reader.pages:
        content.append(page.extract_text() or "")
    return "\n".join(content)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
