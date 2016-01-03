SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE DATABASE IF NOT EXISTS `otohdotio` ;

DROP SCHEMA IF EXISTS `otohdotio` ;
CREATE SCHEMA IF NOT EXISTS `otohdotio` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `otohdotio` ;

-- -----------------------------------------------------
-- Table `otoh`.`certificate`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `otohdotio`.`certificate` ;

CREATE  TABLE IF NOT EXISTS `otohdotio`.`certificate` (
  `sn` INT NOT NULL ,
  `cert_uuid` TEXT NOT NULL ,
  PRIMARY KEY (`sn`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;