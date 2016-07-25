-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema belt_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belt_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belt_db` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema new_schema1
-- -----------------------------------------------------
USE `belt_db` ;

-- -----------------------------------------------------
-- Table `belt_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `alias` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `pw_hash` VARCHAR(255) NULL,
  `dob` DATETIME NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_db`.`favquoteslists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_db`.`favquoteslists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quoteauthor` VARCHAR(255) NULL,
  `content` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `users_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_favquoteslists_users1_idx` (`users_id` ASC),
  CONSTRAINT `fk_favquoteslists_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `belt_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_db`.`quotablequotes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_db`.`quotablequotes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quoteauthor` VARCHAR(255) NULL,
  `content` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `whoadded` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_db`.`quotablequotes_has_favquoteslists`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_db`.`quotablequotes_has_favquoteslists` (
  `quotablequotes_id` INT NOT NULL,
  `favquoteslists_id` INT NOT NULL,
  PRIMARY KEY (`quotablequotes_id`, `favquoteslists_id`),
  INDEX `fk_quotablequotes_has_favquoteslists_favquoteslists1_idx` (`favquoteslists_id` ASC),
  INDEX `fk_quotablequotes_has_favquoteslists_quotablequotes1_idx` (`quotablequotes_id` ASC),
  CONSTRAINT `fk_quotablequotes_has_favquoteslists_quotablequotes1`
    FOREIGN KEY (`quotablequotes_id`)
    REFERENCES `belt_db`.`quotablequotes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_quotablequotes_has_favquoteslists_favquoteslists1`
    FOREIGN KEY (`favquoteslists_id`)
    REFERENCES `belt_db`.`favquoteslists` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_db`.`users_quotes_favs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_db`.`users_quotes_favs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `quotablequotes_id` INT NULL,
  `users_id` INT NULL,
  `favorite_status` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
