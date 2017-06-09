-- MySQL dump 10.13  Distrib 5.1.69, for redhat-linux-gnu (i386)
--
-- Host: localhost    Database: kx
-- ------------------------------------------------------
-- Server version	5.1.69-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=211 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `blog`
--

DROP TABLE IF EXISTS `blog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `summary` longtext NOT NULL,
  `content` longtext NOT NULL,
  `status` int(11) NOT NULL,
  `is_above` tinyint(1) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `hits` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  KEY `blog_6f33f001` (`category_id`),
  KEY `blog_e969df21` (`author_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `order` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `category_f52cfca0` (`slug`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1160 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=71 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum_comment`
--

DROP TABLE IF EXISTS `forum_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fid_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `ip` char(15) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_comment_fc60dd82` (`fid_id`),
  KEY `forum_comment_6340c63c` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=490 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum_post`
--

DROP TABLE IF EXISTS `forum_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `vote_up` int(11) NOT NULL,
  `vote_down` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `ip` char(15) DEFAULT NULL,
  `status` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `hits` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `forum_post_6340c63c` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=533 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum_post_tags`
--

DROP TABLE IF EXISTS `forum_post_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum_post_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forumpost_id` int(11) NOT NULL,
  `forumtags_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `forumpost_id` (`forumpost_id`,`forumtags_id`),
  KEY `forum_post_tags_7c90d24d` (`forumpost_id`),
  KEY `forum_post_tags_21ee4633` (`forumtags_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `forum_tags`
--

DROP TABLE IF EXISTS `forum_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `forum_tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `count_post` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_grade`
--

DROP TABLE IF EXISTS `group_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_grade` (
  `grade` int(11) DEFAULT NULL,
  `begin_time` int(11) DEFAULT NULL,
  `end_time` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_act_tongji`
--

DROP TABLE IF EXISTS `kx_act_tongji`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_act_tongji` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tongji_day` date NOT NULL COMMENT '统计日期',
  `on_num` int(11) NOT NULL DEFAULT '0' COMMENT '当日上线总注册用户数',
  `act_num` int(11) NOT NULL DEFAULT '0' COMMENT '当日激活数',
  `un_num` int(11) NOT NULL DEFAULT '0' COMMENT '卸载数',
  `vc_val` decimal(2,2) NOT NULL DEFAULT '0.00' COMMENT '病毒传播系数',
  `trans0` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输>0次',
  `trans1` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输1次',
  `trans2` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输2-4次',
  `trans3` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输5次及以上',
  `print0` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数>0',
  `print1` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数1',
  `print2` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数2',
  `print3` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数5及以上',
  `chat0` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数>0',
  `chat1` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数1',
  `chat2` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数2-4',
  `chat3` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数5及以上',
  `friend0` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数>0',
  `friend1` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数1',
  `friend2` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数2-4',
  `friend3` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数5及以上',
  `invite0` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数>0',
  `invite1` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数1',
  `invite2` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数2-3',
  `invite3` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数4-5',
  `invite4` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数6及以上',
  `friend_all0` int(11) NOT NULL DEFAULT '0' COMMENT '累计好友人数0',
  `friend_all1` int(11) NOT NULL DEFAULT '0' COMMENT '累计好友人数1',
  `friend_all2` int(11) NOT NULL DEFAULT '0' COMMENT '累计好友人数2-4',
  `friend_all3` int(11) NOT NULL DEFAULT '0' COMMENT '累计好友人数5及以上',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tongji_day` (`tongji_day`)
) ENGINE=MyISAM AUTO_INCREMENT=243 DEFAULT CHARSET=utf8 COMMENT='每日上线注册用户行为统计信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_alipay_order`
--

DROP TABLE IF EXISTS `kx_alipay_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_alipay_order` (
  `order_id` varchar(14) NOT NULL,
  `title` varchar(200) NOT NULL,
  `pay_money` decimal(10,2) NOT NULL,
  `qianmo_dot` int(11) NOT NULL,
  `add_qianmo_dot` int(11) NOT NULL DEFAULT '0',
  `user_id` varchar(32) NOT NULL,
  `trade_no` varchar(16) DEFAULT NULL,
  `pay_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0=待支付，1=支付完成',
  `create_time` datetime NOT NULL,
  `finish_time` datetime DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='支付订单';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_csc_record`
--

DROP TABLE IF EXISTS `kx_csc_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_csc_record` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `mac` varchar(100) DEFAULT NULL,
  `called_email` varchar(50) DEFAULT NULL,
  `called_mac` varchar(100) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `transferd_size` bigint(20) unsigned DEFAULT '0' COMMENT '单位:byte',
  `status` tinyint(3) unsigned DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=157418 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_email_invate`
--

DROP TABLE IF EXISTS `kx_email_invate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_email_invate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL COMMENT '邀请人用户ID',
  `user_name` varchar(20) NOT NULL COMMENT '邀请人用户姓名',
  `invate_email` varchar(50) NOT NULL COMMENT '被邀请用户email',
  `invate_name` varchar(20) NOT NULL COMMENT '被邀请用户姓名',
  `group_id` int(11) NOT NULL COMMENT '群ID -1表示加好友',
  `group_name` varchar(50) NOT NULL COMMENT '群名称',
  `invate_code` varchar(50) NOT NULL COMMENT '邀请码',
  `qianmo_dot` int(11) NOT NULL COMMENT '赠送推广者的阡陌点',
  `create_time` datetime NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT ' 0=表示被邀请人未注册，1=邀请人通过邀请链接注册完成',
  `register_email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invate_code` (`invate_code`),
  KEY `user_id` (`user_id`),
  KEY `invate_email` (`invate_email`)
) ENGINE=MyISAM AUTO_INCREMENT=207 DEFAULT CHARSET=utf8 COMMENT='邮件方式邀请注册（入群、添加好友）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_ent`
--

DROP TABLE IF EXISTS `kx_ent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_ent` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '企业ID',
  `ent_name` varchar(40) NOT NULL COMMENT '企业名称',
  `ent_country` varchar(15) DEFAULT NULL COMMENT '企业所在国家',
  `ent_province` varchar(15) DEFAULT NULL COMMENT '企业所在省份',
  `ent_city` varchar(15) DEFAULT NULL COMMENT '企业所在城市',
  `ent_address` varchar(70) DEFAULT NULL COMMENT '企业通信地址',
  `ent_zipcode` char(7) DEFAULT NULL COMMENT '企业邮编',
  `ent_contact1_nick` varchar(10) DEFAULT NULL COMMENT '企业联系人1(本业务联系人)',
  `ent_contact1_tel` varchar(40) DEFAULT NULL COMMENT '联系人1电话,多个用半角逗号',
  `ent_contact1_phone` varchar(40) DEFAULT NULL COMMENT '联系人1手机,多个用半角逗号',
  `ent_contact2_nick` varchar(10) DEFAULT NULL COMMENT '企业联系人2(本业务联系人)',
  `ent_contact2_tel` varchar(40) DEFAULT NULL,
  `ent_contact2_phone` varchar(40) DEFAULT NULL,
  `ent_reg_date` datetime NOT NULL COMMENT '企业注册时间,',
  `ent_status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '企业状态,',
  `ent_setup_indexMaxFileSize` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '索引的最大文件值,单位K',
  `ent_user_num` int(11) NOT NULL DEFAULT '1' COMMENT '企业用户数',
  `ent_master_id` varchar(32) NOT NULL COMMENT '企业管理员ID',
  `create_time` datetime NOT NULL COMMENT '信息录入时间',
  `update_time` datetime NOT NULL COMMENT '信息修改时间',
  `version` int(11) NOT NULL DEFAULT '0' COMMENT '策略版本号',
  PRIMARY KEY (`id`),
  KEY `ent_city` (`ent_country`,`ent_province`,`ent_city`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='企业信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_ent_user`
--

DROP TABLE IF EXISTS `kx_ent_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_ent_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL,
  `ent_id` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '企业用户状态',
  `update_time` datetime NOT NULL COMMENT '最近修改时间',
  `updater_id` varchar(32) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ent_user_index` (`user_id`,`ent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COMMENT='企业--用户关系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_forum_forum`
--

DROP TABLE IF EXISTS `kx_forum_forum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_forum_forum` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(20) NOT NULL COMMENT '版块名称',
  `posts_num` int(11) NOT NULL DEFAULT '0' COMMENT '版块帖子数',
  `order_num` int(11) NOT NULL DEFAULT '0' COMMENT '版块顺序（数字大的排在前面）',
  `updater_id` varchar(32) NOT NULL,
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `order_num` (`order_num`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='论坛版块';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_forum_mpost`
--

DROP TABLE IF EXISTS `kx_forum_mpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_forum_mpost` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主帖ID',
  `forum_id` int(11) NOT NULL COMMENT '所属版块ID',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '帖子标题',
  `user_id` varchar(32) NOT NULL,
  `reply_num` int(11) NOT NULL DEFAULT '0' COMMENT '主题帖的回复数',
  `view_num` int(11) NOT NULL DEFAULT '0' COMMENT '主题帖的访问数',
  `top_num` int(11) NOT NULL DEFAULT '0' COMMENT '置顶 数字越大越在前',
  `is_fine` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否加精 1表示有',
  `attach` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0表示有帖子下无附件，1=有图片附件，2=其他附件，3=两者都有',
  `posts_type` tinyint(4) NOT NULL DEFAULT '1' COMMENT '帖子类型 1=普通帖，2=投票帖',
  `is_del` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除帖子 1=删除',
  `create_time` datetime NOT NULL COMMENT '发帖时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  `last_time` datetime NOT NULL COMMENT '最新回帖时间',
  `last_uid` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `top_num` (`top_num`),
  KEY `forum_id` (`forum_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='论坛主帖';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_forum_posts`
--

DROP TABLE IF EXISTS `kx_forum_posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_forum_posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `forum_id` int(11) NOT NULL COMMENT '所属版块ID',
  `tid` int(11) NOT NULL COMMENT '主帖ID',
  `title` varchar(100) NOT NULL DEFAULT '' COMMENT '帖子标题',
  `content` text NOT NULL COMMENT '帖子内容',
  `user_id` varchar(32) NOT NULL,
  `reply_id` int(11) NOT NULL DEFAULT '0' COMMENT '回复的帖子ID',
  `is_main` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是主帖',
  `user_ip` varchar(15) NOT NULL COMMENT '发帖用户IP',
  `is_del` tinyint(1) NOT NULL DEFAULT '0' COMMENT '删除帖子 1=删除',
  `create_time` datetime NOT NULL COMMENT '发帖时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `create_time` (`create_time`),
  KEY `reply_id` (`reply_id`),
  KEY `forum_id` (`forum_id`),
  KEY `tid` (`tid`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='论坛帖子';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_group`
--

DROP TABLE IF EXISTS `kx_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_group` (
  `groupid` int(11) NOT NULL,
  `groupname` varchar(50) NOT NULL,
  `founder` varchar(50) NOT NULL,
  `eff` tinyint(4) NOT NULL DEFAULT '0',
  `eff_date` date NOT NULL,
  `create_date` date NOT NULL,
  `mem_nums` int(11) NOT NULL DEFAULT '1',
  `max_members` int(11) DEFAULT '50',
  `grade` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`groupid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_groupmembers`
--

DROP TABLE IF EXISTS `kx_groupmembers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_groupmembers` (
  `groupid` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `join_time` date NOT NULL,
  `indentity` int(11) NOT NULL DEFAULT '0',
  UNIQUE KEY `gm_unique_index` (`groupid`,`email`),
  KEY `groupmember_index` (`groupid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_invate_record`
--

DROP TABLE IF EXISTS `kx_invate_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_invate_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL COMMENT '注册用户ID',
  `invate_id` varchar(32) NOT NULL COMMENT '推广ID',
  `qianmo_dot` int(11) NOT NULL COMMENT '赠送推广者的阡陌点',
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`qianmo_dot`,`user_id`),
  KEY `invate_id` (`invate_id`)
) ENGINE=MyISAM AUTO_INCREMENT=133 DEFAULT CHARSET=utf8 COMMENT='推广注册记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_lan_day`
--

DROP TABLE IF EXISTS `kx_lan_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_lan_day` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tongji_day` date NOT NULL COMMENT '统计日期',
  `lan_num` int(11) NOT NULL DEFAULT '0' COMMENT '局域网数',
  `pc1` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数1',
  `pc2` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数2-5',
  `pc3` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数6-10',
  `pc4` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数11-20',
  `pc5` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数21-30',
  `pc6` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数31-50',
  `pc7` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数50以上',
  `qm1` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数1',
  `qm2` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数2-5',
  `qm3` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数6-10',
  `qm4` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数11-20',
  `qm5` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数21-30',
  `qm6` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数31-50',
  `qm7` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌数50以上',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tongji_day` (`tongji_day`)
) ENGINE=MyISAM AUTO_INCREMENT=276 DEFAULT CHARSET=utf8 COMMENT='局域网数据统计';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_lan_tongji`
--

DROP TABLE IF EXISTS `kx_lan_tongji`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_lan_tongji` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL COMMENT '局域网外网IP',
  `tongji_day` date NOT NULL COMMENT '统计日期',
  `pc_num` int(11) NOT NULL DEFAULT '0' COMMENT '电脑数',
  `qm_num` int(11) NOT NULL DEFAULT '0' COMMENT '阡陌装机数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_day` (`ip`,`tongji_day`)
) ENGINE=MyISAM AUTO_INCREMENT=313604 DEFAULT CHARSET=utf8 COMMENT='局域网数据统计';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_login_record`
--

DROP TABLE IF EXISTS `kx_login_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_login_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_day` date NOT NULL,
  `login_num` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login_day` (`login_day`)
) ENGINE=MyISAM AUTO_INCREMENT=431 DEFAULT CHARSET=utf8 COMMENT='每日注册用户登录记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_mailing_addfriend`
--

