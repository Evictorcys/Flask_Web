from flask import Flask,render_template,session,redirect,url_for,flash
from flask_wtf import FlaskForm
from flask_script import Manager
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)

# 设置Flask-WTF
# app.config字典可用来存储框架、扩展和程序本身的配置变量。
app.config['SECRET_KEY'] = "Evictor's password"

# 一个简单的Web表单，包含一个名为name的文本字段和一个名为submit的提交按钮
# StringField类表示属性为type="text"的<input>元素。
# SubmitField类表示属性为type="submit"的<input>元素。
# validators指定一个由验证函数组成的列表，在接受用户提交的数据之前验证数据。验证函数Required()确保提交的字段不为空。
class NameForm(FlaskForm):
    name = StringField("What is your name?",validators = [Required()])
    submit = SubmitField('Submit')

"""
WTForms支持的HTML标准字段：
StringField 文本字段    TextAreaField 多行文本字段
PasswordField 密码文本字段    HiddenField 隐藏文本字段
DateField 文本字段，值为datetime.date格式
DateTimeField 文本字段，值为datetime.datetime格式
IntegerField 文本字段，值为整数    DecimalField 文本字段，值为decimal.Decimal
FloatField 文本字段，值为浮点数    BooleanField 复选框，值为True和False
RadioField 一组单选框    SelectField 下拉列表
SelectMultipleField 下拉列表，可选择多个值    FileField 文件上传字段
SubmitField 表单提交按钮    FormField 把表单作为字段嵌入另一个表单
FieldList 一组指定类型的字段
"""
"""
WTForms验证函数：
Email 验证电子邮件地址
EqualTo 比较两个字段的值；常用于要求输入两次密码进行确认的情况
IPAddress 验证IPv4网络地址    Length 验证输入字符串的长度
NumberRange 验证输入的值在数字范围内    Optional 无输入值时跳过其他验证函数
Required 确保字段中有数据    Regexp 使用正则表达式验证输入值
URL 验证URL    AnyOf 确保输入值在可选列表中
NoneOf 确保输入值不在可选列表中
"""

# 在视图函数中处理表单
# validate_on_submit()函数的返回值决定是重新渲染表单还是处理表单提交的数据。
# 实现了重定向和用户会话，解决了刷新页面重新提交表单问题
# 使用flash()函数让用户知道状态变化，如确认消息、警告或错误提醒。
@app.route('/',methods = ['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('form_index.html',form = form,name = session.get('name'))

@app.route('/index',methods = ['GET','POST'])
def flash_index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name !=form.name.data:
            flash("Looks like you have changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('flash_index'))
    return render_template('form_index.html',form = form,name = session.get('name'))

def main():
    manager.run()

if __name__ == "__main__":
    main()

