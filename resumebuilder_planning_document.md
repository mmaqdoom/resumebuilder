# Comprehensive Planning Document: ResumeBuilder Application

## 1. Project Overview & Objectives

**ResumeBuilder** is a web-based application designed for students to manage professional profiles and generate tailored resumes in PDF format. The system allows students to maintain multiple role profiles (e.g., "Software Engineer", "Data Analyst") under a single account, allowing them to customize their resume content per job domain.

### Key Goals
* **MVP Phase:** Allow user registration, role-based profile management, dynamic resume preview, and single-template PDF downloads using Flask and standard Jinja2 templating.
* **Future Phase:** Integrate a paywall (monetization via download restriction/Stripe) and introduce multiple customizable resume template designs.

---

## 2. Technology Stack & Dependencies

| Component | Choice | Reason / Purpose |
| --- | --- | --- |
| **Backend Framework** | Flask | Lightweight, highly modular Python web framework. |
| **Template Engine** | Jinja2 | Native Flask templating for UI rendering and HTML resume layout generation. |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) | Structured relational storage managed via `Flask-SQLAlchemy`. |
| **Form Handling** | Flask-WTF / WTForms | Dynamic input validation, CSRF protection, and structured data handling. |
| **Authentication** | Flask-Login | User session management and secure route authorization. |
| **PDF Engine** | WeasyPrint | Renders HTML/CSS templates into high-fidelity PDF documents. |

---

## 3. Database Architecture & Data Models

To support multiple resume variations per student, the database uses a one-to-many model where a `User` owns multiple `ResumeProfile` entries. Each `ResumeProfile` contains dedicated personal details, education entries, experience items, and skills.

```
                     +-------------------+
                     |       User        |
                     +-------------------+
                     | id (PK)           |
                     | email             |
                     | password_hash     |
                     | is_premium        |
                     +---------+---------+
                               | 1
                               |
                               | N
                   +-----------v-----------+
                   |     ResumeProfile     |
                   +-----------------------+
                   | id (PK)               |
                   | user_id (FK)          |
                   | role_title            |
                   | design_id             |
                   +-----------+-----------+
                               |
       +-----------------------+-----------------------+-----------------------+
       | 1                     | 1                     | 1                     | 1
       | 1                     | N                     | N                     | N
+------v-------+        +------v-------+        +------v-------+        +------v-------+
| PersonalInfo |        |  Education   |        |  Experience  |        |    Skill     |
+--------------+        +--------------+        +--------------+        +--------------+
| id (PK)      |        | id (PK)      |        | id (PK)      |        | id (PK)      |
| resume_id(FK)|        | resume_id(FK)|        | resume_id(FK)|        | resume_id(FK)|
| full_name    |        | institution  |        | company      |        | skill_name   |
| email        |        | degree       |        | job_title    |        | proficiency  |
| phone        |        | start_date   |        | start_date   |        +--------------+
| linkedin     |        | end_date     |        | end_date     |
| github       |        +--------------+        | description  |
+--------------+                                +--------------+
```

### Detailed Table Specifications

* **User**: `id`, `email`, `password_hash`, `is_premium` (Boolean, default `False`), `created_at`
* **ResumeProfile**: `id`, `user_id` (FK -> User.id), `role_title` (e.g., "Full Stack Developer"), `design_id` (Integer, default `1`), `updated_at`
* **PersonalInfo**: `id`, `resume_id` (FK -> ResumeProfile.id), `full_name`, `email`, `phone`, `location`, `linkedin_url`, `github_url`, `summary`
* **Education**: `id`, `resume_id` (FK -> ResumeProfile.id), `institution`, `degree`, `field_of_study`, `start_date`, `end_date`, `gpa`
* **Experience**: `id`, `resume_id` (FK -> ResumeProfile.id), `company`, `job_title`, `location`, `start_date`, `end_date`, `is_current`, `description`
* **Skill**: `id`, `resume_id` (FK -> ResumeProfile.id), `skill_name`, `category` (e.g., "Programming Languages", "Tools")

---

## 4. Project Directory Structure

