"""
Defect Tracking System
Prepared by: Ruknuddin Asrari
Role: Software Quality Engineer
Department: IT Software Development
Organization: The Career Insights Hub LLC

A lightweight Flask application for logging, searching, updating, and reporting software defects.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os
import re
from typing import Any

from flask import Flask, Response, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("DTS_SECRET_KEY", "dts-ruknuddin-asrari-demo-key")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "defects.json")

MODULES = ["Login", "Student Signup", "Course Enrollment", "Profile Update", "Admin Dashboard", "Other"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
PRIORITIES = ["High", "Medium", "Low"]
STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

SEED_DEFECTS: list[dict[str, Any]] = [
    {
        "id": "BUG-001",
        "title": "Login accepted with invalid password",
        "description": "System allows login with an incorrect password and creates an authenticated session.",
        "module": "Login",
        "severity": "Critical",
        "priority": "High",
        "status": "Open",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Open login page\n2. Enter valid email\n3. Enter incorrect password\n4. Click Login",
        "expected_result": "System should reject the login attempt and display an authentication error.",
        "actual_result": "User is logged in successfully with an invalid password.",
        "date_reported": "2026-03-10",
        "date_updated": "2026-03-10",
        "comments": "P1 issue because authentication validation is failing.",
    },
    {
        "id": "BUG-002",
        "title": "Account lockout not triggered after five failed attempts",
        "description": "No lockout or throttling occurs after repeated incorrect password attempts.",
        "module": "Login",
        "severity": "High",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Attempt login five times with wrong password\n2. Attempt sixth login immediately",
        "expected_result": "Account should be locked or throttled after the configured failed-attempt limit.",
        "actual_result": "The system continues accepting unlimited attempts.",
        "date_reported": "2026-03-10",
        "date_updated": "2026-03-12",
        "comments": "Security validation needed for brute-force protection.",
    },
    {
        "id": "BUG-003",
        "title": "Duplicate email accepted during student signup",
        "description": "The signup form allows creating more than one student account with the same email address.",
        "module": "Student Signup",
        "severity": "Critical",
        "priority": "High",
        "status": "Resolved",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Register using an existing email\n2. Submit the form",
        "expected_result": "System should reject duplicate email and show a clear validation message.",
        "actual_result": "A duplicate account is created.",
        "date_reported": "2026-03-10",
        "date_updated": "2026-03-14",
        "comments": "Unique constraint added; pending regression verification.",
    },
    {
        "id": "BUG-004",
        "title": "Weak password accepted during registration",
        "description": "Passwords such as 123456 are accepted during signup.",
        "module": "Student Signup",
        "severity": "High",
        "priority": "High",
        "status": "Open",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Open signup page\n2. Enter password 123456\n3. Submit registration",
        "expected_result": "System should enforce minimum password complexity rules.",
        "actual_result": "Weak password is accepted.",
        "date_reported": "2026-03-10",
        "date_updated": "2026-03-10",
        "comments": "Frontend and backend validation required.",
    },
    {
        "id": "BUG-005",
        "title": "Student can enroll in the same course multiple times",
        "description": "Duplicate enrollments are saved for the same student-course pair.",
        "module": "Course Enrollment",
        "severity": "High",
        "priority": "High",
        "status": "Open",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Enroll in a course\n2. Return to course page\n3. Click Enroll again",
        "expected_result": "System should prevent duplicate enrollment.",
        "actual_result": "Multiple enrollment records are created.",
        "date_reported": "2026-03-11",
        "date_updated": "2026-03-11",
        "comments": "Missing unique validation on enrollment records.",
    },
    {
        "id": "BUG-006",
        "title": "Session persists after logout when browser back button is used",
        "description": "After logout, pressing browser Back displays authenticated dashboard content.",
        "module": "Login",
        "severity": "High",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Login successfully\n2. Logout\n3. Press browser Back button",
        "expected_result": "Dashboard should not be accessible after logout.",
        "actual_result": "Dashboard content is visible again.",
        "date_reported": "2026-03-11",
        "date_updated": "2026-03-13",
        "comments": "Add server-side session invalidation and cache-control headers.",
    },
    {
        "id": "BUG-007",
        "title": "Student accesses Admin Dashboard through direct URL",
        "description": "A student role user can open the admin dashboard directly by entering the URL.",
        "module": "Admin Dashboard",
        "severity": "Critical",
        "priority": "High",
        "status": "Open",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Login as student\n2. Navigate directly to /admin/dashboard",
        "expected_result": "System should block access with an authorization error.",
        "actual_result": "Admin dashboard opens for student user.",
        "date_reported": "2026-03-11",
        "date_updated": "2026-03-11",
        "comments": "Critical RBAC defect; server-side access control required.",
    },
    {
        "id": "BUG-008",
        "title": "Profile saves with empty Last Name field",
        "description": "The system stores a blank Last Name value without backend validation.",
        "module": "Profile Update",
        "severity": "Medium",
        "priority": "Medium",
        "status": "Closed",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Edit profile\n2. Clear Last Name\n3. Save profile",
        "expected_result": "Last Name should remain required.",
        "actual_result": "Blank value is saved.",
        "date_reported": "2026-03-12",
        "date_updated": "2026-03-15",
        "comments": "Verified fixed and closed.",
    },
    {
        "id": "BUG-009",
        "title": "Enrollment in full course causes negative seat count",
        "description": "Enrollment proceeds even when course capacity is zero.",
        "module": "Course Enrollment",
        "severity": "Critical",
        "priority": "High",
        "status": "In Progress",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Set course capacity to zero\n2. Attempt enrollment\n3. Review remaining seat count",
        "expected_result": "System should block enrollment when no seats are available.",
        "actual_result": "Enrollment succeeds and seat count becomes negative.",
        "date_reported": "2026-03-12",
        "date_updated": "2026-03-14",
        "comments": "Likely race condition and missing capacity validation.",
    },
    {
        "id": "BUG-010",
        "title": "Oversized profile photo upload accepted",
        "description": "Files larger than the 5 MB limit upload successfully without an error message.",
        "module": "Profile Update",
        "severity": "Medium",
        "priority": "Medium",
        "status": "Resolved",
        "assigned_to": "Development Team",
        "reported_by": "Ruknuddin Asrari",
        "steps_to_reproduce": "1. Open profile photo upload\n2. Upload a 15 MB image\n3. Save profile",
        "expected_result": "System should reject files over 5 MB.",
        "actual_result": "Oversized image uploads successfully.",
        "date_reported": "2026-03-12",
        "date_updated": "2026-03-15",
        "comments": "Server-side size validation added; pending final retest.",
    },
]


def today() -> str:
    return dt.date.today().isoformat()


def load_defects() -> list[dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        save_defects(SEED_DEFECTS)
    with open(DATA_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_defects(defects: list[dict[str, Any]]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as handle:
        json.dump(defects, handle, indent=2)


def next_bug_id(defects: list[dict[str, Any]]) -> str:
    numbers = []
    for defect in defects:
        match = re.fullmatch(r"BUG-(\d{3,})", defect.get("id", ""))
        if match:
            numbers.append(int(match.group(1)))
    return f"BUG-{(max(numbers) + 1) if numbers else 1:03d}"


def clean_choice(value: str | None, allowed: list[str], default: str) -> str:
    return value if value in allowed else default


def build_defect_from_form(form: Any, existing: dict[str, Any] | None = None) -> dict[str, Any]:
    now = today()
    base = existing.copy() if existing else {}
    title = form.get("title", "").strip()
    base.update(
        {
            "title": title,
            "description": form.get("description", "").strip(),
            "module": clean_choice(form.get("module"), MODULES, "Other"),
            "severity": clean_choice(form.get("severity"), SEVERITIES, "Medium"),
            "priority": clean_choice(form.get("priority"), PRIORITIES, "Medium"),
            "status": clean_choice(form.get("status"), STATUSES, "Open"),
            "assigned_to": form.get("assigned_to", "").strip(),
            "reported_by": form.get("reported_by", "Ruknuddin Asrari").strip() or "Ruknuddin Asrari",
            "steps_to_reproduce": form.get("steps_to_reproduce", "").strip(),
            "expected_result": form.get("expected_result", "").strip(),
            "actual_result": form.get("actual_result", "").strip(),
            "comments": form.get("comments", "").strip(),
            "date_updated": now,
        }
    )
    if "date_reported" not in base:
        base["date_reported"] = now
    return base


def summarize(defects: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total": len(defects),
        "by_status": {status: sum(1 for d in defects if d["status"] == status) for status in STATUSES},
        "by_severity": {severity: sum(1 for d in defects if d["severity"] == severity) for severity in SEVERITIES},
        "by_priority": {priority: sum(1 for d in defects if d["priority"] == priority) for priority in PRIORITIES},
        "by_module": {module: sum(1 for d in defects if d["module"] == module) for module in MODULES},
        "open_critical": [d for d in defects if d["severity"] == "Critical" and d["status"] not in {"Resolved", "Closed"}],
    }


@app.route("/")
def index() -> str:
    defects = load_defects()
    query = request.args.get("q", "").strip().lower()
    status = request.args.get("status", "")
    severity = request.args.get("severity", "")
    module = request.args.get("module", "")

    filtered = defects
    if query:
        filtered = [
            d
            for d in filtered
            if query in d["id"].lower()
            or query in d["title"].lower()
            or query in d.get("description", "").lower()
            or query in d.get("module", "").lower()
        ]
    if status:
        filtered = [d for d in filtered if d["status"] == status]
    if severity:
        filtered = [d for d in filtered if d["severity"] == severity]
    if module:
        filtered = [d for d in filtered if d["module"] == module]

    stats = summarize(defects)
    return render_template(
        "index.html",
        defects=filtered,
        stats=stats,
        modules=MODULES,
        severities=SEVERITIES,
        priorities=PRIORITIES,
        statuses=STATUSES,
        q=query,
        status=status,
        severity=severity,
        module=module,
    )


@app.route("/add", methods=["GET", "POST"])
def add() -> str | Response:
    if request.method == "POST":
        defects = load_defects()
        if not request.form.get("title", "").strip():
            flash("Title is required before a defect can be logged.", "error")
            return redirect(url_for("add"))
        defect = build_defect_from_form(request.form)
        defect["id"] = next_bug_id(defects)
        defects.append(defect)
        save_defects(defects)
        flash(f"{defect['id']} logged successfully.", "success")
        return redirect(url_for("view", bug_id=defect["id"]))
    return render_template("add.html", modules=MODULES, severities=SEVERITIES, priorities=PRIORITIES)


@app.route("/view/<bug_id>")
def view(bug_id: str) -> str | Response:
    defect = next((d for d in load_defects() if d["id"] == bug_id), None)
    if defect is None:
        flash(f"{bug_id} was not found.", "error")
        return redirect(url_for("index"))
    return render_template("view.html", defect=defect)


@app.route("/edit/<bug_id>", methods=["GET", "POST"])
def edit(bug_id: str) -> str | Response:
    defects = load_defects()
    defect = next((d for d in defects if d["id"] == bug_id), None)
    if defect is None:
        flash(f"{bug_id} was not found.", "error")
        return redirect(url_for("index"))
    if request.method == "POST":
        if not request.form.get("title", "").strip():
            flash("Title is required before saving changes.", "error")
            return redirect(url_for("edit", bug_id=bug_id))
        defect.update(build_defect_from_form(request.form, existing=defect))
        save_defects(defects)
        flash(f"{bug_id} updated successfully.", "success")
        return redirect(url_for("view", bug_id=bug_id))
    return render_template(
        "edit.html",
        defect=defect,
        modules=MODULES,
        severities=SEVERITIES,
        priorities=PRIORITIES,
        statuses=STATUSES,
    )


@app.route("/delete/<bug_id>", methods=["POST"])
def delete(bug_id: str) -> Response:
    defects = load_defects()
    remaining = [d for d in defects if d["id"] != bug_id]
    if len(remaining) == len(defects):
        flash(f"{bug_id} was not found.", "error")
    else:
        save_defects(remaining)
        flash(f"{bug_id} deleted successfully.", "success")
    return redirect(url_for("index"))


@app.route("/report")
def report() -> str:
    defects = load_defects()
    return render_template("report.html", defects=defects, stats=summarize(defects), statuses=STATUSES, severities=SEVERITIES)


@app.route("/api/defects")
def api_defects() -> Response:
    return jsonify(load_defects())


@app.route("/export.csv")
def export_csv() -> Response:
    defects = load_defects()
    fields = [
        "id",
        "title",
        "module",
        "severity",
        "priority",
        "status",
        "assigned_to",
        "reported_by",
        "date_reported",
        "date_updated",
        "description",
        "steps_to_reproduce",
        "expected_result",
        "actual_result",
        "comments",
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows({field: defect.get(field, "") for field in fields} for defect in defects)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=defect_summary_ruknuddin_asrari.csv"},
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
