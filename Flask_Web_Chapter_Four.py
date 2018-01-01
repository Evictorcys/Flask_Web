import sys
sys.path.append('..')
from flask import Flask,redirect,render_template,session,url_for,flash
from flask_wtf import FlaskForm
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_moment import Moment
from flask_migrate import Migrate,MigrateCommand
from config import MYSQL_NAME,MYSQL_PASSWORD

# 初始化及配置一个简单的Mysql数据库
app = Flask(__name__)
app.config['SECRET_KEY'] = "Evictor's password"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{0}:{1}@localhost/BlogSystem".format(MYSQL_NAME,MYSQL_PASSWORD)
# 每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)

# 配置Flask-Migrate
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

class NameForm(FlaskForm):
	name = StringField("What is your name?",validators = [Required()])
	submit = SubmitField('Submit')

# 定义Role和User模型
# 类变量__tablename__定义在数据库中使用的表名。
# 其余类变量为该模型的属性，被定义为的db.Column的实例。
# db.Column的第一个参数为列类型
# 其余参数为列选项：主键(primary_key)、非重复(unique)、创建索引(index)、允许空值(nullable)、定义默认值(default)
# 关系表示：Role模型中users属性将返回与角色向关联的用户列表；User模型中role_id列被定义为外键。
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