DROP TABLE IF EXISTS `kx_mailing_addfriend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_mailing_addfriend` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(50) NOT NULL,
  `friend` varchar(50) NOT NULL,
  `invite_msg` varchar(200) NOT NULL,
  `create_time` datetime NOT NULL,
  `is_sendemail` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `send_who` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0=friend; 1=user; 2=all;',
  `send_reason_type` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0=friend is unregister when user invite;1=friend is offline when user invite; 2=user is offline when friend agree;',
  `invite_content` varchar(200) DEFAULT NULL,
  `is_del` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5311 DEFAULT CHARSET=utf8 COMMENT='the record for user adding unregister friend';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_msg_board`
--

DROP TABLE IF EXISTS `kx_msg_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_msg_board` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(15) NOT NULL COMMENT '留言用户IP',
  `msg` varchar(500) NOT NULL,
  `create_time` datetime NOT NULL COMMENT '留言时间',
  `reply_id` int(11) NOT NULL DEFAULT '0' COMMENT '要回复的留言ID，0表示新的留言',
  `is_del` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否删除，0=未删除，1=删除',
  `user_id` varchar(32) NOT NULL DEFAULT '0' COMMENT '留言用户ID',
  `user_nick` varchar(50) NOT NULL DEFAULT '--',
  PRIMARY KEY (`id`),
  KEY `create_time` (`create_time`),
  KEY `reply_id` (`reply_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2583 DEFAULT CHARSET=utf8 COMMENT='留言板';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_org`
--

DROP TABLE IF EXISTS `kx_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_org` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `parent_id` int(11) NOT NULL COMMENT '上级岗位ID',
  `ent_id` int(11) NOT NULL COMMENT '企业ID',
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `updater_id` varchar(32) NOT NULL COMMENT '最后修改人（管理员）ID user.id',
  PRIMARY KEY (`id`),
  KEY `org_parentId` (`parent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='企业角色（组织结构）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_org_self`
