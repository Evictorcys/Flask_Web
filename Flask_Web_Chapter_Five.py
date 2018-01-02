import sys
sys.path.append('..')
from flask import Flask,redirect,render_template,session,url_for,flash
from flask_wtf import FlaskForm
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from config import MYSQL_NAME,MYSQL_PASSWORD,ADMIN_MAIL,MAIL_USERNAME,MAIL_PASSWORD
from flask_mail import Mail,Message
from threading import Thread

app = Flask(__name__)

app.config['SECRET_KEY'] = "Evictor's password"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{0}:{1}@localhost/BlogSystem".format(MYSQL_NAME,MYSQL_PASSWORD)
# 每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['ADMIN_MAIL'] = ADMIN_MAIL
# 配置Flask-Mail使用163邮箱
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
# 定义邮件主题的前缀
app.config['MAIL_SUBJECT_PREFIX'] = '[Evictor]'
# 定义邮件发件人地址
app.config['MAIL_SENDER'] = 'Admin <e2856527729@163.com>'

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)

# 配置Flask-Migrate
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class NameForm(FlaskForm):
	name = StringField("What is your name?",validators = [Required()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(64),unique = True)
	users = db.relationship('User',backref = 'role',lazy = 'dynamic')

	def __repr__(self):
		return '<Role %r>'%self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(64),unique = True,index =True)
	role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>'%self.username

# 利用后台线程异步发送电子邮件
def send_async_mail(app,msg):
	with app.app_context():
		mail.send(msg)

# send_email参数分别为收件人地址、主题、渲染邮件正文的模板(不含扩展名)、关键字参数列表
def send_email(to,subject,template,**kwargs):
	msg = Message(app.config['MAIL_SUBJECT_PREFIX']+subject,
				  sender = app.config['MAIL_SENDER'],recipients = [to])
	msg.body = render_template(template + '.txt',**kwargs)
	msg.html = render_template(template + '.html',**kwargs)
	thr = Thread(target = send_async_mail,args = [app,msg])
	thr.start()
	return thr

# 为shell命令添加一个上下文
def make_shell_context():
	return dict(app = app,db =db,User = User,Role = Role)
manager.add_command('Shell',Shell(make_context = make_shell_context))

@app.route('/',methods = ['GET','POST'])
def index():
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
			if app.config['ADMIN_MAIL']:
				send_email(app.config['ADMIN_MAIL'],'A New User','mail/new_user',user = user)
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('db_index.html',form = form,name = session.get('name'),known = session.get('known',False))

def main():
	manager.run()

if __name__ == "__main__":
	main()
