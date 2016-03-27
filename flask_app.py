from flask import Flask, redirect, render_template, request, url_for
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

from flask_wtf.csrf import CsrfProtect

class MyForm(Form):
    name = StringField('name', validators=[DataRequired()])

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'ljhqweroisyudfjweroincsdjkhwids.nkusyfd'
CsrfProtect(app)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="ssharkey",
    password="knowmore34",
    hostname="ssharkey.mysql.pythonanywhere-services.com",
    databasename="ssharkey$comments",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    notedate = db.Column(db.DateTime)


@app.route('/', methods=["GET","POST"])
def index():
    form = MyForm()
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.order_by(desc(Comment.notedate)).all())

    if form.validate_on_submit:
        comment = Comment(content=request.form["contents"], notedate=datetime.now())
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=["POST"])
def delete_entry():
    form = MyForm()
    if form.validate_on_submit:
        Comment.query.filter(Comment.id == request.args.get('ID')).delete()
        db.session.commit()
    return redirect(url_for('index'))
