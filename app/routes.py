import os
from io import BytesIO
from pathlib import Path
import unicodedata
from urllib.parse import urljoin, urlparse

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import db
from app.email import send_password_reset_email
from app.forms import (
    CreateResumeForm,
    LoginForm,
    RegistrationForm,
    RequestResetForm,
    ResetPasswordForm,
    ResumeForm,
)
from app.models import Education, Experience, PersonalInfo, ResumeProfile, Skill, User, utc_now

main = Blueprint("main", __name__)


def _safe_next_url(target):
    if not target:
        return None
    parsed = urlparse(target)
    if (
        parsed.scheme
        or parsed.netloc
        or "\\" in target
        or not target.startswith("/")
        or target.startswith("//")
    ):
        return None
    if urlparse(urljoin(request.host_url, target)).netloc != request.host:
        return None
    return target


def _owned_resume(resume_id):
    resume = db.session.scalar(
        select(ResumeProfile).where(
            ResumeProfile.id == resume_id, ResumeProfile.user_id == current_user.id
        )
    )
    if resume is None:
        abort(404)
    return resume


def _resume_form_data(resume):
    info = resume.personal_info
    return {
        "role_title": resume.role_title,
        "full_name": info.full_name if info else "",
        "email": info.email if info else "",
        "phone": info.phone if info else "",
        "location": info.location if info else "",
        "linkedin_url": info.linkedin_url if info else "",
        "github_url": info.github_url if info else "",
        "summary": info.summary if info else "",
        "education": [
            {
                "institution": item.institution,
                "degree": item.degree,
                "field_of_study": item.field_of_study,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "gpa": item.gpa,
            }
            for item in resume.education
        ],
        "experience": [
            {
                "company": item.company,
                "job_title": item.job_title,
                "location": item.location,
                "start_date": item.start_date,
                "end_date": item.end_date,
                "is_current": item.is_current,
                "description": item.description,
            }
            for item in resume.experience
        ],
        "skills": [
            {"skill_name": item.skill_name, "category": item.category}
            for item in resume.skills
        ],
    }


def _get_or_create_personal_info(resume):
    if resume.personal_info is None:
        resume.personal_info = PersonalInfo()
    return resume.personal_info


def _update_resume(resume, form):
    resume.role_title = form.role_title.data.strip()
    info = _get_or_create_personal_info(resume)
    for field in (
        "full_name",
        "email",
        "phone",
        "location",
        "linkedin_url",
        "github_url",
        "summary",
    ):
        value = getattr(form, field).data
        setattr(info, field, value.strip() if value else "")

    resume.education.clear()
    for entry in form.education.entries:
        data = entry.form
        if data.deleted.data or not (data.institution.data or data.degree.data):
            continue
        if not data.institution.data or not data.degree.data:
            raise ValueError("Each education entry needs both an institution and a degree.")
        if data.start_date.data and data.end_date.data and data.end_date.data < data.start_date.data:
            raise ValueError("Education end dates must be on or after the start date.")
        resume.education.append(
            Education(
                institution=data.institution.data.strip(),
                degree=data.degree.data.strip(),
                field_of_study=(data.field_of_study.data or "").strip(),
                start_date=data.start_date.data,
                end_date=data.end_date.data,
                gpa=(data.gpa.data or "").strip(),
            )
        )

    resume.experience.clear()
    for entry in form.experience.entries:
        data = entry.form
        if data.deleted.data or not (data.company.data or data.job_title.data):
            continue
        if not data.company.data or not data.job_title.data:
            raise ValueError("Each experience entry needs both a company and a job title.")
        if data.is_current.data:
            end_date = None
        else:
            end_date = data.end_date.data
        if data.start_date.data and end_date and end_date < data.start_date.data:
            raise ValueError("Experience end dates must be on or after the start date.")
        resume.experience.append(
            Experience(
                company=data.company.data.strip(),
                job_title=data.job_title.data.strip(),
                location=(data.location.data or "").strip(),
                start_date=data.start_date.data,
                end_date=end_date,
                is_current=data.is_current.data,
                description=(data.description.data or "").strip(),
            )
        )

    resume.skills.clear()
    for entry in form.skills.entries:
        data = entry.form
        if data.deleted.data or not data.skill_name.data:
            continue
        resume.skills.append(
            Skill(
                skill_name=data.skill_name.data.strip(),
                category=(data.category.data or "").strip(),
            )
        )
    resume.updated_at = utc_now()


@main.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if db.session.scalar(select(User.id).where(User.email == email)) is not None:
            form.email.errors.append("An account with this email already exists.")
        else:
            user = User(email=email)
            user.set_password(form.password.data)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                form.email.errors.append("An account with this email already exists.")
            else:
                login_user(user)
                flash("Your account is ready. Create your first resume profile.", "success")
                return redirect(url_for("main.dashboard"))
    return render_template("auth/register.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.scalar(select(User).where(User.email == email))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password.", "danger")
        else:
            login_user(user, remember=form.remember.data)
            flash("Welcome back.", "success")
            return redirect(_safe_next_url(request.args.get("next")) or url_for("main.dashboard"))
    return render_template("auth/login.html", form=form)


