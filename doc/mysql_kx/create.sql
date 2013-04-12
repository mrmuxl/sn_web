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
