# Group Calendar Availability Planner

## Overview

This project began as a personal scheduling tool built to solve a very practical problem:  
finding shared free time between friends who all have different class schedules.

Instead of guessing availability or manually comparing calendars to plan lunches or study sessions, I wanted a simple way to visualize when people were actually free during the day. What started as a small utility quickly grew into a more complete web application and DevOps learning project.

---

## Motivation & Idea

As a student juggling multiple classes—and coordinating with friends doing the same—I noticed how inefficient it was to plan meetups. Everyone had different lecture times, labs, and commitments, which made finding overlapping free time surprisingly difficult.

This tool was created to:
- Eliminate guesswork when planning meetups
- Automatically visualize availability based on class schedules
- Make it easy to identify shared free windows for lunch, studying, or meetings

---

## Project Evolution

While the original goal was simply to generate a usable schedule visualization, the project expanded as I decided to treat it as a **real-world web application**:

- A **FastAPI backend** processes schedule data
- A lightweight **HTML frontend** displays availability
- The app is fully **containerized with Docker**
- The container is deployed using **Azure App Services**
- **CI/CD is handled with GitHub Actions**, enabling automated builds and deployments

Through this process, the project became a hands-on way to learn:
- Docker-based application packaging
- Cloud deployment using Azure
- Continuous Integration and Continuous Deployment (CI/CD) pipelines
- Practical DevOps workflows used in real production environments

---

## AI-Assisted Development

An important aspect of this project is how it was built:

- **All Python and HTML code was generated using ChatGPT (GPT-4.1)**
- I acted as the tester, debugger, and reviewer:
  - Running the code
  - Identifying bugs or design issues
  - Requesting refactors or improvements from the AI
- This iterative loop allowed me to focus on **understanding system design, debugging, and deployment**, rather than writing every line from scratch

This approach turned the project into both a learning tool and an experiment in AI-assisted software development.

---

## Technologies Used

- **Backend:** FastAPI (Python)
- **Frontend:** HTML (served as static content)
- **Containerization:** Docker
- **Cloud Platform:** Azure App Services
- **CI/CD:** GitHub Actions
- **Version Control:** Git & GitHub

---

## Key Learning Outcomes

- Designing a backend API to support a real user need
- Serving static frontend assets alongside an API
- Building and running Docker containers locally
- Deploying containerized applications to Azure
- Automating builds and deployments with GitHub Actions
- Understanding how modern DevOps workflows fit together

---

## Future Improvements

- Better UI/UX for availability visualization
- Authentication and persistent storage
- Calendar integrations (Google Calendar, Outlook, etc.)

---

## Final Notes

This project represents a progression from a **simple personal tool** into a **full-stack, cloud-deployed application**. It reflects both a practical problem-solving mindset and a deliberate effort to learn industry-relevant development and DevOps practices.

