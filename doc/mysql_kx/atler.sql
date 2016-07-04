添加字段并设置默认值
ALTER TABLE kx_user ADD is_superuser tinyint(1) NOT NULL DEFAULT 0 COMMENT "是否为超级用户" AFTER last_lan_ip;
ALTER TABLE kx_user ADD is_active tinyint(1) NOT NULL DEFAULT 1 COMMENT "用户是否激活跟status字段无关" AFTER is_superuser;
ALTER TABLE kx_user ADD is_staff tinyint(1) NOT NULL DEFAULT 0 COMMENT "能否登入Django Admin" AFTER is_active;
ALTER TABLE kx_user ADD is_vip tinyint(1) NOT NULL DEFAULT 0 COMMENT "是否vip用户" AFTER is_active;

删除is_staff字段
ALTER TABLE kx_user DROP COLUMN  is_staff;

更新kx_user表的is_acitve字段(慎用)
 UPDATE kx_user SET is_active=1 

添加超级用户:
 UPDATE kx_user SET is_superuser=1 WHERE email='mrmuxl@sina.com';

添加可登陆admin的用户:
 UPDATE kx_user SET is_staff=1 WHERE email='mrmuxl@sina.com';


关于kx_user表不能删除主键的问题:
第一步删除django_admin_log表引用的外键

ALTER TABLE django_admin_log DROP FOREIGN KEY user_id_refs_id_fda4e7d9;

第二步删除kx_user表的主键

ALTER TABLE kx_user DROP PRIMARY KEY;

第三步添加auto_id字段并设置为主键和自增字段

ALTER TABLE kx_user ADD auto_id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST;

第四步建立django_admin_log引用的外键

ALTER TABLE kx_user ADD INDEX `id_index`(`id`);

ALTER TABLE django_admin_log ADD CONSTRAINT `user_id_refs_id_fda4e7d9` FOREIGN KEY (`user_id`) REFERENCES `kx_user` (`id`)


给kx_pub 表添加字段
ALTER TABLE kx_pub ADD install_md5 varchar(32) NULL DEFAULT NULL COMMENT "安装文件的MD5" AFTER install_file;
ALTER TABLE kx_pub ADD patch_md5 varchar(32) NULL DEFAULT NULL COMMENT "patch文件的MD5" AFTER patch_file;
ALTER TABLE kx_pub ADD is_publish tinyint(1) NOT NULL DEFAULT 0 COMMENT "是否灰度发布用户" AFTER is_tongji;