--

DROP TABLE IF EXISTS `kx_org_self`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_org_self` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL COMMENT '用户ID',
  `target_user_id` varchar(32) NOT NULL COMMENT '查看该用户的其他用户ID',
  `ent_id` int(11) NOT NULL COMMENT '浼佷笟ID',
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `updater_id` varchar(32) NOT NULL COMMENT '最后修改人（管理员）ID user.id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `org_self_index` (`user_id`,`target_user_id`,`ent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=88 DEFAULT CHARSET=utf8 COMMENT='企业用户定义权限（用户与用户的权限的关系，也会影响企业权限版本号）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_pub`
--

DROP TABLE IF EXISTS `kx_pub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_pub` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ver` varchar(30) NOT NULL COMMENT '版本号',
  `pub_desc` varchar(600) NOT NULL COMMENT '功能描述',
  `install_file` varchar(100) DEFAULT NULL COMMENT '安装包路径',
  `install_md5` varchar(32) DEFAULT NULL COMMENT '安装包MD5',
  `patch_file` varchar(100) DEFAULT NULL COMMENT '补丁包路径',
  `patch_md5` varchar(32) DEFAULT NULL COMMENT 'patch补丁包MD5',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `pub_time` datetime DEFAULT NULL COMMENT '发布时间',
  `is_tongji` tinyint(1) NOT NULL DEFAULT '0' COMMENT '当前数据是否统计过',
  `is_publish` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否发布',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ver` (`ver`)
) ENGINE=MyISAM AUTO_INCREMENT=47 DEFAULT CHARSET=utf8 COMMENT='版本发布';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_pub_record`
--

DROP TABLE IF EXISTS `kx_pub_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_pub_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL COMMENT '登录用户email',
  `tongji_time` datetime NOT NULL COMMENT '统计时间',
  `obj` tinyint(4) NOT NULL DEFAULT '0' COMMENT '统计对象1=文件传输，2=打印，3=聊天，4=好友',
  `obj_val` int(11) NOT NULL DEFAULT '0' COMMENT '统计值',
  PRIMARY KEY (`id`),
  KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=416296 DEFAULT CHARSET=utf8 COMMENT='发布后新用户信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_pub_tongji`
