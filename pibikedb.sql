-- creates clean database for weerstation 
DROP USER IF EXISTS 'sensem'@'localhost';
DROP USER IF EXISTS 'senser'@'localhost';
DROP DATABASE IF EXISTS pibike;
CREATE DATABASE pibike;
USE pibike;
CREATE TABLE sensor (
  id INT(11) NOT NULL AUTO_INCREMENT,
  naam VARCHAR(45),
  eenheid VARCHAR(45),
  PRIMARY KEY (id)
);
CREATE TABLE meting (
  id INT(11) NOT NULL AUTO_INCREMENT,
  sensor_id INT(11) NOT NULL,
  tijd TIMESTAMP,
  waarde FLOAT DEFAULT NULL,
  PRIMARY KEY (id),
  KEY fk_meting_sensor (sensor_id),
  CONSTRAINT fk_meting_sensor FOREIGN KEY (sensor_id) REFERENCES sensor (id)
);
CREATE USER 'sensem'@'localhost' IDENTIFIED BY 'h@';
CREATE USER 'senser'@'localhost' IDENTIFIED BY 'h@';
GRANT INSERT ON pibike.meting TO 'sensem'@'localhost';
GRANT SELECT ON pibike.sensor TO 'sensem'@'localhost';
GRANT SELECT ON pibike.* TO 'senser'@'localhost';

INSERT INTO sensor (naam, eenheid) VALUES ('Lengtegraad', 'DD');
INSERT INTO sensor (naam, eenheid) VALUES ('Breedtegraad', 'DD');
INSERT INTO sensor (naam, eenheid) VALUES ('Temperatuur', 'C');
INSERT INTO sensor (naam, eenheid) VALUES ('Image', 'Str');

