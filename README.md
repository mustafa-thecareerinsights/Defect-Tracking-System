# Defect Tracking System

> **Software Quality Engineer Project Assignment**  
> **Prepared by:** Ruknuddin Asrari  
> **Role:** Software Quality Engineer  
> **Department:** IT Software Development  
> **Email:** ruknuddin.asrari@thecareerinsights.com  
> **Organization:** The Career Insights Hub LLC  
> **Copyright:** © 2026 Ruknuddin Asrari

## Overview

This is a structured defect management web application built with Python and Flask. It helps QA teams log, track, search, update, and report software bugs for a Student Registration System.

The application meets the assignment requirements by supporting Bug IDs, severity and priority levels, defect status lifecycle, search by ID/status, and defect summary reports.

## Key Features

| Feature | Description |
|---|---|
| Defect Logging | Create defects with auto-generated Bug IDs such as `BUG-001` |
| Severity Levels | Critical, High, Medium, Low |
| Priority Levels | High, Medium, Low |
| Status Workflow | Open, In Progress, Resolved, Closed |
| Search and Filters | Search by Bug ID, title, module, or description; filter by status, severity, and module |
| Detail View | View full defect details, steps to reproduce, expected result, actual result, and comments |
| Edit Defects | Update severity, priority, status, ownership, and notes |
| Summary Reports | Report breakdown by status, severity, priority, and module |
| Open Critical Panel | Highlights unresolved critical issues requiring immediate attention |
| CSV Export | Download all defects through `/export.csv` |
| REST API | View all defects as JSON through `/api/defects` |

## Project Structure

```text
Defect-Tracking-System-Ruknuddin-Asrari/
├── app.py
├── defects.json
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   └── styles.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add.html
│   ├── edit.html
│   ├── view.html
│   └── report.html
└── screenshots/
    ├── dashboard.png
    ├── add_defect.png
    ├── defect_detail.png
    └── report.png
```

## Installation and Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/mustafa-thecareerinsights/Defect-Tracking-System.git
cd Defect-Tracking-System/Defect-Tracking-System-Ruknuddin-Asrari
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open this URL in your browser:

```text
http://localhost:5050
```

## Application Routes

| Route | Purpose |
|---|---|
| `/` | Dashboard with summary cards, search, filters, and defect register |
| `/add` | Log a new defect |
| `/view/<BUG-ID>` | View full defect details |
| `/edit/<BUG-ID>` | Edit an existing defect |
| `/report` | Defect summary reports |
| `/api/defects` | JSON API output |
| `/export.csv` | Download CSV report |

## Sample Seed Data

The project starts with ten sample defects covering common Student Registration System test scenarios, including login validation, duplicate signup, course enrollment, profile update, and admin access control defects.

| Bug ID | Module | Severity | Status |
|---|---|---|---|
| BUG-001 | Login | Critical | Open |
| BUG-002 | Login | High | In Progress |
| BUG-003 | Student Signup | Critical | Resolved |
| BUG-004 | Student Signup | High | Open |
| BUG-005 | Course Enrollment | High | Open |
| BUG-006 | Login | High | In Progress |
| BUG-007 | Admin Dashboard | Critical | Open |
| BUG-008 | Profile Update | Medium | Closed |
| BUG-009 | Course Enrollment | Critical | In Progress |
| BUG-010 | Profile Update | Medium | Resolved |

## Validation and Design Decisions

- Frontend and backend validation require a title before a defect is saved.
- Dropdown values are restricted to valid severity, priority, module, and status lists.
- Bug IDs are auto-incremented and use the `BUG-###` format.
- Defects are stored in a portable JSON file to keep the assignment easy to review without database setup.
- Delete uses a POST request with confirmation to avoid accidental deletions from direct URL clicks.
- The footer clearly includes authorship and copyright details for Ruknuddin Asrari.

## Author

Prepared by **Ruknuddin Asrari**  
Software Quality Engineer  
The Career Insights Hub LLC  
© 2026 Ruknuddin Asrari. All rights reserved.
