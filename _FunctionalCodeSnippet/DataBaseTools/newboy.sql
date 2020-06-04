CREATE TABLE `platform`.`newboy` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `age` INT NULL,
  `name` VARCHAR(45) NULL,
  `grade` FLOAT NULL,
  `dates` DATE NULL,
  `times` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;