@main.route("/reset_password", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RequestResetForm()
    dev_reset_url = None
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = db.session.scalar(select(User).where(User.email == email))
        if user is not None:
            token = user.get_reset_token()
            reset_url = url_for("main.reset_password", token=token, _external=True)
            sent = send_password_reset_email(user, reset_url)
            if not sent:
                dev_reset_url = reset_url
        flash(
            "If an account with that email exists, password reset instructions have been sent.",
            "info",
        )
        return render_template(
            "auth/reset_password_request.html",
            form=form,
            dev_reset_url=dev_reset_url,
            submitted=True,
        )
    return render_template("auth/reset_password_request.html", form=form)


@main.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That password reset link is invalid or has expired. Please request a new one.", "danger")
        return redirect(url_for("main.reset_password_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset successfully! You can now log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("auth/reset_password.html", form=form)


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", resumes=current_user.resumes, form=CreateResumeForm())


@main.route("/resume/create", methods=["POST"])
@login_required
def create_resume():
    form = CreateResumeForm()
    if not form.validate_on_submit():
        for errors in form.errors.values():
            for error in errors:
                flash(error, "danger")
        return redirect(url_for("main.dashboard"))
    resume = ResumeProfile(user_id=current_user.id, role_title=form.role_title.data.strip())
    resume.personal_info = PersonalInfo()
    db.session.add(resume)
    db.session.commit()
    flash("Resume profile created. Add your details below.", "success")
    return redirect(url_for("main.edit_resume", resume_id=resume.id))


@main.route("/resume/<int:resume_id>/edit", methods=["GET", "POST"])
@login_required
def edit_resume(resume_id):
    resume = _owned_resume(resume_id)
    form = ResumeForm(data=_resume_form_data(resume)) if request.method == "GET" else ResumeForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            _update_resume(resume, form)
        except ValueError as error:
            db.session.rollback()
            flash(str(error), "danger")
        else:
            db.session.commit()
            flash("Resume changes saved.", "success")
            return redirect(url_for("main.edit_resume", resume_id=resume.id))
    return render_template("edit_resume.html", resume=resume, form=form)


@main.route("/resume/<int:resume_id>/preview")
@login_required
def preview_resume(resume_id):
    resume = _owned_resume(resume_id)
    return render_template(
        "designs/simple.html",
        resume=resume,
        stylesheet_href=url_for("static", filename="css/resume_1.css"),
        preview=True,
    )


@main.route("/resume/<int:resume_id>/download")
@login_required
def download_resume(resume_id):
    resume = _owned_resume(resume_id)
    stylesheet = Path(current_app.static_folder) / "css" / "resume_1.css"
    html = render_template(
        "designs/simple.html",
        resume=resume,
        stylesheet_href=None,
        stylesheet_inline=stylesheet.read_text(encoding="utf-8"),
        preview=False,
    )
    try:
        pdf = _render_pdf(html)
    except (ImportError, OSError):
        current_app.logger.exception("PDF rendering dependencies are unavailable.")
        abort(
            503,
            description=(
                "PDF generation is unavailable. Install xhtml2pdf or install "
                "WeasyPrint and its platform dependencies."
            ),
        )
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{_download_filename(resume.role_title)}"'
    )
    response.headers["Content-Length"] = str(len(pdf))
    return response


def _render_pdf(html):
    if os.name == "nt":
        return _render_xhtml2pdf(html)

    try:
        from weasyprint import HTML
    except (ImportError, OSError) as error:
        current_app.logger.warning(
            "WeasyPrint is unavailable (%s); trying the xhtml2pdf renderer.",
            error,
        )
    else:
        try:
            return HTML(string=html, base_url=current_app.root_path).write_pdf()
        except OSError as error:
            current_app.logger.warning(
                "WeasyPrint could not load a platform library (%s); trying xhtml2pdf instead.",
                error,
            )

    return _render_xhtml2pdf(html)


def _render_xhtml2pdf(html):
    from xhtml2pdf import pisa

    output = BytesIO()
    result = pisa.CreatePDF(src=html, dest=output, path=current_app.root_path)
    if result.err:
        raise OSError("The xhtml2pdf renderer could not create the resume PDF.")
    return output.getvalue()


def _download_filename(role_title):
    ascii_title = unicodedata.normalize("NFKD", role_title).encode("ascii", "ignore").decode()
    slug = "".join(character.lower() if character.isalnum() else "_" for character in ascii_title)
    slug = slug.strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return f"{slug or 'resume'}_Resume.pdf"


@main.route("/resume/<int:resume_id>/delete", methods=["POST"])
@login_required
def delete_resume(resume_id):
    resume = _owned_resume(resume_id)
    db.session.delete(resume)
    db.session.commit()
    flash("Resume profile deleted.", "success")
    return redirect(url_for("main.dashboard"))
