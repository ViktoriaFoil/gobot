

--
-- Table structure for table `Cities`
--

DROP TABLE IF EXISTS `Cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cities`
--

/*!40000 ALTER TABLE `Cities` DISABLE KEYS */;
INSERT INTO `Cities` VALUES (48,'Badukpop'),(50,'GoQuest'),(49,'Pandanet'),(59,'Амурск'),(7,'Архангельск'),(8,'Астрахань'),(9,'Барнаул'),(10,'Великий Новгород'),(11,'Владивосток'),(12,'Волгоград'),(13,'Вологда'),(14,'Екатеринбург'),(4,'Жуковский'),(15,'Ижевск'),(16,'Казань'),(17,'Калининград'),(5,'Калуга'),(6,'Калужская обл.'),(46,'КГС'),(18,'Киров'),(19,'Краснодар'),(20,'Красноярск'),(21,'Курган'),(53,'Ленинградская обл.'),(22,'Магадан'),(3,'Моск.обл.'),(1,'Москва'),(60,'Мытищи'),(23,'Нижний Новгород'),(58,'Николаевск-на-Амуре'),(24,'Новосибирск'),(25,'Новоуральск'),(47,'ОГС'),(57,'Омск'),(26,'Пермь'),(27,'Петрозаводск'),(28,'Самара'),(2,'Санкт-Петербург'),(29,'Севастополь'),(30,'Симферополь'),(31,'Суздаль'),(32,'Тверь'),(38,'Тольятти'),(34,'Томск'),(44,'Тула'),(39,'Уфа'),(40,'Феодосия'),(41,'Хабаровск'),(42,'Челябинск'),(43,'Ярославль');
/*!40000 ALTER TABLE `Cities` ENABLE KEYS */;


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
-- Table structure for table `keyboards`
--

DROP TABLE IF EXISTS `keyboards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keyboards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text_button` varchar(200) DEFAULT NULL,
  `type_keyboard` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyboards`
--

/*!40000 ALTER TABLE `keyboards` DISABLE KEYS */;
INSERT INTO `keyboards` VALUES (3,'мой город','main'),(4,'турниры в моем городе','main'),(5,'я ребенок, до 18 лет','age'),(6,'я взрослый','age'),(7,'далее','navigation'),(8,'стоп','navigation'),(10,'сообщение автору','main'),(11,'сменить город','main'),(12,'отписаться от детских турниров','main'),(13,'подписаться на детские турниры','main');
/*!40000 ALTER TABLE `keyboards` ENABLE KEYS */;

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
  `is_new` varchar(255) DEFAULT 'yes',
  `details` varchar(255) DEFAULT 'not_exist',
  PRIMARY KEY (`id`),
  UNIQUE KEY `link` (`link`),
  KEY `CityID` (`CityID`),
  CONSTRAINT `tournament_go_ibfk_1` FOREIGN KEY (`CityID`) REFERENCES `Cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tournament_go`
--

/*!40000 ALTER TABLE `tournament_go` DISABLE KEYS */;
/*!40000 ALTER TABLE `tournament_go` ENABLE KEYS */;

--
-- Table structure for table `user_BotGo`
--

DROP TABLE IF EXISTS `user_BotGo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_BotGo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chatID` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT 'Человек',
  `last_name` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `state_user` varchar(255) DEFAULT NULL,
  `is_child` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chatID` (`chatID`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_BotGo`
--

/*!40000 ALTER TABLE `user_BotGo` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_BotGo` ENABLE KEYS */;


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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserCity`
--

/*!40000 ALTER TABLE `UserCity` DISABLE KEYS */;
/*!40000 ALTER TABLE `UserCity` ENABLE KEYS */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-09 19:02:44
