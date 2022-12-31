-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: fast_stock
-- ------------------------------------------------------
-- Server version	5.7.39

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
-- Table structure for table `stock_basic_info`
--

DROP TABLE IF EXISTS `stock_basic_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_basic_info` (
  `index` bigint(20) DEFAULT NULL,
  `ts_code` text,
  `code` text,
  `name` text,
  `area` text,
  `industry` text,
  `market` text,
  `list_date` text,
  `update_date` datetime DEFAULT NULL,
  KEY `ix_stock_basic_info_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_basic_status`
--

DROP TABLE IF EXISTS `stock_basic_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_basic_status` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index` bigint(20) DEFAULT NULL COMMENT 'basic_info 表序号',
  `ts_code` varchar(10) DEFAULT NULL COMMENT '股票代码',
  `line_type` varchar(10) DEFAULT NULL COMMENT 'day|5min|15min',
  `sync_status` tinyint(4) DEFAULT NULL COMMENT '0:未开始;1:进行中;2:完成;3:失败',
  `last_value` varchar(50) DEFAULT NULL COMMENT '最后同步到哪个时间点',
  `last_success_date` datetime DEFAULT NULL COMMENT '最后同步作业行运日期',
  `order_index` int(11) DEFAULT NULL COMMENT '排序，越小优先级越高',
  `app_mode` tinyint(4) DEFAULT NULL COMMENT '1:增量同步;2:全量同步;临时全量同步',
  `degree` int(11) DEFAULT NULL COMMENT '值越小关注程度越高',
  `allow_delay_second` int(11) DEFAULT NULL COMMENT '允许延迟同步的秒数',
  `label` varchar(50) DEFAULT NULL COMMENT '自定义打标记',
  `record_status` tinyint(1) NOT NULL COMMENT '状态(0,初始化;1,可用;2,不可用;)',
  `remark` varchar(50) DEFAULT NULL COMMENT '备注',
  `created_on` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_on` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5025 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='基本信息状态表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stock_line_day`
--

DROP TABLE IF EXISTS `stock_line_day`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stock_line_day` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `index` bigint(20) DEFAULT NULL,
  `ts_code` varchar(12) DEFAULT NULL,
  `trade_date` varchar(20) DEFAULT NULL,
  `open` float(10,2) DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `pre_close` float DEFAULT NULL,
  `change` float DEFAULT NULL,
  `pct_chg` float DEFAULT NULL,
  `vol` float DEFAULT NULL,
  `amount` float DEFAULT NULL,
  KEY `ix_tb_daily_index` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12663590 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'fast_stock'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-11 14:15:59

create index idx_ts_code on stock_line_day(ts_code);