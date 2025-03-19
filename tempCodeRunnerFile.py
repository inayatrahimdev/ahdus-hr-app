from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_socketio import SocketIO
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import hashlib
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app)

# Connect to MongoDB (local instance)
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/ahdus_hr_app"))
db = client["ahdus_hr_app"]
jobs_collection = db["jobs"]
applications_collection = db["applications"]

# Directory for storing CVs
UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Simulate blockchain verification using SHA-256 hash
def simulate_blockchain_verification(file_content):
    hasher = hashlib.sha256()
    hasher.update(file_content)
    return hasher.hexdigest()

# Validate file type (only allow PDFs)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

# Routes for HTML pages
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

# API Routes (unchanged)
@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    jobs = list(jobs_collection.find({}, {"_id": 0}))
    return jsonify(jobs)

@app.route("/api/jobs", methods=["POST"])
def add_job():
    job_data = request.json
    jobs_collection.insert_one(job_data)
    socketio.emit("new_job", job_data)  # Real-time notification
    return jsonify({"message": "Job added successfully!"}), 201

@app.route("/api/applications", methods=["POST"])
def submit_application():
    try:
        # Check if the required fields are present
        if "name" not in request.form or "email" not in request.form or "jobId" not in request.form:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if a file is uploaded
        if "cv" not in request.files:
            return jsonify({"error": "No CV file uploaded"}), 400

        cv_file = request.files["cv"]

        # Validate file type
        if not allowed_file(cv_file.filename):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        # Generate a unique filename for the CV
        filename = f"cv_{uuid.uuid4()}_{cv_file.filename}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save the file locally
        cv_file.save(file_path)

        # Simulate blockchain verification
        cv_file.seek(0)  # Reset file pointer to the beginning
        file_content = cv_file.read()
        cv_hash = simulate_blockchain_verification(file_content)

        # Construct the application data
        application = {
            "jobId": request.form["jobId"],
            "name": request.form["name"],
            "email": request.form["email"],
            "cvPath": file_path,
            "cvHash": cv_hash,
            "appliedAt": request.form.get("appliedAt", datetime.utcnow().isoformat())
        }

        # Insert the application into the database
        applications_collection.insert_one(application)

        # Emit a real-time notification
        socketio.emit("new_application", application)

        return jsonify({"message": "Application submitted successfully!", "cvPath": file_path, "cvHash": cv_hash}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# WebSocket Event for Real-Time Updates
@socketio.on("connect")
def handle_connect():
    print("Client connected")

if __name__ == "__main__":
    # Create indexes for faster queries
    jobs_collection.create_index([("title", 1), ("location", 1)])
    applications_collection.create_index([("jobId", 1), ("appliedAt", -1)])
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)