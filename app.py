import os
import sys
import click
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)


@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(40))


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Hyde Sun'
    movies = [
        {
            'title': 'My Neighbor Totoro',
            'year': '1988'
        },
        {
            'title': 'Dead Poets Society',
            'year': '1989'
        },
        {
            'title': 'A Perfect World',
            'year': '1993'
        },
        {
            'title': 'Leon',
            'year': '1994'
        },
        {
            'title': 'Mahjong',
            'year': '1996'
        },
        {
            'title': 'Swallowtail Butterfly',
            'year': '1996'
        },
        {
            'title': 'King of Comedy',
            'year': '1999'
        },
        {
            'title': 'Devils on the Doorstep',
            'year': '1999'
        },
        {
            'title': 'WALL-E',
            'year': '2008'
        },
        {
            'title': 'The Pork of Music',
            'year': '2012'
        },
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