--

DROP TABLE IF EXISTS `kx_pub_tongji`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_pub_tongji` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pub_id` int(11) NOT NULL COMMENT '版本发布ID',
  `reg_num` int(11) NOT NULL DEFAULT '0' COMMENT '发布24小时内注册用户数',
  `act_num` int(11) NOT NULL DEFAULT '0' COMMENT '激活用户数',
  `un_num` int(11) NOT NULL DEFAULT '0' COMMENT '卸载数',
  `vc_val` decimal(2,2) NOT NULL DEFAULT '0.00' COMMENT '病毒传播系数',
  `trans0` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输>0次',
  `trans1` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输1次',
  `trans2` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输2-4次',
  `trans3` int(11) NOT NULL DEFAULT '0' COMMENT '文件传输5次及以上',
  `print0` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数>0',
  `print1` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数1',
  `print2` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数2',
  `print3` int(11) NOT NULL DEFAULT '0' COMMENT '打印次数5及以上',
  `chat0` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数>0',
  `chat1` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数1',
  `chat2` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数2-4',
  `chat3` int(11) NOT NULL DEFAULT '0' COMMENT '聊天对话人数5及以上',
  `friend0` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数>0',
  `friend1` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数1',
  `friend2` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数2-4',
  `friend3` int(11) NOT NULL DEFAULT '0' COMMENT '好友人数5及以上',
  `invite0` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数>0',
  `invite1` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数1',
  `invite2` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数2-3',
  `invite3` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数4-5',
  `invite4` int(11) NOT NULL DEFAULT '0' COMMENT '邀请好友人数6及以上',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pub_id` (`pub_id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='发布24小时内新注册用户信息统计';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_share`
--

DROP TABLE IF EXISTS `kx_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(45) NOT NULL,
  `share_name` varchar(260) NOT NULL,
  `size` varchar(25) NOT NULL,
  `owner_email` varchar(50) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `info` varchar(430) NOT NULL,
  `Comment_count` int(10) unsigned NOT NULL DEFAULT '0',
  `owner_mac` varchar(100) NOT NULL,
  `is_del` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `owner_kx_user_id` int(10) unsigned DEFAULT NULL,
  `share_file_type` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '0=normal folder,1=normal file',
  PRIMARY KEY (`id`,`uuid`)
) ENGINE=MyISAM AUTO_INCREMENT=16486 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_share_comment`
--

DROP TABLE IF EXISTS `kx_share_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share_comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kx_share_id` int(10) unsigned NOT NULL,
  `content` varchar(430) NOT NULL,
  `creater_email` varchar(50) NOT NULL,
  `create_time` datetime NOT NULL,
  `creater_kx_user_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=269 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_share_follow`
--

DROP TABLE IF EXISTS `kx_share_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share_follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kx_share_id` int(10) unsigned NOT NULL,
  `follower_email` varchar(50) NOT NULL,
  `follow_type` tinyint(3) unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  `follower_kx_user_id` int(10) unsigned DEFAULT NULL,
  `is_join_discussion` tinyint(3) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28402 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_soft_ad`
