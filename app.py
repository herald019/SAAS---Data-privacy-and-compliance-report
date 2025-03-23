from flask import Flask, request, render_template, redirect, url_for
import boto3
import os
import time

app = Flask(__name__)

S3_BUCKET = "hackathonwin"

s3 = boto3.client("s3")

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles CSV file upload and redirects to buffer page before result"""
    if "csvFile" not in request.files:
        return "No file uploaded", 400

    file = request.files["csvFile"]
    if file.filename == "":
        return "No selected file", 400

    file_name, file_extension = os.path.splitext(file.filename)
    if file_extension.lower() != ".csv":
        return "Only CSV files are allowed", 400

    s3.upload_fileobj(file, S3_BUCKET, file.filename)

    # Redirect to buffer page before showing result
    return redirect(url_for("buffer", filename=file_name))

@app.route("/buffer")
def buffer():
    """Temporary buffer page before showing result"""
    file_name = request.args.get("filename")
    if not file_name:
        return "Invalid request", 400

    return render_template("buffer.html", filename=file_name)

@app.route("/result")
def result():
    """Renders result page after buffering"""
    file_name = request.args.get("filename")
    if not file_name:
        return "Invalid request", 400

    pdf_key = f"{file_name}.pdf"
    pdf_url = generate_presigned_url(pdf_key)

    return render_template("result.html", file_name=file_name, pdf_url=pdf_url)

def generate_presigned_url(file_key):
    """Generate a pre-signed URL for downloading the PDF from S3"""
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": file_key},
            ExpiresIn=3600,
        )
        return url
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
