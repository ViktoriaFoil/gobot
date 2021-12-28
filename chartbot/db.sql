

DROP TABLE IF EXISTS `Cities`;
CREATE TABLE `Cities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb3;
INSERT INTO `Cities` VALUES (1,'Москва'),(2,'Санкт-Петербург'),(3,'Моск.обл.'),(4,'Жуковский'),(5,'Калуга'),(6,'Калужская обл.'),(7,'Архангельск'),(8,'Астрахань'),(9,'Барнаул'),(10,'Великий Новгород'),(11,'Владивосток'),(12,'Волгоград'),(13,'Вологда'),(14,'Екатеринбург'),(15,'Ижевск'),(16,'Казань'),(17,'Калининград'),(18,'Киров'),(19,'Краснодар'),(20,'Красноярск'),(21,'Курган'),(22,'Магадан'),(23,'Нижний Новгород'),(24,'Новосибирск'),(25,'Новоуральск'),(26,'Пермь'),(27,'Петрозаводск'),(28,'Самара'),(29,'Севастополь'),(30,'Симферополь'),(31,'Суздаль'),(32,'Тверь'),(34,'Томск'),(38,'Тольятти'),(39,'Уфа'),(40,'Феодосия'),(41,'Хабаровск'),(42,'Челябинск'),(43,'Ярославль'),(44,'Тула'),(46,'КГС'),(47,'ОГС'),(48,'Badukpop'),(49,'Pandanet'),(50,'GoQuest'),(53,'Ленинградская обл.'),(57,'Омск'),(58,'Николаевск-на-Амуре'),(59,'Амурск');



DROP TABLE IF EXISTS `user_BotGo`;
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb3;




DROP TABLE IF EXISTS `UserCity`;
CREATE TABLE `UserCity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) DEFAULT NULL,
  `CityID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `UserID` (`UserID`),
  KEY `CityID` (`CityID`),
  CONSTRAINT `UserCity_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `user_BotGo` (`id`) ON DELETE CASCADE,
  CONSTRAINT `UserCity_ibfk_2` FOREIGN KEY (`CityID`) REFERENCES `Cities` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;



DROP TABLE IF EXISTS `children_categories`;
CREATE TABLE `children_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `categories` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4;
INSERT INTO `children_categories` VALUES (1,'до 9'),(2,'до 12'),(3,'до 16'),(4,'до 18'),(5,'до 20'),(6,'9-11'),(7,'12-15'),(8,'16-19'),(9,'Гран-при'),(10,'Гран при'),(11,'до 9,12,16 и 20'),(12,'до 9, 12, 16 и 20 лет'),(13,'До 9'),(14,'До 12'),(15,'До 16'),(16,'До 20'),(17,'для учащихся'),(18,'Детский'),(19,'гран-при'),(20,'гран при'),(21,'до 9 лет, 9-11 лет, 12-15 лет'),(22,'детский'),(23,'школьников'),(24,'Школьников'),(25,'Первенство'),(26,'первенство');




DROP TABLE IF EXISTS `keyboards`;
CREATE TABLE `keyboards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text_button` varchar(200) DEFAULT NULL,
  `type_keyboard` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
INSERT INTO `keyboards` VALUES (3,'мой город','main'),(4,'турниры в моем городе','main'),(5,'я ребенок, до 18 лет','age'),(6,'я взрослый','age'),(7,'далее','navigation'),(8,'стоп','navigation'),(10,'сообщение автору','main'),(11,'сменить город','main'),(12,'отписаться от детских турниров','main'),(13,'подписаться на детские турниры','main');



DROP TABLE IF EXISTS `tournament_go`;
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
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;






