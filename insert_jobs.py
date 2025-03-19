from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ahdus_hr_app"]
jobs_collection = db["jobs"]

# Define a list of trending jobs for the German market
trending_jobs = [
    {"title": "Software Engineer", "location": "Berlin", "skills_required": ["Python", "Flask", "Django"], "company": "TechCorp", "salary": "€60,000 - €80,000"},
    {"title": "Data Analyst", "location": "Munich", "skills_required": ["SQL", "Excel", "Power BI"], "company": "DataSolutions", "salary": "€50,000 - €70,000"},
    {"title": "AI Specialist", "location": "Frankfurt", "skills_required": ["TensorFlow", "PyTorch", "Machine Learning"], "company": "AI Innovations", "salary": "€70,000 - €90,000"},
    {"title": "DevOps Engineer", "location": "Hamburg", "skills_required": ["Docker", "Kubernetes", "CI/CD"], "company": "CloudTech", "salary": "€65,000 - €85,000"},
    {"title": "Frontend Developer", "location": "Stuttgart", "skills_required": ["React", "JavaScript", "HTML/CSS"], "company": "WebWorks", "salary": "€55,000 - €75,000"},
    # Add more jobs here...
]

# Generate 1000+ jobs dynamically
def generate_jobs():
    locations = ["Berlin", "Munich", "Frankfurt", "Hamburg", "Stuttgart"]
    companies = ["TechCorp", "DataSolutions", "AI Innovations", "CloudTech", "WebWorks"]
    job_titles = ["Software Engineer", "Data Analyst", "AI Specialist", "DevOps Engineer", "Frontend Developer"]
    skills = [["Python", "Flask", "Django"], ["SQL", "Excel", "Power BI"], ["TensorFlow", "PyTorch", "Machine Learning"], ["Docker", "Kubernetes", "CI/CD"], ["React", "JavaScript", "HTML/CSS"]]
    salaries = ["€60,000 - €80,000", "€50,000 - €70,000", "€70,000 - €90,000", "€65,000 - €85,000", "€55,000 - €75,000"]

    jobs = []
    for i in range(1000):
        job = {
            "title": job_titles[i % len(job_titles)],
            "location": locations[i % len(locations)],
            "skills_required": skills[i % len(skills)],
            "company": companies[i % len(companies)],
            "salary": salaries[i % len(salaries)]
        }
        jobs.append(job)
    return jobs

# Clear existing jobs and insert new ones
jobs_collection.delete_many({})
jobs_collection.insert_many(generate_jobs())
print("1000+ jobs added to the database!")