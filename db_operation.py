from Flask_Web_Chapter_Four import db
from Flask_Web_Chapter_Four import Role,User

# 销毁旧旧表
db.drop_all()
# 根据模型类创建数据库
db.create_all()

admin_role = Role(name = 'Admin')
mod_role = Role(name = 'Moderator')
user_role = Role(name ='User')
user_evictor = User(user_name = 'Evictor',role = admin_role)
user_forever = User(user_name = 'Forever',role = user_role)
user_imundis = User(user_name = 'imundis',role = user_role)
user_charryyang = User(user_name = 'Charryyang',role = user_role)

# role属性虽然不是真正的数据库列，但也可使用
# 执行完上述操作后，这些对象只存在于Python中，还未写入数据库，故id为None

# 把对象写入数据库之前，先将其添加到会话中
db.session.add(admin_role)
db.session.add(mod_role)
db.session.add(user_role)
db.session.add(user_evictor)
db.session.add(user_forever)
db.session.add(user_imundis)
sb.session.add(user_charryyang)
# 或者简写成：db.session.add([admin_role,mod_role,...user_charryyang])

# 提交会话以写入数据库
db.session.commit()
# 回滚：db.session.rollback()

# 修改行
admin_role.name = 'Adminstrator'
db.session.add(admin_role)
db.session.commit()

# 删除行
db.session.delete(mod_role)
db.session.commit()

# 查询
# 利用query对象取回对应表中所有记录
Role.qury.all()
User.qury.all()
# 利用过滤器进行更精确的查询
'''
查询过滤器：
filter_by() 等值过滤器    limit() 限制查询结果数量
order_by() 排序    group_by() 分组
查询执行函数：
all() 以列表形式返回所有结果    first() 返回第一个结果或None
first_or_404() 返回第一个结果或终止请求返回404错误响应
get() 返回指定主键对应行或None    get_or_404()
count() 返回查询结果数目
paginate() 返回一个Paginate对象，包含指定范围内的结果 
''' 
User.qury.filter_by(role = user_role).all()
user_role = Role.query.filter_by(name = 'User').first()
user_role.users.order_by(User.username).all()
user_role.users.count()
# 查询原生SQL查询语句：
str(User.query.filter_by(role = user_role))
