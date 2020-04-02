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
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


def main():
    global_init('db/blogs.sqlite')
    session = db_session.create_session()
    app.run()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationUser(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegistrtionJob(FlaskForm):
    team_leader = StringField('Team leader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = IntegerField('Size of work', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    is_finished = BooleanField('Finished or not')
    submit = SubmitField('Submit')


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(Jobs)
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
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/regjobs', methods=['GET', 'POST'])
def reqjobs():
    form = RegistrtionJob()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            teamleader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('RegJobs.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
