 # 维护数据库迁移之前，使用init子命令创建迁移仓库
 # 该命令会创建migrations文件夹，所有迁移脚本都存放其中
 python Flask_Web_Chapter_Four.py db init

# 创建迁移脚本

# migrate子命令自动创建迁移脚本
python Flask_Web_Chapter_Four.py db migrate -m "initial migration"
# db upgrade命令将迁移应用到数据库中
python Flask_Web_Chapter_Four.py db upgrade
# downgrade将改动删除