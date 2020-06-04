CREATE TABLE `platform`.`student` (
  `seq` INT NOT NULL,
  `num` INT NULL,
  `age` INT NULL,
  `name` VARCHAR(45) NULL,
  `friend` VARCHAR(45) NULL,
  `times` DATE NULL,
  PRIMARY KEY (`seq`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

DROP TABLE IF EXISTS `platform`.`rule_test`;

INSERT INTO student(seq, num, age, name, friend, times) VALUES (12, 52, 15, 'kk', 'por', '2020-06-07');
