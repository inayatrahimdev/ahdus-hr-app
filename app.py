from flask import Flask, jsonify, request, render_template, send_from_directory
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import hashlib
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB (ensure correct connection string for Vercel)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ahdus_hr_app")
client = MongoClient(MONGO_URI)
db = client["ahdus_hr_app"]
jobs_collection = db["jobs"]
applications_collection = db["applications"]

# Directory for storing CVs
UPLOAD_FOLDER = os.path.join(app.root_path, "static/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Blockchain-like file verification
def simulate_blockchain_verification(file_content):
    return hashlib.sha256(file_content).hexdigest()

# Allowed file types
def allowed_file(filename):
    return filename.lower().endswith(".pdf")

# HTML Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about-us")
def about_us():
    return render_template("about-us.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/careers")
def careers():
    return render_template("careers.html")

@app.route("/contact-us")
def contact_us():
    return render_template("contact-us.html")

# API Routes
@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    jobs = list(jobs_collection.find({}, {"_id": 0}))
    return jsonify(jobs)

@app.route("/api/jobs", methods=["POST"])
def add_job():
    job_data = request.json
    jobs_collection.insert_one(job_data)
    return jsonify({"message": "Job added successfully!"}), 201

@app.route("/api/applications", methods=["POST"])
def submit_application():
    try:
        if "name" not in request.form or "email" not in request.form or "jobId" not in request.form:
            return jsonify({"error": "Missing required fields"}), 400

        if "cv" not in request.files:
            return jsonify({"error": "No CV file uploaded"}), 400

        cv_file = request.files["cv"]
        if not allowed_file(cv_file.filename):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        filename = f"cv_{uuid.uuid4()}_{cv_file.filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        cv_file.save(file_path)

        cv_file.seek(0)
        file_content = cv_file.read()
        cv_hash = simulate_blockchain_verification(file_content)

        application = {
            "jobId": request.form["jobId"],
            "name": request.form["name"],
            "email": request.form["email"],
            "cvPath": filename,
            "cvHash": cv_hash,
            "appliedAt": datetime.utcnow().isoformat()
        }

        applications_collection.insert_one(application)

        return jsonify({"message": "Application submitted successfully!", "cvPath": file_path, "cvHash": cv_hash}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve uploaded CVs
@app.route("/static/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
