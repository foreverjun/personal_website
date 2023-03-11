from pathlib import Path
import shutil

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

from config import SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    text = db.Column(db.String(2048), nullable=False)

    create_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    update_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())


def db_init():
    guestbook_init = [
        {'name': 'Матвей', 'text': 'Помоему это похоже на неплохой сайт'}
    ]

    db_file = Path(SQLITE_DATABASE_NAME)
    if db_file.is_file():
        shutil.copyfile(SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME)

    db.session.commit()
    db.drop_all()
    db.create_all()
    print('Create guestbook')
    for p in guestbook_init:
        post = Post(name=p['name'], text=p['text'])
        db.session.add(post)
        db.session.commit()
