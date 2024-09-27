from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired


# Application init
app = Flask(__name__)  # initialize app object via Flask
bootstrap = Bootstrap(app)  # pass app into bootstrap
moment = Moment(app)  # Time
app.config["SECRET_KEY"] = "superstring"  # configure secret Key


# FlaskForm class with validators attached to fields
class NameForm(FlaskForm):
    name = StringField(
        "What is your name?",
        validators=[DataRequired(message="Your name is required.")],
    )
    uoft_email = StringField(
        "What is your UofT email?",
        validators=[DataRequired(message="Email is required.")],
    )
    submit = SubmitField("Submit")

    def validate_uoft_email(self, field):  # needs to follow validate_<field name>
        if "@" not in field.data:
            raise ValidationError(
                f"Please include an '@' in the email address. '{field.data}' is missing an '@'."
            )
        if "utoronto" not in field.data:
            raise ValidationError("Email must contain 'utoronto'.")


# Render WTF Form
@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # validate name
        old_name = session.get("name")
        old_email = session.get("uoft_email")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        if old_email is not None and old_email != form.uoft_email.data:
            flash("Looks like you have changed your email!")
        session["name"] = form.name.data

        # email validated
        session["uoft_email"] = form.uoft_email.data
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        uoft_email=session.get("uoft_email"),
    )


@app.route("/user/<name>")
def user(name):
    return render_template(
        "user.html", name=name, current_time=datetime.now(timezone.utc)
    )


# ERROR HANDLERS
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500
