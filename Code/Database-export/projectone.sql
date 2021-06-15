-- MySQL dump 10.13  Distrib 8.0.21, for macos10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: projectdb
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `devices` (
  `id_device` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL,
  `meeteenheid` varchar(45) DEFAULT NULL,
  `status_device` tinyint DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_device`),
  UNIQUE KEY `id_device_UNIQUE` (`id_device`),
  UNIQUE KEY `naam_UNIQUE` (`naam`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,'luchtkwaliteitssensor',NULL,1,'sensor'),(2,'rotary encoder',NULL,1,'sensor'),(3,'PIR sensor',NULL,0,'sensor'),(4,'neopixel',NULL,1,'actuator'),(5,'trilmotor',NULL,1,'actuator'),(6,'buzzer speaker',NULL,1,'actuator'),(7,'lcd display',NULL,1,'actuator');
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek_devices`
--

DROP TABLE IF EXISTS `historiek_devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek_devices` (
  `volgnummer_devicehistoriek` int NOT NULL AUTO_INCREMENT,
  `id_device` int NOT NULL,
  `datum_meting` datetime NOT NULL,
  `meetresultaat` float DEFAULT NULL,
  PRIMARY KEY (`volgnummer_devicehistoriek`),
  UNIQUE KEY `datum_meting_UNIQUE` (`datum_meting`),
  UNIQUE KEY `volgnummer_devicehistoriek_UNIQUE` (`volgnummer_devicehistoriek`),
  KEY `FK_deviceid_idx` (`id_device`),
  CONSTRAINT `FK_deviceid` FOREIGN KEY (`id_device`) REFERENCES `devices` (`id_device`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek_devices`
--

LOCK TABLES `historiek_devices` WRITE;
/*!40000 ALTER TABLE `historiek_devices` DISABLE KEYS */;
INSERT INTO `historiek_devices` VALUES (1,1,'2021-02-09 19:29:33',NULL),(2,3,'2021-03-15 23:48:54',NULL),(3,1,'2021-04-05 05:55:57',NULL),(4,3,'2021-04-14 19:12:25',NULL),(5,1,'2021-03-12 22:51:30',NULL),(6,3,'2021-04-06 10:15:34',NULL),(7,1,'2021-01-18 10:33:09',NULL),(8,3,'2021-05-12 18:25:42',NULL),(9,1,'2021-02-15 14:52:22',NULL),(10,3,'2021-03-25 06:29:29',NULL),(11,1,'2021-01-15 02:26:27',NULL),(12,3,'2021-03-08 16:38:56',NULL),(13,1,'2021-01-12 12:04:00',NULL),(14,3,'2021-05-11 04:57:20',NULL),(15,1,'2021-04-04 22:14:32',NULL),(16,3,'2021-04-12 15:19:08',NULL),(17,1,'2021-05-18 03:23:36',NULL),(18,3,'2021-05-20 12:02:43',NULL),(19,1,'2021-02-10 09:31:51',NULL),(20,3,'2021-01-23 13:46:09',NULL),(21,1,'2021-04-19 08:47:09',NULL),(22,3,'2021-01-29 05:43:43',NULL),(23,1,'2021-02-14 00:55:38',NULL),(24,3,'2021-05-24 18:32:21',NULL),(25,1,'2021-04-21 17:47:30',NULL),(26,3,'2021-03-10 23:49:18',NULL),(27,1,'2021-05-21 00:58:32',NULL),(28,3,'2021-01-16 02:38:23',NULL),(29,1,'2021-03-20 15:30:37',NULL),(30,3,'2021-01-15 01:31:35',NULL),(31,1,'2021-03-22 02:39:12',NULL),(32,3,'2021-04-13 13:25:03',NULL),(33,1,'2021-01-30 03:17:19',NULL),(34,3,'2021-02-12 13:15:41',NULL),(35,1,'2021-02-16 22:22:08',NULL),(36,3,'2021-04-30 22:37:50',NULL),(37,1,'2021-05-07 07:10:29',NULL),(38,3,'2021-05-19 18:12:31',NULL),(39,1,'2021-04-11 21:36:51',NULL),(40,3,'2021-01-27 23:26:05',NULL),(41,1,'2021-04-15 09:46:07',NULL),(42,3,'2021-01-12 07:53:14',NULL),(43,1,'2021-02-14 15:07:25',NULL),(44,3,'2021-02-09 22:32:13',NULL),(45,1,'2021-05-01 08:22:44',NULL),(46,3,'2021-01-31 00:54:51',NULL),(47,1,'2021-05-21 18:47:47',NULL),(48,3,'2021-03-21 11:03:55',NULL),(49,1,'2021-04-06 07:36:49',NULL),(50,3,'2021-02-16 05:43:28',NULL);
/*!40000 ALTER TABLE `historiek_devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historiek_melding`
--

DROP TABLE IF EXISTS `historiek_melding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiek_melding` (
  `volgnummer_melding` int NOT NULL AUTO_INCREMENT,
  `tijd_melding` datetime NOT NULL,
  `tijd_afdrukken_melding` datetime DEFAULT NULL,
  `bericht` varchar(150) DEFAULT NULL,
  `status_melding` int NOT NULL,
  PRIMARY KEY (`volgnummer_melding`),
  UNIQUE KEY `tijd_melding_UNIQUE` (`tijd_melding`),
  UNIQUE KEY `volgnummer_melding_UNIQUE` (`volgnummer_melding`),
  UNIQUE KEY `tijd_afdrukken_melding_UNIQUE` (`tijd_afdrukken_melding`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historiek_melding`
--

LOCK TABLES `historiek_melding` WRITE;
/*!40000 ALTER TABLE `historiek_melding` DISABLE KEYS */;
INSERT INTO `historiek_melding` VALUES (1,'2021-05-06 09:26:14','2021-05-06 09:26:30','KOMEN ETEN!',1),(2,'2021-03-18 11:50:33','2021-03-18 11:50:38','KOMEN HELPEN!',2),(3,'2021-03-25 13:19:21','2021-03-25 13:19:29','KOMEN HELPEN!',3),(4,'2021-05-02 23:40:22','2021-05-02 23:40:24','We gaan samen een film kijken, dus kom maar naar beneden',1),(5,'2021-05-15 18:53:37','2021-05-15 18:53:39','We gaan samen een film kijken, dus kom maar naar beneden',2),(6,'2021-04-02 04:55:19','2021-04-02 04:55:23','KOMEN ETEN!',3),(7,'2021-04-02 04:42:27','2021-04-02 04:42:29','KOMEN HELPEN!',1),(8,'2021-01-15 11:02:27','2021-01-15 11:02:29','KOMEN ETEN!',2),(9,'2021-02-22 19:38:21','2021-02-22 19:38:26','KOMEN ETEN!',3),(10,'2021-02-22 06:43:27','2021-02-22 06:43:29','KOMEN ETEN!',1),(11,'2021-04-22 07:14:22','2021-04-22 07:14:28','KOMEN ETEN!',2),(12,'2021-05-12 18:28:23','2021-05-12 18:28:29','KOMEN ETEN!',3),(13,'2021-03-27 05:06:50','2021-03-27 05:06:53','KOMEN ETEN!',1),(14,'2021-01-07 03:39:27','2021-01-07 03:39:29','KOMEN ETEN!',2),(15,'2021-04-22 14:26:48','2021-04-22 14:26:48','KOMEN ETEN!',3),(16,'2021-02-23 01:40:45','2021-02-23 01:40:45','KOMEN ETEN!',1),(17,'2021-03-13 21:11:30','2021-03-13 21:11:30','KOMEN ETEN!',2),(18,'2021-05-14 08:21:06','2021-05-14 08:21:06','KOMEN ETEN!',3),(19,'2021-03-15 01:45:19','2021-03-15 01:45:19','KOMEN ETEN!',1),(20,'2021-05-01 08:26:39','2021-05-01 08:26:39','KOMEN HELPEN!',2),(21,'2021-04-26 07:04:43','2021-04-26 07:04:43','We gaan samen een film kijken, dus kom maar naar beneden',3),(22,'2021-02-09 10:34:37','2021-02-09 10:34:37','KOMEN HELPEN!',1),(23,'2021-04-24 19:10:46','2021-04-24 19:10:46','KOMEN ETEN!',2),(24,'2021-04-20 19:18:37','2021-04-20 19:18:37','We gaan samen een film kijken, dus kom maar naar beneden',3),(25,'2021-03-17 22:41:16','2021-03-17 22:41:16','KOMEN ETEN!',1),(26,'2021-04-24 23:17:14','2021-04-24 23:17:14','KOMEN ETEN!',2),(27,'2021-02-02 04:26:52','2021-02-02 04:26:52','We gaan samen een film kijken, dus kom maar naar beneden',3),(28,'2021-03-09 23:30:02','2021-03-09 23:30:02','KOMEN HELPEN!',1),(29,'2021-05-05 15:34:21','2021-05-05 15:34:21','KOMEN ETEN!',2),(30,'2021-04-17 20:56:42','2021-04-17 20:56:42','KOMEN ETEN!',3),(31,'2021-04-01 12:08:18','2021-04-01 12:08:18','KOMEN HELPEN!',1),(32,'2021-02-02 09:25:46','2021-02-02 09:25:46','We gaan samen een film kijken, dus kom maar naar beneden',2),(33,'2021-04-08 05:48:17','2021-04-08 05:48:17','KOMEN ETEN!',3),(34,'2021-04-20 02:00:46','2021-04-20 02:00:46','We gaan samen een film kijken, dus kom maar naar beneden',1),(35,'2021-05-16 14:36:42','2021-05-16 14:36:42','KOMEN HELPEN!',2),(36,'2021-01-18 06:46:17','2021-01-18 06:46:17','KOMEN ETEN!',3),(37,'2021-02-01 21:38:13','2021-02-01 21:38:13','KOMEN HELPEN!',1),(38,'2021-04-02 11:55:41','2021-04-02 11:55:41','KOMEN ETEN!',2),(39,'2021-05-03 19:45:59','2021-05-03 19:45:59','KOMEN ETEN!',3),(40,'2021-02-07 02:15:34','2021-02-07 02:15:34','We gaan samen een film kijken, dus kom maar naar beneden',3),(41,'2021-01-20 05:45:04','2021-01-20 05:45:04','KOMEN HELPEN!',1),(42,'2021-03-14 23:16:51','2021-03-14 23:16:51','KOMEN ETEN!',2),(43,'2021-01-29 06:06:43','2021-01-29 06:06:43','KOMEN HELPEN!',3),(44,'2021-05-01 10:16:06','2021-05-01 10:16:06','KOMEN ETEN!',1),(45,'2021-02-02 20:15:16','2021-02-02 20:15:16','We gaan samen een film kijken, dus kom maar naar beneden',2),(46,'2021-02-15 09:08:23','2021-02-15 09:08:23','KOMEN ETEN!',3),(47,'2021-02-25 00:42:34','2021-02-25 00:42:34','KOMEN HELPEN!',1),(48,'2021-04-27 19:29:44','2021-04-27 19:29:44','KOMEN ETEN!',2),(49,'2021-02-25 15:07:46','2021-02-25 15:07:46','We gaan samen een film kijken, dus kom maar naar beneden',3),(50,'2021-02-28 04:22:22','2021-02-28 04:22:22','KOMEN HELPEN!',1);
/*!40000 ALTER TABLE `historiek_melding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kamer`
--

DROP TABLE IF EXISTS `kamer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kamer` (
  `id_kamer` int NOT NULL AUTO_INCREMENT,
  `voornaam` varchar(45) NOT NULL,
  PRIMARY KEY (`id_kamer`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kamer`
--

LOCK TABLES `kamer` WRITE;
/*!40000 ALTER TABLE `kamer` DISABLE KEYS */;
INSERT INTO `kamer` VALUES (1,'Junior');
/*!40000 ALTER TABLE `kamer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-15 16:05:15
