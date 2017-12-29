# coding=utf-8

# 使用Jinja2模板引擎
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
from datetime import datetime
app = Flask(__name__)
manager = Manager(app)
# 初始化Flask-Bootstrap
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html',current_time = datetime.utcnow())

'''
Flask默认在程序文件夹中的templates子文件夹中寻找模板。
render_template函数将Jinja2模板引擎集成到程序中，
该函数第一个参数为模板文件名，随后的参数都是键值对。
'''

@app.route('/user/<name>')
def user(name):
    return render_template('bootstrap_user.html',name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

def main():
    # app.run()
    manager.run()

if __name__ == "__main__":
    manager.run()
