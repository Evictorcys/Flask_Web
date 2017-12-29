#  coding=utf-8
from flask import Flask
'''
实例Flask类的对象.
Flask所用参数决定程序的根目录,以便找到相对于程序根目录的资源文件位置.
'''
app =  Flask(__name__)

# 使用flask扩展，添加命令行解析功能
from flask.ext.script import Manager
manager = Manager(app)

# 利用app.route修饰器将修饰的函数注册为路由.
@app.route('/')
def index():
    #视图函数(view function)及返回响应
    return '<h1>Hello World!</h1>',200

'''
<name>为动态部分,默认使用字符串,但也可用类型定义:如<int:id>
还有float和path类型.path类型也是字符串,但不把斜线视作分隔符.
'''
@app.route('/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>' % name

# 通过make_response函数返回Response对象
from flask import make_response
@app.route('/response')
def myresponse():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

# redirect函数生成重定向响应
from flask import redirect
@app.route('/redirect')
def myredirect():
    return redirect('http://www.baidu.com')

# abort函数生成处理错误的特殊响应
from flask import abort
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello,%s</h1>' % user.name

def load_user(id):
    return False

if __name__ == "__main__":
    manager.run()

'''
python3 Flask_Web_Chapter_One.py runserver --host 0.0.0.0
让Web服务器监听公共网络接口上的连接
'''
