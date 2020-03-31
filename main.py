from flask import Flask
from data import db_session
from data.jobs import Jobs
from flask import Flask
from flask import url_for
from flask import request
from flask import render_template, redirect
from data.users import User
from data.db_session import global_init
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    global_init('db/blogs.sqlite')
    app.run()


class RegistrationUser(FlaskForm):
    login = StringField('Login/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(User)
    return render_template("jurnalrabot.html", users=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegistrationUser()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
