import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request
from google.cloud import storage
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

app = Flask(__name__)

# -------------------------------------------------
# Configuration – change these values once you create them
# -------------------------------------------------
# BUCKET_NAME = "my-pdf-demo-bucket"          # Cloud Storage bucket (public)
BUCKET_NAME = "la-biblioteca-de-babel-bucket"          # Cloud Storage bucket (public)
PROJECT_ID  = os.getenv("GOOGLE_CLOUD_PROJECT")  # auto‑filled by Cloud Run
# -------------------------------------------------

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


def _create_pdf(local_path: str):
    """Very small PDF – replace with whatever you need."""
    c = canvas.Canvas(local_path, pagesize=LETTER)
    w, h = LETTER
    c.drawString(100, h - 100, "Hello from the PDF generator!")
    c.drawString(
        100,
        h - 130,
        f"Generated at {datetime.now():%Y-%m-%d %H:%M UTC}",
    )
    c.showPage()
    c.save()


@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    # 1️⃣ Create a temporary file locally
    tmp_name = f"/tmp/{uuid.uuid4()}.pdf"
    _create_pdf(tmp_name)

    # 2️⃣ Upload to Cloud Storage (make it publicly readable)
    blob_name = f"pdfs/{os.path.basename(tmp_name)}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(tmp_name)
    blob.make_public()                     # simple public URL; for prod use signed URLs

    # 3️⃣ Return the public URL
    pdf_url = blob.public_url
    return jsonify({"pdf_url": pdf_url})


if __name__ == "__main__":
    # Local testing only
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))