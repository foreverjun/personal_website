import sys

from flask import Flask, render_template, request, url_for, redirect, flash

from config import SQLITE_DATABASE_NAME
from model import db, db_init, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + SQLITE_DATABASE_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "test-key"

db.app = app
db.init_app(app)


@app.route('/')
def main_page():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('index.html', posts=posts)


@app.route('/guestbook', methods=['POST'])
def guest_book():
    name = request.form.get('name', type=str, default='')
    message = request.form.get('message', type=str, default='')

    if not name.strip() and not message.strip():
        flash('Поля не должны быть пустыми')
        return redirect(url_for("main_page") + '#contacts')
    try:
        post = Post(name=name, text=message)
        db.session.add(post)
        db.session.commit()
    except:
        flash('Не удалось добавить отзыв. Попробуйте позже.')
        print('Error wile adding new post')
        return redirect(url_for("main_page") + '#contacts')

    return redirect(url_for("main_page") + '#reviews')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            with app.app_context():
                db_init()
                sys.exit(0)
    app.run()