--

DROP TABLE IF EXISTS `kx_soft_ad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_soft_ad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `ad_url` varchar(200) NOT NULL,
  `exp_day` date NOT NULL,
  `creater_id` varchar(32) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exp_day` (`exp_day`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COMMENT='软件轮播广告';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_soft_bug`
--

DROP TABLE IF EXISTS `kx_soft_bug`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_soft_bug` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_identifie` varchar(32) NOT NULL COMMENT '客户端标识（mac）',
  `version` varchar(10) NOT NULL COMMENT '软件版本',
  `upload_time` datetime NOT NULL COMMENT 'bug上传时间',
  `os` varchar(50) NOT NULL COMMENT '操作系统',
  `auto_start` tinyint(1) NOT NULL COMMENT '是否开机启动 1=是',
  `lan_num` int(11) NOT NULL DEFAULT '0' COMMENT '局域网成员数',
  `u_email` varchar(50) DEFAULT NULL COMMENT '注册账号',
  PRIMARY KEY (`id`),
  KEY `version` (`version`),
  KEY `clientIdentifie` (`client_identifie`),
  KEY `clientIdentifie_time` (`client_identifie`,`upload_time`),
  KEY `os` (`os`)
) ENGINE=MyISAM AUTO_INCREMENT=12920 DEFAULT CHARSET=utf8 COMMENT='软件BUG记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_soft_record`
--

DROP TABLE IF EXISTS `kx_soft_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_soft_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_identifie` varchar(32) NOT NULL,
  `version` varchar(10) NOT NULL,
  `login_time` datetime NOT NULL,
  `is_new` tinyint(1) NOT NULL DEFAULT '0',
  `is_uninstall` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `version` (`version`),
  KEY `clientIdentifie` (`client_identifie`),
  KEY `clientIdentifie_loginTime` (`client_identifie`,`login_time`)
) ENGINE=MyISAM AUTO_INCREMENT=1411274 DEFAULT CHARSET=utf8 COMMENT='软件使用记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_soft_utime`
--

