let jobs = [];

// Fetch jobs from the backend
async function fetchJobs() {
    try {
        const response = await fetch("/api/jobs");
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        jobs = await response.json();
        console.log("Jobs fetched:", jobs); // Debug log
        renderJobs(jobs);
    } catch (error) {
        console.error("Error fetching jobs:", error);
        document.getElementById("loading").textContent = "Failed to load job opportunities.";
    }
}

// Render jobs to the DOM with Apply button
function renderJobs(filteredJobs) {
    const container = document.getElementById("jobs-container");
    container.innerHTML = "";

    if (filteredJobs.length === 0) {
        container.innerHTML = "<p>No jobs found.</p>";
        return;
    }

    filteredJobs.forEach((job, index) => {
        const jobCard = document.createElement("div");
        jobCard.classList.add("job-card");
        jobCard.innerHTML = `
            <h3>${job.title}</h3>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Skills Required:</strong> ${job.skills_required.join(", ")}</p>
            <p><strong>Salary:</strong> ${job.salary}</p>
            <p><strong>Type:</strong> ${job.type}</p>
            <p class="description">${job.description}</p>
            <button class="apply-btn" onclick="openApplyModal(${index})">Apply Now</button>
        `;
        container.appendChild(jobCard);
    });

    document.getElementById("loading").style.display = "none";
}

// Filter jobs based on search query
function filterJobs() {
    const searchQuery = document.getElementById("search").value.toLowerCase();
    const filteredJobs = jobs.filter(job =>
        job.title.toLowerCase().includes(searchQuery) ||
        job.location.toLowerCase().includes(searchQuery) ||
        job.company.toLowerCase().includes(searchQuery) ||
        job.skills_required.some(skill => skill.toLowerCase().includes(searchQuery))
    );
    renderJobs(filteredJobs);
}

// Job Application Modal
function openApplyModal(jobIndex) {
    const modal = document.getElementById("apply-modal");
    modal.style.display = "block";

    const form = document.getElementById("apply-form");
    form.onsubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        formData.append("jobId", jobs[jobIndex].title); // Use job title as jobId

        try {
            const response = await fetch("/api/applications", {
                method: "POST",
                body: formData
            });
            const result = await response.json();
            if (response.ok) {
                alert("Application submitted successfully! CV saved to /static/uploads.");
                modal.style.display = "none";
                form.reset();
            } else {
                alert("Failed to submit application: " + result.error);
            }
        } catch (error) {
            console.error("Error submitting application:", error);
            alert("Error submitting application. Check console for details.");
        }
    };
}

// Close Modal
document.querySelector(".close").addEventListener("click", () => {
    document.getElementById("apply-modal").style.display = "none";
});

// Hamburger Menu Toggle
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
hamburger.addEventListener("click", () => {
    navMenu.classList.toggle("active");
    hamburger.classList.toggle("active");
});

// Initialize the app
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded, fetching jobs..."); // Debug log
    fetchJobs();
});