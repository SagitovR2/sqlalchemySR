from flask import Flask
from data import db_session
from data.jobs import Jobs
from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from data.users import User
from data.db_session import global_init

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    global_init('db/blogs.sqlite')
    app.run()


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(User)
    return render_template("jurnalrabot.html", users=news)


if __name__ == '__main__':
    main()
