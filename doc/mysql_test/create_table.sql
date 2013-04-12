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
  `updater_id` varchar(32) NOT NULL COMMENT '更新用户',
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
  `user_id` varchar(32) NOT NULL COMMENT '发帖用户',
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
  `last_uid` varchar(32) NOT NULL COMMENT '最新回帖用户',
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
  `user_id` varchar(32) NOT NULL COMMENT '发帖用户',
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


