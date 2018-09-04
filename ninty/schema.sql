PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE genres (
 id integer PRIMARY KEY,
 name text NOT NULL
);
INSERT INTO genres VALUES(1,'Action');
INSERT INTO genres VALUES(2,'Adventure');
INSERT INTO genres VALUES(3,'Arcade');
INSERT INTO genres VALUES(4,'Fighting');
INSERT INTO genres VALUES(5,'Music');
INSERT INTO genres VALUES(6,'Party');
INSERT INTO genres VALUES(7,'Platformer');
INSERT INTO genres VALUES(8,'Puzzle');
INSERT INTO genres VALUES(9,'RPG');
INSERT INTO genres VALUES(10,'Racing');
INSERT INTO genres VALUES(11,'Shooter');
INSERT INTO genres VALUES(12,'Simulation');
INSERT INTO genres VALUES(13,'Sports');
INSERT INTO genres VALUES(14,'Strategy');
CREATE TABLE games (
 id integer PRIMARY KEY,
 name text NOT NULL,
 genre_id integer NOT NULL,
 link text,
 up integer,
 down integer,
 FOREIGN KEY(genre_id) references genres(id)
);
INSERT INTO games VALUES(1,'ACA NEO GEO THE LAST BLADE',4,NULL,1,0);
INSERT INTO games VALUES(2,'Axiom Verge',7,NULL,2,1);
INSERT INTO games VALUES(3,'Azure Striker GUNVOLT: STRIKER PACK',1,NULL,1,0);
INSERT INTO games VALUES(4,'Bad North',14,NULL,0,1);
INSERT INTO games VALUES(5,'Battle Chef Brigade',8,NULL,1,0);
INSERT INTO games VALUES(6,'Bloodstained: Curse of the Moon',1,NULL,0,0);
INSERT INTO games VALUES(7,'Bomb Chicken',1,NULL,0,0);
INSERT INTO games VALUES(8,'Celeste',7,NULL,6,0);
INSERT INTO games VALUES(9,'Darkest Dungeon',9,NULL,2,0);
INSERT INTO games VALUES(10,'Dead Cells',7,NULL,8,0);
INSERT INTO games VALUES(11,'Death Road to Canada',1,NULL,1,0);
INSERT INTO games VALUES(12,'Death Squared',8,NULL,3,0);
INSERT INTO games VALUES(13,'Enter the Gungeon',1,NULL,3,0);
INSERT INTO games VALUES(14,'Fast RMX',10,NULL,2,1);
INSERT INTO games VALUES(15,'Flinthook',1,NULL,0,0);
INSERT INTO games VALUES(16,'Floor Kids',5,NULL,0,0);
INSERT INTO games VALUES(17,'Forma.8',2,NULL,1,1);
INSERT INTO games VALUES(18,'Fortnite',11,NULL,1,1);
INSERT INTO games VALUES(19,'Garage',11,NULL,1,0);
INSERT INTO games VALUES(20,'Golf Story',2,NULL,3,4);
INSERT INTO games VALUES(21,'Gorogoa',8,NULL,3,0);
INSERT INTO games VALUES(22,'Graceful Explosion Machine',3,NULL,2,0);
INSERT INTO games VALUES(23,'Has Been Heroes',14,NULL,3,0);
INSERT INTO games VALUES(24,'Hollow Knight',7,NULL,13,0);
INSERT INTO games VALUES(25,'Hyper Sentinel',3,NULL,1,0);
INSERT INTO games VALUES(26,'I Am Setsuna',9,NULL,1,2);
INSERT INTO games VALUES(27,'Iconoclasts',1,NULL,1,0);
INSERT INTO games VALUES(28,'INSIDE',2,NULL,1,0);
INSERT INTO games VALUES(29,'Into the Breach',14,NULL,4,0);
INSERT INTO games VALUES(30,'Inversus',3,NULL,1,0);
INSERT INTO games VALUES(31,'Jack Box Party (1 - 4)',6,NULL,1,0);
INSERT INTO games VALUES(32,'KAMIKO',1,NULL,1,0);
INSERT INTO games VALUES(33,'Keep Talking and Nobody Explodes',8,NULL,0,0);
INSERT INTO games VALUES(34,'Kingdom New Lands',14,NULL,1,0);
INSERT INTO games VALUES(35,'LIMBO',2,NULL,0,0);
INSERT INTO games VALUES(36,'Lumines Remastered',8,NULL,5,0);
INSERT INTO games VALUES(37,'Minecraft',2,NULL,0,0);
INSERT INTO games VALUES(38,'Minit',2,NULL,0,0);
INSERT INTO games VALUES(39,'Mr. Shifty',1,NULL,1,0);
INSERT INTO games VALUES(40,'Mummy Demastered',7,NULL,1,2);
INSERT INTO games VALUES(41,'N++',7,NULL,2,0);
INSERT INTO games VALUES(42,'Night in the Woods',2,NULL,2,0);
INSERT INTO games VALUES(43,'Oceanhorn',2,NULL,1,0);
INSERT INTO games VALUES(44,'Overcooked! 2',6,NULL,1,0);
INSERT INTO games VALUES(45,'Overcooked! Special Edition',6,NULL,1,0);
INSERT INTO games VALUES(46,'Owlboy',7,NULL,0,3);
INSERT INTO games VALUES(47,'Oxenfree',2,NULL,1,0);
INSERT INTO games VALUES(48,'Paladins',11,NULL,2,0);
INSERT INTO games VALUES(49,'Picross S',8,NULL,2,0);
INSERT INTO games VALUES(50,'Picross S2',8,NULL,0,0);
INSERT INTO games VALUES(51,'Piczle Lines DX',8,NULL,1,0);
INSERT INTO games VALUES(52,'Pinball FX 3',3,NULL,1,0);
INSERT INTO games VALUES(53,'Pokemon Quest',9,NULL,0,0);
INSERT INTO games VALUES(54,'Portal Bridge Builder',8,NULL,2,0);
INSERT INTO games VALUES(55,'Puyo Puyo Tetris',8,NULL,4,0);
INSERT INTO games VALUES(56,'Riptide Renegade',10,NULL,1,0);
INSERT INTO games VALUES(57,'Rive',1,NULL,2,0);
INSERT INTO games VALUES(58,'Rocket League',13,NULL,2,0);
INSERT INTO games VALUES(59,'Rogue Aces',3,NULL,0,0);
INSERT INTO games VALUES(60,'Salt and Sanctuary',1,NULL,1,0);
INSERT INTO games VALUES(61,'Shovel Knight: Treasure Trove',7,NULL,4,0);
INSERT INTO games VALUES(62,'Snake Pass',7,NULL,4,3);
INSERT INTO games VALUES(63,'Snipperclips: Cut it out Together!',8,NULL,6,0);
INSERT INTO games VALUES(64,'Sonic Mania',7,NULL,5,0);
INSERT INTO games VALUES(65,'Stardew Valley',12,NULL,5,0);
INSERT INTO games VALUES(66,'Steamworld Dig 2',7,NULL,6,0);
INSERT INTO games VALUES(67,'Steamworld Heist: Ultimate Edition',14,NULL,1,0);
INSERT INTO games VALUES(68,'Strikers 1945',13,NULL,1,0);
INSERT INTO games VALUES(69,'The Binding of Isaac: Afterbirth+',1,NULL,3,0);
INSERT INTO games VALUES(70,'The Flame in the Flood: Complete Edition',2,NULL,0,0);
INSERT INTO games VALUES(71,'The Messenger',7,NULL,1,0);
INSERT INTO games VALUES(72,'The Next Penelope',10,NULL,1,0);
INSERT INTO games VALUES(73,'Thimbleweed Park',8,NULL,2,0);
INSERT INTO games VALUES(74,'Thumper',5,NULL,0,0);
INSERT INTO games VALUES(75,'Tumbleseed',1,NULL,0,0);
INSERT INTO games VALUES(76,'Uurnog Uurnlimited',8,NULL,1,0);
INSERT INTO games VALUES(77,'Vostok Inc.',3,NULL,3,0);
INSERT INTO games VALUES(78,'West of Loathing',2,NULL,0,0);
INSERT INTO games VALUES(79,'Wonderboy: The Dragon''s Trap',7,NULL,2,1);
INSERT INTO games VALUES(80,'Yoku''s Island Express',7,NULL,10,0);
COMMIT;
