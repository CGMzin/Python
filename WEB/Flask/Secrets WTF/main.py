from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(check_deliverability=True)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In')


app = Flask(__name__)
app.secret_key = "teste"
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@email.com' and login_form.password.data == '12345678':
            return render_template('success.html')
        else:
            return render_template('denied.html')
    return render_template('login.html', form=login_form)

if __name__ == '__main__':
    app.run()