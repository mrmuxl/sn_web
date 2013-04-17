Django集成现有数据库的步骤:
1:设置settings.py文件,设置好数据库用户名和密码
2:运行manager.py syncdb,运行之后会在数据库中创建几张表,这几张表是django运行所需要的表
3:用sql语句修改表结构
