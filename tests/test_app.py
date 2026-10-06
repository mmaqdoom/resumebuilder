import unittest
from io import BytesIO
from unittest.mock import patch

from pypdf import PdfReader

from app import create_app, db
from app.models import Education, Experience, ResumeProfile, Skill, User


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


class ResumeBuilderTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def register(self, email="person@example.com"):
        return self.client.post(
            "/register",
            data={
                "email": email,
                "password": "secure-password-123",
                "confirm_password": "secure-password-123",
            },
            follow_redirects=True,
        )

    def test_auth_profile_edit_preview_pdf_and_delete(self):
        response = self.register()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My resumes", response.data)

        response = self.client.post(
            "/resume/create", data={"role_title": "Software Engineer"}
        )
        self.assertEqual(response.status_code, 302)
        resume = db.session.query(ResumeProfile).one()
        response = self.client.get(f"/resume/{resume.id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add experience", response.data)

        response = self.client.post(
            f"/resume/{resume.id}/edit",
            data={
                "role_title": "Backend Engineer",
                "full_name": "Casey Student",
                "email": "casey@example.com",
                "phone": "555-0100",
                "location": "Toronto, Canada",
                "linkedin_url": "https://www.linkedin.com/in/casey",
                "github_url": "https://github.com/casey",
                "summary": "Early-career engineer focused on reliable services.",
                "education-0-institution": "Example University",
                "education-0-degree": "Bachelor of Science",
                "education-0-field_of_study": "Computer Science",
                "education-0-start_date": "2021-09-01",
                "education-0-end_date": "2025-05-01",
                "education-0-gpa": "3.8",
                "education-0-deleted": "",
                "experience-0-company": "Example Labs",
                "experience-0-job_title": "Engineering Intern",
                "experience-0-location": "Toronto",
                "experience-0-start_date": "2024-05-01",
                "experience-0-end_date": "",
                "experience-0-is_current": "y",
                "experience-0-description": "Built internal developer tooling.",
                "experience-0-deleted": "",
                "skills-0-skill_name": "Python",
                "skills-0-category": "Programming",
                "skills-0-deleted": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        db.session.expire_all()
        self.assertEqual(resume.role_title, "Backend Engineer")
        self.assertEqual(resume.personal_info.full_name, "Casey Student")
        self.assertEqual(len(resume.education), 1)
        self.assertEqual(resume.education[0].institution, "Example University")
        self.assertEqual(len(resume.experience), 1)
        self.assertTrue(resume.experience[0].is_current)
        self.assertEqual(len(resume.skills), 1)

        response = self.client.get(f"/resume/{resume.id}/preview")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Casey Student", response.data)
        self.assertIn(b"Example Labs", response.data)

        response = self.client.get(f"/resume/{resume.id}/download")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertTrue(response.data.startswith(b"%PDF-"))
        self.assertIn("backend_engineer_Resume.pdf", response.headers["Content-Disposition"])
        pdf = PdfReader(BytesIO(response.data))
        self.assertEqual(len(pdf.pages), 1)
        pdf_text = pdf.pages[0].extract_text()
        self.assertIn("Casey Student", pdf_text)
        self.assertIn("Example Labs", pdf_text)

        response = self.client.post(f"/resume/{resume.id}/delete")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(db.session.query(ResumeProfile).count(), 0)
        self.assertEqual(db.session.query(Education).count(), 0)
        self.assertEqual(db.session.query(Experience).count(), 0)
        self.assertEqual(db.session.query(Skill).count(), 0)

    def test_resume_is_not_accessible_to_another_user(self):
        self.register()
        self.client.post("/resume/create", data={"role_title": "Data Analyst"})
        resume = db.session.query(ResumeProfile).one()

        self.client.post("/logout")
        self.register("other@example.com")
        response = self.client.get(f"/resume/{resume.id}/edit")
        self.assertEqual(response.status_code, 404)

    def test_login_rejects_external_next_url(self):
        self.register()
        self.client.post("/logout")
        response = self.client.post(
            "/login?next=https://example.org/",
            data={"email": "person@example.com", "password": "secure-password-123"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")

    def test_pdf_dependency_failure_is_reported(self):
        self.register()
        self.client.post("/resume/create", data={"role_title": "Developer"})
        resume = db.session.query(ResumeProfile).one()
        with patch("app.routes._render_pdf", side_effect=OSError("both renderers unavailable")):
            response = self.client.get(f"/resume/{resume.id}/download")
        self.assertEqual(response.status_code, 503)
        self.assertIn(b"Install xhtml2pdf", response.data)

    def test_invalid_dates_do_not_save_resume(self):
        self.register()
        self.client.post("/resume/create", data={"role_title": "Developer"})
        resume = db.session.query(ResumeProfile).one()
        response = self.client.post(
            f"/resume/{resume.id}/edit",
            data={
                "role_title": "Developer",
                "education-0-institution": "Example University",
                "education-0-degree": "Bachelor",
                "education-0-start_date": "2025-01-01",
                "education-0-end_date": "2024-01-01",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Education end dates must be on or after the start date.", response.data)
        self.assertEqual(db.session.query(Education).count(), 0)

    def test_whitespace_only_role_title_is_rejected(self):
        self.register()
        response = self.client.post(
            "/resume/create",
            data={"role_title": "   "},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.data)
        self.assertEqual(db.session.query(ResumeProfile).count(), 0)

    def test_password_reset_flow(self):
        self.register(email="user@example.com")
        self.client.post("/logout")

        # 1. Request reset link
        response = self.client.get("/reset_password")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Reset your password", response.data)

        # 2. Submit existing email
        response = self.client.post(
            "/reset_password",
            data={"email": "user@example.com"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"password reset instructions have been sent", response.data)

        # 3. Verify token and reset password
        user = db.session.scalar(db.select(User).where(User.email == "user@example.com"))
        self.assertIsNotNone(user)
        reset_token = user.get_reset_token()
        self.assertEqual(User.verify_reset_token(reset_token).id, user.id)

        response = self.client.get(f"/reset_password/{reset_token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Choose a new password", response.data)

        # 4. Submit new password
        response = self.client.post(
            f"/reset_password/{reset_token}",
            data={
                "password": "brand-new-password-123",
                "confirm_password": "brand-new-password-123",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Your password has been reset successfully", response.data)

        # 5. Old password no longer works
        response = self.client.post(
            "/login",
            data={"email": "user@example.com", "password": "secure-password-123"},
            follow_redirects=True,
        )
        self.assertIn(b"Invalid email or password", response.data)

        # 6. New password works
        response = self.client.post(
            "/login",
            data={"email": "user@example.com", "password": "brand-new-password-123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My resumes", response.data)


if __name__ == "__main__":
    unittest.main()
