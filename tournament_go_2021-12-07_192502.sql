-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: tournament_go
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cities`
--

DROP TABLE IF EXISTS `Cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cities`
--

/*!40000 ALTER TABLE `Cities` DISABLE KEYS */;
INSERT INTO `Cities` VALUES (1,'Москва'),(2,'Санкт-Петербург'),(3,'Моск.обл.'),(4,'Жуковский'),(5,'Калуга'),(6,'Калужская обл.'),(7,'Архангельск'),(8,'Астрахань'),(9,'Барнаул'),(10,'Великий Новгород'),(11,'Владивосток'),(12,'Волгоград'),(13,'Вологда'),(14,'Екатеринбург'),(15,'Ижевск'),(16,'Казань'),(17,'Калининград'),(18,'Киров'),(19,'Краснодар'),(20,'Красноярск'),(21,'Курган'),(22,'Магадан'),(23,'Нижний Новгород'),(24,'Новосибирск'),(25,'Новоуральск'),(26,'Пермь'),(27,'Петрозаводск'),(28,'Самара'),(29,'Севастополь'),(30,'Симферополь'),(31,'Суздаль'),(32,'Тверь'),(34,'Томск'),(38,'Тольятти'),(39,'Уфа'),(40,'Феодосия'),(41,'Хабаровск'),(42,'Челябинск'),(43,'Ярославль'),(44,'Тула'),(46,'КГС'),(47,'ОГС'),(48,'Badukpop'),(49,'Pandanet'),(50,'GoQuest'),(53,'Ленинградская обл.'),(55,'KGS'),(56,'OGS'),(57,'Омск'),(58,'Николаевск-на-Амуре'),(59,'Амурск');
/*!40000 ALTER TABLE `Cities` ENABLE KEYS */;

--
-- Table structure for table `UserCity`
--

DROP TABLE IF EXISTS `UserCity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserCity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) DEFAULT NULL,
  `CityID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `UserID` (`UserID`),
  KEY `CityID` (`CityID`),
  CONSTRAINT `UserCity_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user_BotGo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `UserCity_ibfk_2` FOREIGN KEY (`CityID`) REFERENCES `Cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserCity`
--

/*!40000 ALTER TABLE `UserCity` DISABLE KEYS */;
INSERT INTO `UserCity` VALUES (5,2,1);
/*!40000 ALTER TABLE `UserCity` ENABLE KEYS */;

--
-- Table structure for table `children_categories`
--

DROP TABLE IF EXISTS `children_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `children_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `categories` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `children_categories`
--

/*!40000 ALTER TABLE `children_categories` DISABLE KEYS */;
INSERT INTO `children_categories` VALUES (1,'до 9'),(2,'до 12'),(3,'до 16'),(4,'до 18'),(5,'до 20'),(6,'9-11'),(7,'12-15'),(8,'16-19'),(9,'Гран-при'),(10,'Гран при'),(11,'до 9,12,16 и 20'),(12,'до 9, 12, 16 и 20 лет'),(13,'До 9'),(14,'До 12'),(15,'До 16'),(16,'До 20'),(17,'для учащихся'),(18,'Детский'),(19,'гран-при'),(20,'гран при'),(21,'до 9 лет, 9-11 лет, 12-15 лет'),(22,'детский'),(23,'школьников'),(24,'Школьников'),(25,'Первенство'),(26,'первенство');
/*!40000 ALTER TABLE `children_categories` ENABLE KEYS */;

--
-- Table structure for table `tournament_go`
--

DROP TABLE IF EXISTS `tournament_go`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tournament_go` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `t_start` date DEFAULT NULL,
  `t_end` date DEFAULT NULL,
  `t_name` varchar(255) DEFAULT NULL,
  `CityID` int(11) DEFAULT NULL,
  `link` varchar(255) DEFAULT NULL,
  `is_child` tinyint(1) DEFAULT 0,
  `date_time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `t_name` (`t_name`),
  KEY `CityID` (`CityID`),
  CONSTRAINT `tournament_go_ibfk_1` FOREIGN KEY (`CityID`) REFERENCES `Cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4577 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament_go`
--

/*!40000 ALTER TABLE `tournament_go` DISABLE KEYS */;
INSERT INTO `tournament_go` VALUES (4209,'2021-12-25','2021-12-26','Чемпионат Республики Татарстан ',16,'https://gofederation.ru/tournaments/595050511',0,'2021-12-07 19:19:15'),(4210,'2021-12-25','2021-12-25','Зимний Амурск',59,'https://gofederation.ru/tournaments/767029750',0,'2021-12-07 19:19:15'),(4211,'2021-12-19','2021-12-19','Новогодний турнир \"Привет, Тигр!\"',41,'https://gofederation.ru/tournaments/768505503',0,'2021-12-07 19:19:15'),(4212,'2021-12-18','2021-12-19','Всероссийское соревнование \"Мемориал В.А.Асташкина\"',2,'https://gofederation.ru/tournaments/236418546',0,'2021-12-07 19:19:15'),(4213,'2021-12-18','2021-12-19','Кубок Посла Китая по вэйци (онлайн)',46,'https://gofederation.ru/tournaments/517298186',0,'2021-12-07 19:19:15'),(4214,'2021-12-18','2021-12-19','Чемпионат Свердловской области (женщины)',14,'https://gofederation.ru/tournaments/624238861',0,'2021-12-07 19:19:15'),(4215,'2021-12-18','2021-12-19','Кубок Посла Китая по вэйци (ТОП-16)',1,'https://gofederation.ru/tournaments/1028538551',0,'2021-12-07 19:19:15'),(4216,'2021-12-17','2021-12-22','Третий Зимний',41,'https://gofederation.ru/tournaments/606061281',0,'2021-12-07 19:19:15'),(4217,'2021-12-15','2021-12-16','Второй Зимний',41,'https://gofederation.ru/tournaments/494896614',0,'2021-12-07 19:19:15'),(4218,'2021-12-12','2021-12-12','Первенство Санкт-Петербурга до 9, до 12 и до 16 лет',2,'https://gofederation.ru/tournaments/646683407',1,'2021-12-07 19:19:15'),(4219,'2021-12-11','2021-12-11','Чемпионат Московской области',4,'https://gofederation.ru/tournaments/52134110',0,'2021-12-07 19:19:15'),(4220,'2021-12-11','2021-12-12','VII Уральский кубок Полиметалла',14,'https://gofederation.ru/tournaments/794077735',0,'2021-12-07 19:19:15'),(4221,'2021-12-10','2021-12-29','39 Ru. Декабрь',17,'https://gofederation.ru/tournaments/472509254',0,'2021-12-07 19:19:15'),(4222,'2021-12-08','2021-12-08','Первый Зимний',41,'https://gofederation.ru/tournaments/25045615',0,'2021-12-07 19:19:15');
/*!40000 ALTER TABLE `tournament_go` ENABLE KEYS */;

--
-- Table structure for table `user_BotGo`
--

DROP TABLE IF EXISTS `user_BotGo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_BotGo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_User` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT 'Человек',
  `last_name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `state_user` varchar(255) DEFAULT NULL,
  `is_child` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_User` (`id_User`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_BotGo`
--

/*!40000 ALTER TABLE `user_BotGo` DISABLE KEYS */;
INSERT INTO `user_BotGo` VALUES (2,'925936432','Виктория','Королькова','FoilV','main',0);
/*!40000 ALTER TABLE `user_BotGo` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-07 19:25:19
