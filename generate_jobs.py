from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["ahdus_hr_app"]
jobs_collection = db["jobs"]

# Curated list of professional jobs for Ahdus Technology (German market focus)
trending_jobs = [
    {
        "title": "Senior Software Engineer",
        "location": "Berlin",
        "skills_required": ["Python", "Django", "AWS"],
        "company": "Ahdus Technology",
        "salary": "€70,000 - €90,000",
        "type": "Full-Time",
        "description": "Lead the development of scalable web applications using Python and AWS. Collaborate with cross-functional teams to deliver high-quality software solutions."
    },
    {
        "title": "Data Scientist",
        "location": "Munich",
        "skills_required": ["Python", "Pandas", "Machine Learning"],
        "company": "Ahdus Technology",
        "salary": "€65,000 - €85,000",
        "type": "Full-Time",
        "description": "Analyze large datasets to derive actionable insights. Build predictive models to enhance business decision-making."
    },
    {
        "title": "Frontend Developer",
        "location": "Hamburg",
        "skills_required": ["React", "TypeScript", "CSS"],
        "company": "Ahdus Technology",
        "salary": "€55,000 - €75,000",
        "type": "Full-Time",
        "description": "Design and implement responsive, user-friendly interfaces for enterprise-grade web applications."
    },
    {
        "title": "DevOps Engineer",
        "location": "Frankfurt",
        "skills_required": ["Docker", "Kubernetes", "Terraform"],
        "company": "Ahdus Technology",
        "salary": "€70,000 - €95,000",
        "type": "Full-Time",
        "description": "Optimize CI/CD pipelines and manage cloud infrastructure to ensure seamless deployment and scalability."
    },
    {
        "title": "Cloud Architect",
        "location": "Stuttgart",
        "skills_required": ["AWS", "Azure", "Google Cloud"],
        "company": "Ahdus Technology",
        "salary": "€80,000 - €110,000",
        "type": "Full-Time",
        "description": "Architect and oversee cloud solutions for enterprise clients, ensuring security, scalability, and performance."
    },
    {
        "title": "Cybersecurity Specialist",
        "location": "Berlin",
        "skills_required": ["Penetration Testing", "SIEM", "Python"],
        "company": "Ahdus Technology",
        "salary": "€75,000 - €100,000",
        "type": "Full-Time",
        "description": "Protect company assets by identifying vulnerabilities and implementing robust security measures."
    },
    {
        "title": "Backend Developer",
        "location": "Munich",
        "skills_required": ["Node.js", "MongoDB", "REST APIs"],
        "company": "Ahdus Technology",
        "salary": "€60,000 - €80,000",
        "type": "Full-Time",
        "description": "Develop and maintain server-side logic and APIs to support web and mobile applications."
    },
    {
        "title": "Product Manager (Tech)",
        "location": "Hamburg",
        "skills_required": ["Agile", "Scrum", "JIRA"],
        "company": "Ahdus Technology",
        "salary": "€70,000 - €90,000",
        "type": "Full-Time",
        "description": "Drive product development from ideation to launch, working closely with engineering and design teams."
    },
    {
        "title": "UI/UX Designer",
        "location": "Frankfurt",
        "skills_required": ["Figma", "Adobe XD", "Prototyping"],
        "company": "Ahdus Technology",
        "salary": "€50,000 - €70,000",
        "type": "Full-Time",
        "description": "Create intuitive and visually appealing designs for web and mobile applications."
    },
    {
        "title": "QA Engineer",
        "location": "Stuttgart",
        "skills_required": ["Selenium", "Test Automation", "Python"],
        "company": "Ahdus Technology",
        "salary": "€55,000 - €75,000",
        "type": "Full-Time",
        "description": "Ensure software quality through automated and manual testing processes."
    }
]

# Clear existing jobs and insert curated ones
jobs_collection.delete_many({})
jobs_collection.insert_many(trending_jobs)
print(f"{len(trending_jobs)} professional jobs added to the database!")