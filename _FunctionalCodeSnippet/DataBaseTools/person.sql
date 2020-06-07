CREATE TABLE `platform`.`person` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `age` INT NULL,
  `weight` FLOAT NULL,
  `birthday` DATE NULL,
  `TIMER` TIME NULL,
  PRIMARY KEY (`id`)
  )ENGINE = InnoDB DEFAULT CHARACTER SET = utf8;