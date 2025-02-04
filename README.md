# AI Based Road Lane Detection Project
## Project Overview
The Road Lane Detection project aims to develop an AI-powered system that enhances road safety, optimizes driver training, and supports infrastructure management. The project focuses on three primary use cases:
- **Driving Training System:** Provides real-time feedback and performance tracking to improve lane-keeping skills and reduce accidents.
- **Low-Cost Smart Dashcam:** Integrates lane detection technology into affordable dashcams for real-time alerts and safety reporting.
- **Road Infrastructure Assessment:** Monitors road conditions to identify issues like faded or missing lane markings, offering actionable insights for maintenance.
## Project Status
This project is currently in the second week of the Sprint 0 development cycle.
## Key Components
- **README.md:** Contains the project overview and documentation.
- **orchestrator.ipynb:** A notebook that reads datasets from the data-collection folder and/or database, then saves intermediate files such as trained models and configurations.
- **data-collection:** Folder with datasets used for training the lane detection models.
- **training:** Folder with scripts and notebooks for model training.
- **dev:** Folder including development scripts (e.g., `dev-run-v0.py`).
- **documentation:** Folder containing additional project documentation.
## CI/CD Plan
The project follows a SCRUM-based approach with incremental sprint releases. Each cycle includes:
1. **Code Review:** The team reviews recent code changes to ensure they meet the project requirements.
2. **Sprint-N Merge:** Approved changes are merged into the main branch.
3. **Main Deployment:** After successful testing on the staging server, changes are deployed to the production server.