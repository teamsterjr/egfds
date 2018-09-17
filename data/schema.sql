DROP database `EGFDS`;
CREATE DATABASE `EGFDS`;
use EGFDS;
CREATE TABLE `genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `platform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT '0',
  `password` text,
  `deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB;

CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `genre_id` int(11) NOT NULL,
  `link` text,
  PRIMARY KEY (`id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `game_ibfk_1` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`)
) ENGINE=InnoDB;

CREATE TABLE `game_instance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) NOT NULL,
  `platform_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `game_id` (`game_id`,`platform_id`),
  KEY `platform_id` (`platform_id`),
  CONSTRAINT `game_instance_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`),
  CONSTRAINT `game_instance_ibfk_2` FOREIGN KEY (`platform_id`) REFERENCES `platform` (`id`)
) ENGINE=InnoDB;


CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `instance_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` text,
  `promoted` tinyint(1) NOT NULL DEFAULT '0',
  `up` int(11) DEFAULT NULL,
  `down` int(11) DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `game_per_user` (`user_id`,`instance_id`),
  KEY `instance_id` (`instance_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`instance_id`) REFERENCES `game_instance` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB;
