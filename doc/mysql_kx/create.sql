--
-- Table structure for table `kx_share`
--

DROP TABLE IF EXISTS `kx_share`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share` (
      `id` int(10) unsigned NOT NULL auto_increment,
      `uuid` varchar(45) NOT NULL,
      `share_name` varchar(260) NOT NULL,
      `size` varchar(25) NOT NULL,
      `owner_email` varchar(50) NOT NULL,
      `create_time` datetime NOT NULL,
      `update_time` datetime NOT NULL,
      `info` varchar(430) NOT NULL,
      `Comment_count` int(10) unsigned NOT NULL default '0',
      `owner_mac` varchar(100) NOT NULL,
      `is_del` tinyint(3) unsigned NOT NULL default '0',
      `owner_kx_user_id` int(10) unsigned default NULL,
      `share_file_type` tinyint(3) unsigned NOT NULL default '0' COMMENT '0=normal folder,1=normal file',
      PRIMARY KEY  (`id`,`uuid`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_share_comment`
--

DROP TABLE IF EXISTS `kx_share_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share_comment` (
      `id` int(10) unsigned NOT NULL auto_increment,
      `kx_share_id` int(10) unsigned NOT NULL,
      `content` varchar(430) NOT NULL,
      `creater_email` varchar(50) NOT NULL,
      `create_time` datetime NOT NULL,
      `creater_kx_user_id` int(10) unsigned default NULL,
      PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `kx_share_follow`
--

DROP TABLE IF EXISTS `kx_share_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kx_share_follow` (
      `id` int(10) unsigned NOT NULL auto_increment,
      `kx_share_id` int(10) unsigned NOT NULL,
      `follower_email` varchar(50) NOT NULL,
      `follow_type` tinyint(3) unsigned NOT NULL,
      `create_time` datetime NOT NULL,
      `follower_kx_user_id` int(10) unsigned default NULL,
      PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
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
  KEY `kx_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `kxuser_id_refs_id_434910cf` FOREIGN KEY (`kxuser_id`) REFERENCES `kx_user` (`id`),
  CONSTRAINT `group_id_refs_id_4d5845f5` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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
  KEY `kx_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `kxuser_id_refs_id_1bb8a2db` FOREIGN KEY (`kxuser_id`) REFERENCES `kx_user` (`id`),
  CONSTRAINT `permission_id_refs_id_087c9a86` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
