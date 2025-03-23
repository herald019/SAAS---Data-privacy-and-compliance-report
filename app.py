from flask import Flask, request, render_template, redirect, url_for
import boto3
import os
import json

app = Flask(__name__)

# S3 Bucket Configurations
CSV_BUCKET = "hackathonwin"
JSON_BUCKET = "macie-job-exports"
JSON_PREFIX = "macie-findings/"  # Folder where JSON files are stored

s3 = boto3.client("s3")

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles CSV file upload and redirects to buffer page before result"""
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    file_name, file_extension = os.path.splitext(file.filename)
    
    if file_extension.lower() != ".csv":
        return "Only CSV files are allowed", 400

    # Upload CSV to the hackathon bucket
    s3.upload_fileobj(file, CSV_BUCKET, file.filename)

    # Redirect to buffer page before fetching JSON file
    return redirect(url_for("buffer"))

@app.route("/buffer")
def buffer():
    """Temporary buffer page before showing result"""
    return render_template("buffer.html", result_url=url_for("result"))

@app.route("/result")
def result():
    """Fetches a JSON file and displays compliance details"""
    try:
        json_data, json_file_key = fetch_json_from_s3()

        if json_data is None:
            return "No compliance report found", 404

        # Extract necessary compliance details
        compliance_details = extract_compliance_details(json_data)

        # Generate a pre-signed URL for downloading the JSON file
        json_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": JSON_BUCKET, "Key": json_file_key},
            ExpiresIn=3600,  # Link expires in 1 hour
        )

        return render_template("result.html", compliance=compliance_details, file_url=json_url)

    except Exception as e:
        print(f"Error fetching JSON file: {e}")
        return "Error fetching JSON file or file not found", 500

def fetch_json_from_s3():
    """Fetches JSON file from S3 and parses it."""
    try:
        response = s3.list_objects_v2(Bucket=JSON_BUCKET, Prefix=JSON_PREFIX)

        if "Contents" not in response or not response["Contents"]:
            print("No JSON file found in S3!")
            return None, None

        json_file_key = response["Contents"][0]["Key"]

        json_object = s3.get_object(Bucket=JSON_BUCKET, Key=json_file_key)
        json_content = json_object["Body"].read().decode("utf-8")

        parsed_json = json.loads(json_content)
        return parsed_json, json_file_key

    except Exception as e:
        print(f"Error fetching JSON file: {e}")
        return None, None

def extract_compliance_details(json_data):
    """Extracts relevant compliance details from JSON report."""
    report = json_data[0]  # Access the first object in the JSON list

    compliance_details = {
        "Risk Level": report.get("severity", {}).get("description", "Unknown"),
        "Category": report.get("category", "Unknown"),
        "Type of Sensitivity": ", ".join(
            [sensitive_data["category"] for sensitive_data in report.get("classificationDetails", {}).get("result", {}).get("sensitiveData", [])]
        ) if report.get("classificationDetails", {}).get("result", {}).get("sensitiveData") else "None",
        "Findings Count": report.get("count", 0),
        "Description": report.get("description", "No description available"),
        "Last Updated": report.get("updatedAt", "Unknown"),
    }
    
    return compliance_details

if __name__ == "__main__":
    app.run(debug=True)
