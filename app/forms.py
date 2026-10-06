from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FieldList,
    Form,
    FormField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    URL,
)


def _strip_input(value):
    return value.strip() if value else value


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email address",
        filters=[_strip_input],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email address",
        filters=[_strip_input],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


class RequestResetForm(FlaskForm):
    email = StringField(
        "Email address",
        filters=[_strip_input],
        validators=[DataRequired(), Email(), Length(max=254)],
    )
    submit = SubmitField("Send password reset link")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New password", validators=[DataRequired(), Length(min=8, max=128)]
    )
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Reset password")


class CreateResumeForm(FlaskForm):
    role_title = StringField(
        "Target role",
        filters=[_strip_input],
        validators=[DataRequired(), Length(min=2, max=100)],
        render_kw={"placeholder": "e.g. Product Designer"},
    )
    submit = SubmitField("Create resume")


class EducationEntryForm(Form):
    institution = StringField(
        "Institution", filters=[_strip_input], validators=[Optional(), Length(max=160)]
    )
    degree = StringField(
        "Degree", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    field_of_study = StringField(
        "Field of study", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    start_date = DateField("Start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("End date", format="%Y-%m-%d", validators=[Optional()])
    gpa = StringField("GPA", filters=[_strip_input], validators=[Optional(), Length(max=20)])
    deleted = HiddenField(default="")


class ExperienceEntryForm(Form):
    company = StringField(
        "Company", filters=[_strip_input], validators=[Optional(), Length(max=160)]
    )
    job_title = StringField(
        "Job title", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    location = StringField(
        "Location", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    start_date = DateField("Start date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("End date", format="%Y-%m-%d", validators=[Optional()])
    is_current = BooleanField("I currently work here")
    description = TextAreaField(
        "Description", filters=[_strip_input], validators=[Optional(), Length(max=5000)]
    )
    deleted = HiddenField(default="")


class SkillEntryForm(Form):
    skill_name = StringField(
        "Skill", filters=[_strip_input], validators=[Optional(), Length(max=100)]
    )
    category = StringField(
        "Category", filters=[_strip_input], validators=[Optional(), Length(max=100)]
    )
    deleted = HiddenField(default="")


class ResumeForm(FlaskForm):
    role_title = StringField(
        "Target role",
        filters=[_strip_input],
        validators=[DataRequired(), Length(min=2, max=100)],
    )
    full_name = StringField(
        "Full name", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    email = StringField(
        "Contact email",
        filters=[_strip_input],
        validators=[Optional(), Email(), Length(max=254)],
    )
    phone = StringField("Phone", filters=[_strip_input], validators=[Optional(), Length(max=40)])
    location = StringField(
        "Location", filters=[_strip_input], validators=[Optional(), Length(max=120)]
    )
    linkedin_url = StringField(
        "LinkedIn URL", filters=[_strip_input], validators=[Optional(), URL(), Length(max=500)]
    )
    github_url = StringField(
        "GitHub URL", filters=[_strip_input], validators=[Optional(), URL(), Length(max=500)]
    )
    summary = TextAreaField(
        "Professional summary",
        filters=[_strip_input],
        validators=[Optional(), Length(max=3000)],
    )
    education = FieldList(FormField(EducationEntryForm), min_entries=1)
    experience = FieldList(FormField(ExperienceEntryForm), min_entries=1)
    skills = FieldList(FormField(SkillEntryForm), min_entries=1)
    submit = SubmitField("Save changes")
