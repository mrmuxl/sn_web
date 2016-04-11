添加字段并设置默认值
ALTER TABLE kx_user ADD is_superuser tinyint(1) NOT NULL DEFAULT 0 COMMENT "是否为超级用户" AFTER active_time;
ALTER TABLE kx_user ADD is_active tinyint(1) NOT NULL DEFAULT 1 COMMENT "用户是否激活跟status字段无关" AFTER is_superuser;
ALTER TABLE kx_user ADD is_staff tinyint(1) NOT NULL DEFAULT 0 COMMENT "能否登入Django Admin" AFTER is_active;
删除is_staff字段
ALTER TABLE kx_user DROP COLUMN  is_staff;
更新kx_user表的is_acitve字段(慎用)
 UPDATE kx_user SET is_active=1 
添加超级用户:
 UPDATE kx_user SET is_superuser=1 WHERE email='mrmuxl@sina.com';
添加可登陆admin的用户:
 UPDATE kx_user SET is_staff=1 WHERE email='mrmuxl@sina.com';