```text
resume_builder/
├── app/
│   ├── __init__.py          # Application factory & extension initialization
│   ├── models.py            # SQLAlchemy database models
│   ├── forms.py             # WTForms schema definitions
│   ├── routes.py            # Application controllers and endpoints
│   ├── static/
│   │   ├── css/
│   │   │   ├── dashboard.css # Styles for web interface/dashboard
│   │   │   └── resume_1.css  # Print/PDF styles for standard resume design
│   │   └── js/
│   │       └── dynamic_forms.js # Frontend script for adding/removing form rows
│   ├── templates/
│   │   ├── base.html        # App layout wrapper
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── dashboard.html   # Resume selection and management interface
│   │   ├── edit_resume.html # Form interface to edit education/experience/skills
│   │   └── designs/
│   │       └── simple.html  # Jinja2 template converted directly to PDF
├── config.py                # Environment configuration
├── requirements.txt         # Dependencies list
└── run.py                   # App startup entrypoint
```

---

## 5. Core Routing & Request Flow

| Route | Method | Access | Purpose |
| --- | --- | --- | --- |
| `/` | GET | Public | Landing page explaining the tool. |
| `/register` | GET, POST | Public | User account creation. |
| `/login` | GET, POST | Public | User authentication using `Flask-Login`. |
| `/logout` | GET | Auth | Logs out current user session. |
| `/dashboard` | GET | Auth | Overview of all created role profiles with action buttons (Edit, Preview, Download, Delete). |
| `/resume/create` | POST | Auth | Initializes a new `ResumeProfile` record with a user-provided `role_title`. |
| `/resume/<int:id>/edit` | GET, POST | Auth | Detailed form interface for updating personal info, education, experience, and skills. |
| `/resume/<int:id>/preview` | GET | Auth | Renders `designs/simple.html` directly in the browser frame. |
| `/resume/<int:id>/download`| GET | Auth | Fetches profile context, parses HTML via WeasyPrint, and returns a binary PDF file. |

---

## 6. PDF Generation Strategy

Instead of relying on headless browsers or strict programmatic layout tools, the PDF generation pipeline converts standard HTML/CSS templates processed by Jinja2 into raw PDF bytes.

### Processing Pipeline:
1. User clicks **"Download PDF"** on `/resume/<id>/download`.
2. Flask queries the database for the given `resume_id` and verifies user ownership.
3. Flask calls `render_template('designs/simple.html', resume=resume_data)`.
4. `WeasyPrint` compiles the HTML string along with linked stylesheets (`resume_1.css`) directly into a binary PDF payload.
5. Flask returns a response configured with `Content-Type: application/pdf` and `Content-Disposition: attachment; filename="<role>_Resume.pdf"`.

---

## 7. Future-Proofing Strategy: Monetization & Template Engine

### A. Template Selection Architecture
The `ResumeProfile` table stores a `design_id`. 
* **Phase 1:** Defaults to `1` (`designs/simple.html`).
* **Phase 2 Expansion:** Adding a new layout involves creating `designs/modern.html` and `static/css/resume_2.css`. The route dynamically renders:
  ```python
  template_map = {1: 'designs/simple.html', 2: 'designs/modern.html'}
  rendered_html = render_template(template_map.get(resume.design_id), resume=resume)
  ```

### B. Download Monetization (Paywall Integration)
1. Free users can access the editor, save profiles, and use `/preview`.
2. On `/download`, Flask checks the monetization status:
   ```python
   if not current_user.is_premium:
       flash("Please purchase a subscription to download PDF resumes.", "warning")
       return redirect(url_for('checkout', resume_id=resume.id))
   ```
3. Integrate Stripe Checkout via API webhooks to toggle `user.is_premium = True` upon completed payment.

---

## 8. Implementation Roadmap

### Phase 1: Foundation & Setup
- [ ] Initialize Flask app structure and configure SQLite/SQLAlchemy.
- [ ] Create user authentication system (`Flask-Login`, password hashing).
- [ ] Build basic app shell (`base.html`, navigation, static asset pipeline).

### Phase 2: Resume Profile & Data Management
- [ ] Implement database models (`ResumeProfile`, `PersonalInfo`, `Education`, `Experience`, `Skill`).
- [ ] Design the dashboard interface to manage multiple role profiles.
- [ ] Build WTForms interface to handle CRUD operations on resume components.

### Phase 3: Preview & PDF Engine
- [ ] Create `designs/simple.html` and CSS optimized for print page sizing (`@page { size: A4; margin: 0; }`).
- [ ] Configure WeasyPrint rendering engine in `/resume/<id>/download`.
- [ ] Implement web preview frame on `/resume/<id>/preview`.

### Phase 4: Monetization & Polish (Future)
- [ ] Add Stripe payment workflow for individual PDF downloads or subscription tiers.
- [ ] Build additional resume layout templates (`designs/modern.html`, `designs/creative.html`).