DROP TABLE IF EXISTS `kx_soft_utime`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_soft_utime` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_identifie` varchar(32) NOT NULL COMMENT '客户端mac',
  `tongji_day` date NOT NULL COMMENT '统计日期',
  `utime` int(11) NOT NULL DEFAULT '0' COMMENT '当日使用时间长',
  `create_time` datetime NOT NULL COMMENT '记录上传时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `clientIdentifie_day` (`client_identifie`,`tongji_day`)
) ENGINE=MyISAM AUTO_INCREMENT=371697 DEFAULT CHARSET=utf8 COMMENT='软件登录时长';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_storehouse`
--

DROP TABLE IF EXISTS `kx_storehouse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_storehouse` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(45) NOT NULL,
  `name` varchar(260) NOT NULL,
  `owner_kx_user_auto_id` int(10) unsigned NOT NULL,
  `owner_email` varchar(50) NOT NULL,
  `owner_mac` varchar(100) NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime DEFAULT NULL,
  `valid_date` datetime NOT NULL,
  `is_valid` tinyint(3) unsigned NOT NULL,
  `store_size` varchar(25) DEFAULT NULL COMMENT 'M',
  `store_info` varchar(430) DEFAULT NULL,
  `is_del` tinyint(3) unsigned DEFAULT '0',
  PRIMARY KEY (`id`,`uuid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_storehouse_follower`
--

DROP TABLE IF EXISTS `kx_storehouse_follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_storehouse_follower` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `kx_storehouse_id` int(10) unsigned NOT NULL,
  `follower_kx_user_auto_id` int(10) unsigned NOT NULL,
  `follower_email` varchar(50) NOT NULL,
  `follow_type` tinyint(3) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=257 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_storehouse_manage_log`
--

DROP TABLE IF EXISTS `kx_storehouse_manage_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_storehouse_manage_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `syncfolder_id` int(10) unsigned NOT NULL,
  `operater_email` varchar(50) NOT NULL,
  `operate_time` datetime NOT NULL,
  `operate_type` tinyint(3) unsigned NOT NULL,
  `store_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_storehouse_syncfolder`
--

DROP TABLE IF EXISTS `kx_storehouse_syncfolder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_storehouse_syncfolder` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `uuid` varchar(45) NOT NULL,
  `name` varchar(260) NOT NULL,
  `owner_email` varchar(50) NOT NULL,
  `owner_mac` varchar(100) NOT NULL,
  `create_time` datetime NOT NULL,
  `store_id` int(10) unsigned NOT NULL,
  `is_del` tinyint(3) unsigned NOT NULL,
  `folder_name_on_store` varchar(260) NOT NULL,
  `folder_path_on_store` varchar(260) NOT NULL,
  PRIMARY KEY (`id`,`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=199 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_storehouse_syncfolder_follower`
--

DROP TABLE IF EXISTS `kx_storehouse_syncfolder_follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_storehouse_syncfolder_follower` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `store_sync_id` int(10) unsigned NOT NULL,
  `follower_email` varchar(45) NOT NULL,
  `follow_type` tinyint(3) unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  `follower_kx_user_auto_id` int(10) unsigned NOT NULL,
  `subdir` varchar(260) NOT NULL,
  `file_type` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_system_info`
--

