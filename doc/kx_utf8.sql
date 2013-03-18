-- MySQL dump 10.13  Distrib 5.5.30, for Linux (x86_64)
--
-- Host: localhost    Database: kx
-- ------------------------------------------------------
-- Server version	5.5.30-log

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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='每日上线注册用户行为统计信息';
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
  `user_id` int(11) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=12329 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_email_invate`
--

DROP TABLE IF EXISTS `kx_email_invate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_email_invate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '邀请人用户ID',
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
  `ent_master_id` int(11) NOT NULL COMMENT '企业管理员ID',
  `create_time` datetime NOT NULL COMMENT '信息录入时间',
  `update_time` datetime NOT NULL COMMENT '信息修改时间',
  `version` int(11) NOT NULL DEFAULT '0' COMMENT '策略版本号',
  PRIMARY KEY (`id`),
  KEY `ent_city` (`ent_country`,`ent_province`,`ent_city`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='企业信息';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_ent_user`
--

DROP TABLE IF EXISTS `kx_ent_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_ent_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `ent_id` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '企业用户状态',
  `update_time` datetime NOT NULL COMMENT '最近修改时间',
  `updater_id` int(11) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ent_user_index` (`user_id`,`ent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COMMENT='企业--用户关系表';
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
  `updater_id` int(11) NOT NULL COMMENT '更新用户',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `order_num` (`order_num`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='论坛版块';
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
  `user_id` int(11) NOT NULL COMMENT '发帖用户',
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
  `last_uid` int(11) NOT NULL COMMENT '最新回帖用户',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `top_num` (`top_num`),
  KEY `forum_id` (`forum_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='论坛主帖';
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
  `user_id` int(11) NOT NULL COMMENT '发帖用户',
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COMMENT='论坛帖子';
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
  `user_id` int(11) NOT NULL COMMENT '注册用户ID',
  `invate_id` int(11) NOT NULL COMMENT '推广ID',
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
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COMMENT='局域网数据统计';
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
) ENGINE=InnoDB AUTO_INCREMENT=24025 DEFAULT CHARSET=utf8 COMMENT='局域网数据统计';
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
) ENGINE=MyISAM AUTO_INCREMENT=196 DEFAULT CHARSET=utf8 COMMENT='每日注册用户登录记录';
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
) ENGINE=InnoDB AUTO_INCREMENT=425 DEFAULT CHARSET=utf8 COMMENT='the record for user adding unregister friend';
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
  `user_id` int(11) NOT NULL DEFAULT '0',
  `user_nick` varchar(50) NOT NULL DEFAULT '--',
  PRIMARY KEY (`id`),
  KEY `create_time` (`create_time`),
  KEY `reply_id` (`reply_id`)
) ENGINE=MyISAM AUTO_INCREMENT=855 DEFAULT CHARSET=utf8 COMMENT='留言板';
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
  `updater_id` int(11) NOT NULL COMMENT '最后修改人（管理员）ID user.id',
  PRIMARY KEY (`id`),
  KEY `org_parentId` (`parent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COMMENT='企业角色（组织结构）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_org_self`
--

DROP TABLE IF EXISTS `kx_org_self`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_org_self` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `target_user_id` int(11) NOT NULL COMMENT '查看该用户的其他用户ID',
  `ent_id` int(11) NOT NULL COMMENT '企业ID',
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `updater_id` int(11) NOT NULL COMMENT '最后修改人（管理员）ID user.id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `org_self_index` (`user_id`,`target_user_id`,`ent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8 COMMENT='企业用户定义权限（用户与用户的权限的关系，也会影响企业权限版本号）';
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
  `patch_file` varchar(100) DEFAULT NULL COMMENT '补丁包路径',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `pub_time` datetime DEFAULT NULL COMMENT '发布时间',
  `is_tongji` tinyint(1) NOT NULL DEFAULT '0' COMMENT '当前数据是否统计过',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ver` (`ver`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='版本发布';
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
) ENGINE=InnoDB AUTO_INCREMENT=13312 DEFAULT CHARSET=utf8 COMMENT='发布后新用户信息';
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COMMENT='发布24小时内新注册用户信息统计';
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
  `creater_id` int(11) NOT NULL,
  `create_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exp_day` (`exp_day`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COMMENT='软件轮播广告';
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
) ENGINE=MyISAM AUTO_INCREMENT=1060 DEFAULT CHARSET=utf8 COMMENT='软件BUG记录';
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
) ENGINE=MyISAM AUTO_INCREMENT=496138 DEFAULT CHARSET=utf8 COMMENT='软件使用记录';
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
) ENGINE=MyISAM AUTO_INCREMENT=6358 DEFAULT CHARSET=utf8 COMMENT='软件登录时长';
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
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8 COMMENT='统计记录 每日新用户、卸载用户、7天卸载率记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user`
--

DROP TABLE IF EXISTS `kx_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_email` (`email`),
  KEY `user_index_2` (`email`,`password`,`status`)
) ENGINE=InnoDB AUTO_INCREMENT=10250 DEFAULT CHARSET=utf8 COMMENT='用户表';
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
) ENGINE=MyISAM AUTO_INCREMENT=13954 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_user_org`
--

DROP TABLE IF EXISTS `kx_user_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_user_org` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `org_id` int(11) NOT NULL DEFAULT '-1' COMMENT '企业角色ID',
  `ent_id` int(11) NOT NULL,
  `update_time` datetime NOT NULL COMMENT ' 最近修改时间',
  `updater_id` int(11) NOT NULL COMMENT '修改人',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_org_index` (`user_id`,`org_id`,`ent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8 COMMENT='用户企业角色关系表';
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
  UNIQUE KEY `email` (`email`,`mac`),
  KEY `login_index` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-03-11  2:44:27
