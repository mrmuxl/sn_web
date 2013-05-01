ALTER TABLE kx_alipay_order MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_email_invate MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_ent MODIFY COLUMN ent_master_id varchar(32) NOT NULL;
ALTER TABLE kx_ent_user MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_ent_user MODIFY COLUMN updater_id varchar(32) NOT NULL;
ALTER TABLE kx_invate_record MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_invate_record MODIFY COLUMN invate_id varchar(32) NOT NULL;
ALTER TABLE kx_msg_board MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_org MODIFY COLUMN updater_id varchar(32) NOT NULL;
ALTER TABLE kx_org_self MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_org_self MODIFY COLUMN updater_id varchar(32) NOT NULL;
ALTER TABLE kx_soft_ad MODIFY COLUMN creater_id varchar(32) NOT NULL;
ALTER TABLE kx_user MODIFY COLUMN id varchar(32) NOT NULL;
ALTER TABLE kx_ent_user MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_ent_user MODIFY COLUMN updater_id varchar(32) NOT NULL;
ALTER TABLE kx_invate_record MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_invate_record MODIFY COLUMN invate_id varchar(32) NOT NULL;
ALTER TABLE kx_user_org MODIFY COLUMN user_id varchar(32) NOT NULL;
ALTER TABLE kx_user_org MODIFY COLUMN updater_id varchar(32) NOT NULL;
将auto_id 改为 id 类型无变化
ALTER TABLE kx_user CHANGE auto_id id int(11) NOT NULL AUTO_INCREMENT
将id 改为 uuid 类型无变化，注意此条要在改auto_id 之前
ALTER TABLE kx_user CHANGE id uuid varchar(32) NOT NULL
增加uuid的索引
ALTER TABLE kx_user ADD INDEX `uuid_index`(`uuid`);