DROP TABLE IF EXISTS `kx_system_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_system_info` (
  `info_name` varchar(20) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`info_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_tongji_record`
--

DROP TABLE IF EXISTS `kx_tongji_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_tongji_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tongji_day` date NOT NULL COMMENT '统计日期',
  `new_num` int(11) NOT NULL DEFAULT '0' COMMENT '当天新用户数',
  `un_num` int(11) NOT NULL DEFAULT '0' COMMENT '当天卸载用户数',
  `seven_new_num` int(11) NOT NULL DEFAULT '0' COMMENT '七天新装用户总数',
  `seven_un_num` int(11) NOT NULL DEFAULT '0' COMMENT '七天卸载用户总数',
  `last_mon_num` int(11) NOT NULL DEFAULT '0' COMMENT '上月上线用户数（15天）',
  `cur_mon_num` int(11) NOT NULL DEFAULT '0' COMMENT '上月已上线用户数在本月中上线数（15天）',
  `no_login_num` int(11) NOT NULL DEFAULT '0' COMMENT '30天内已激活未登录注册用户数',
  `all_num` int(11) NOT NULL DEFAULT '0' COMMENT '当天总用户',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tongji_day` (`tongji_day`)
) ENGINE=MyISAM AUTO_INCREMENT=354 DEFAULT CHARSET=utf8 COMMENT='统计记录 每日新用户、卸载用户、7天卸载率记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user`
--

DROP TABLE IF EXISTS `kx_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(32) NOT NULL,
  `email` varchar(50) NOT NULL COMMENT '用户名为邮箱',
  `nick` varchar(20) NOT NULL COMMENT '用户昵称',
  `password` varchar(50) NOT NULL COMMENT '密码',
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '0=表示未激活，1=正常，2=封禁',
  `create_time` datetime NOT NULL COMMENT '注册时间',
  `last_login` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `avatar` varchar(200) DEFAULT NULL,
  `last_ip` varchar(50) DEFAULT NULL,
  `mobile` varchar(20) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `login_status` int(11) NOT NULL DEFAULT '0',
  `qianmo_dot` int(11) NOT NULL DEFAULT '0' COMMENT '现有阡陌点',
  `con_qianmo_dot` int(11) NOT NULL DEFAULT '0' COMMENT '累计消费阡陌点',
  `invate_init` tinyint(4) NOT NULL DEFAULT '0' COMMENT '0=未登录，1=邀请用户登录并初始化成功，2=非邀请用户',
  `login_counts` int(11) NOT NULL DEFAULT '0',
  `create_group_counts` int(11) NOT NULL DEFAULT '0',
  `online_time` int(11) NOT NULL DEFAULT '0',
  `invites` int(11) NOT NULL DEFAULT '0',
  `user_share` int(11) NOT NULL DEFAULT '0',
  `share_begin_time` date DEFAULT NULL,
  `active_time` datetime DEFAULT NULL COMMENT '激活时间',
  `last_lan_ip` varchar(50) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否是超级用户',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '是否激活',
  `is_staff` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否能登陆Django Admin',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`email`),
  KEY `user_index_2` (`email`,`password`,`status`),
  KEY `uuid_index` (`uuid`)
) ENGINE=MyISAM AUTO_INCREMENT=29484 DEFAULT CHARSET=utf8 COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user_friend`
--

DROP TABLE IF EXISTS `kx_user_friend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user_friend` (
  `user` varchar(50) DEFAULT NULL,
  `friend` varchar(50) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user` (`user`,`friend`),
  KEY `friend_index` (`user`)
) ENGINE=MyISAM AUTO_INCREMENT=58214 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user_groups`
--

DROP TABLE IF EXISTS `kx_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kxuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kxuser_id` (`kxuser_id`,`group_id`),
  KEY `kx_user_groups_1eba34a9` (`kxuser_id`),
  KEY `kx_user_groups_5f412f9a` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user_org`
--

DROP TABLE IF EXISTS `kx_user_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user_org` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) NOT NULL,
  `org_id` int(11) NOT NULL DEFAULT '-1' COMMENT '企业角色ID',
  `ent_id` int(11) NOT NULL,
  `update_time` datetime NOT NULL COMMENT '最近修改时间',
  `updater_id` varchar(32) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_org_index` (`user_id`,`org_id`,`ent_id`)
) ENGINE=MyISAM AUTO_INCREMENT=112 DEFAULT CHARSET=utf8 COMMENT='用户企业角色关系表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user_user_permissions`
--

DROP TABLE IF EXISTS `kx_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kxuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kxuser_id` (`kxuser_id`,`permission_id`),
  KEY `kx_user_user_permissions_1eba34a9` (`kxuser_id`),
  KEY `kx_user_user_permissions_83d7f98b` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_userlogin`
--

DROP TABLE IF EXISTS `kx_userlogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_userlogin` (
  `email` varchar(50) NOT NULL,
  `mac` varchar(100) NOT NULL,
  `lan_ip` varchar(50) DEFAULT NULL,
  `wlan_ip` varchar(50) DEFAULT NULL,
  UNIQUE KEY `email` (`email`,`mac`),
  KEY `login_index` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `online_user_onlineuser`
--

DROP TABLE IF EXISTS `online_user_onlineuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `online_user_onlineuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `owner_email` varchar(50) NOT NULL,
  `lan_ip` varchar(50) NOT NULL,
  `wlan_ip` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operator`
--

DROP TABLE IF EXISTS `operator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `printer_num` int(11) NOT NULL,
  `used_num` int(11) NOT NULL,
  `qq` varchar(14) NOT NULL,
  `tel` varchar(14) NOT NULL,
  `school` varchar(255) DEFAULT NULL,
  `resource` longtext NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  `expire` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `operator_6f33f001` (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operator_assistant`
--

DROP TABLE IF EXISTS `operator_assistant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operator_assistant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `operator_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `operator_assistant_5e7ba3ec` (`operator_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `operator_category`
--

DROP TABLE IF EXISTS `operator_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `operator_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `cid` int(11) NOT NULL,
  `ordering` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `order_info`
--

DROP TABLE IF EXISTS `order_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `order_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` varchar(20) NOT NULL,
  `create_at` datetime NOT NULL,
  `buy_user` varchar(50) NOT NULL,
  `buy_product_id` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `auth_user_num` int(11) NOT NULL DEFAULT '0' COMMENT '购买打印机台数',
  `total_fee` decimal(10,2) NOT NULL,
  `pay_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '付款状态',
  `pay_at` datetime NOT NULL,
  `trade_no` varchar(64) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '订单处理状态',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`),
  KEY `order_info_9dc4d252` (`buy_product_id`),
  KEY `order_info_5997a794` (`trade_no`)
) ENGINE=MyISAM AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `print`
--

