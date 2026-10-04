from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


def utc_now():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_premium = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    resumes = db.relationship(
        "ResumeProfile",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="ResumeProfile.updated_at.desc()",
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class ResumeProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role_title = db.Column(db.String(100), nullable=False)
    design_id = db.Column(db.Integer, nullable=False, default=1)
    updated_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=utc_now, onupdate=utc_now
    )
    user = db.relationship("User", back_populates="resumes")
    personal_info = db.relationship(
        "PersonalInfo",
        back_populates="resume",
        cascade="all, delete-orphan",
        uselist=False,
    )
    education = db.relationship(
        "Education",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Education.id",
    )
    experience = db.relationship(
        "Experience",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Experience.id",
    )
    skills = db.relationship(
        "Skill",
        back_populates="resume",
        cascade="all, delete-orphan",
        order_by="Skill.id",
    )


class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resume_profile.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    full_name = db.Column(db.String(120), nullable=False, default="")
    email = db.Column(db.String(254), nullable=False, default="")
    phone = db.Column(db.String(40), nullable=False, default="")
    location = db.Column(db.String(120), nullable=False, default="")
    linkedin_url = db.Column(db.String(500), nullable=False, default="")
    github_url = db.Column(db.String(500), nullable=False, default="")
    summary = db.Column(db.Text, nullable=False, default="")
    resume = db.relationship("ResumeProfile", back_populates="personal_info")


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(
        db.Integer, db.ForeignKey("resume_profile.id", ondelete="CASCADE"), nullable=False
    )
    institution = db.Column(db.String(160), nullable=False)
    degree = db.Column(db.String(120), nullable=False)
    field_of_study = db.Column(db.String(120), nullable=False, default="")
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    gpa = db.Column(db.String(20), nullable=False, default="")
    resume = db.relationship("ResumeProfile", back_populates="education")


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(
        db.Integer, db.ForeignKey("resume_profile.id", ondelete="CASCADE"), nullable=False
    )
    company = db.Column(db.String(160), nullable=False)
    job_title = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False, default="")
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, nullable=False, default=False)
    description = db.Column(db.Text, nullable=False, default="")
    resume = db.relationship("ResumeProfile", back_populates="experience")


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(
        db.Integer, db.ForeignKey("resume_profile.id", ondelete="CASCADE"), nullable=False
    )
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False, default="")
    resume = db.relationship("ResumeProfile", back_populates="skills")


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