DROP TABLE IF EXISTS `print`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `print` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `is_print` tinyint(1) NOT NULL,
  `print_num` int(11) NOT NULL,
  `used_print_num` int(11) NOT NULL,
  `create_at` datetime NOT NULL,
  `expire` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `print_access`
--

DROP TABLE IF EXISTS `print_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `print_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `access_user` varchar(50) NOT NULL,
  `create_at` datetime NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `print_access_830a6ccb` (`email`),
  KEY `print_access_ee64d3ef` (`access_user`)
) ENGINE=MyISAM AUTO_INCREMENT=1003 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `print_fzu`
--

DROP TABLE IF EXISTS `print_fzu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `print_fzu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `print_pop`
--

DROP TABLE IF EXISTS `print_pop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `print_pop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `create_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `print_spool`
--

DROP TABLE IF EXISTS `print_spool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `print_spool` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(50) NOT NULL,
  `origin_email` varchar(50) NOT NULL,
  `origin_uuid` varchar(260) NOT NULL,
  `accept_email` varchar(50) NOT NULL,
  `accept_uuid` varchar(260) NOT NULL,
  `printer_name` varchar(260) NOT NULL,
  `printer_uuid` varchar(260) NOT NULL,
  `file_name` varchar(260) NOT NULL,
  `file_path` varchar(260) NOT NULL,
  `file_client_path` varchar(260) NOT NULL,
  `page_num` int(11) NOT NULL,
  `print_time` datetime NOT NULL,
  `status` int(11) NOT NULL,
  `create_at` datetime NOT NULL,
  `status_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=MyISAM AUTO_INCREMENT=4528 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_info`
--

DROP TABLE IF EXISTS `product_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `slug` varchar(50) DEFAULT NULL COMMENT '标签',
  `category` int(11) NOT NULL DEFAULT '0' COMMENT '产品分类',
  `desc` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stocked` int(11) NOT NULL,
  `order_num` int(11) DEFAULT '0' COMMENT '排序值',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `publish_user`
--

DROP TABLE IF EXISTS `publish_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `publish_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `ver` int(11) NOT NULL,
  `repo_ver` int(11) NOT NULL,
  `is_publish` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `publish_user_d0b741e1` (`ver`),
  KEY `publish_user_e7ff3a12` (`repo_ver`)
) ENGINE=MyISAM AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shared`
--

DROP TABLE IF EXISTS `shared`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shared` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `is_shared` tinyint(1) NOT NULL,
  `shared_num` int(11) NOT NULL,
  `used_shared_num` int(11) NOT NULL,
  `create_at` datetime NOT NULL,
  `expire` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shared_access`
--

DROP TABLE IF EXISTS `shared_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shared_access` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `access_user` varchar(50) NOT NULL,
  `create_at` datetime NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shared_access_830a6ccb` (`email`),
  KEY `shared_access_ee64d3ef` (`access_user`)
) ENGINE=MyISAM AUTO_INCREMENT=746 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_msg`
--

DROP TABLE IF EXISTS `user_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_msg` (
  `user` varchar(50) DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `content` varchar(2000) DEFAULT NULL,
  `from_email` varchar(50) NOT NULL,
  KEY `msg_index` (`user`,`title`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vipuser`
--

DROP TABLE IF EXISTS `vipuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vipuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL,
  `is_vip` tinyint(1) NOT NULL,
  `create_at` datetime NOT NULL COMMENT '创建时间',
  `expire` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-18 11:22:21
