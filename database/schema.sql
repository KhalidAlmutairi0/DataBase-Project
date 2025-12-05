-- MySQL Workbench Forward Engineering
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS,
FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE,
SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZE
RO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
-- -----------------------------------------------------
-- Schema phase#1
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema phase#1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `phase#1` DEFAULT CHARACTER SET utf8 ;
USE `phase#1` ;
-- -----------------------------------------------------
-- Table `phase#1`.`Airport`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Airport` (
`Airport_iD` INT NULL,
`Airport_Name` VARCHAR(45) NULL,
`City` VARCHAR(45) NULL,
`Country` VARCHAR(45) NULL,
`Code` VARCHAR(45) NULL,
`Capacity` INT NULL,
PRIMARY KEY (`Airport_iD`))
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`AirLine`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`AirLine` (
`Airline_iD` INT NULL,
`Airline_Name` VARCHAR(45) NULL,
`Country` VARCHAR(45) NULL,
`Founded_Year` DATE NULL,
PRIMARY KEY (`Airline_iD`))
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Aircraft`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Aircraft` (
`Aircraft_iD` INT NULL,
`FK_Airline_iD` INT NOT NULL,
`Model` VARCHAR(45) NULL,
`Manufacturer` VARCHAR(45) NULL,
`Capacity` INT NULL,
PRIMARY KEY (`Aircraft_iD`),
INDEX `fk_Aircraft_AirLine1_idx` (`FK_Airline_iD` ASC) VISIBLE,
CONSTRAINT `fk_Aircraft_AirLine1`
FOREIGN KEY (`FK_Airline_iD`)
REFERENCES `phase#1`.`AirLine` (`Airline_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION)
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Flight`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Flight` (
`Flight_iD` INT NULL,
`FK_Aircraft_iD` INT NOT NULL,
`Arr_Airport_iD` INT NOT NULL,
`Dep_Airport_iD` INT NOT NULL,
`Flight_Number` INT NULL,
`Departure_time` VARCHAR(45) NULL,
`Arrival_time` VARCHAR(45) NULL,
`Status` VARCHAR(45) NULL,
PRIMARY KEY (`Flight_iD`, `FK_Aircraft_iD`),
INDEX `fk_Flight_Airport1_idx` (`Dep_Airport_iD` ASC) VISIBLE,
INDEX `fk_Flight_Airport2_idx` (`Arr_Airport_iD` ASC) VISIBLE,
INDEX `fk_Flight_Aircraft1_idx` (`FK_Aircraft_iD` ASC) VISIBLE,
CONSTRAINT `fk_Flight_Airport1`
FOREIGN KEY (`Dep_Airport_iD`)
REFERENCES `phase#1`.`Airport` (`Airport_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION,
CONSTRAINT `fk_Flight_Airport2`
FOREIGN KEY (`Arr_Airport_iD`)
REFERENCES `phase#1`.`Airport` (`Airport_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION,
CONSTRAINT `fk_Flight_Aircraft1`
FOREIGN KEY (`FK_Aircraft_iD`)
REFERENCES `phase#1`.`Aircraft` (`Aircraft_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION)
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Passenger`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Passenger` (
`Passenger_iD` INT NULL,
`First_Name` VARCHAR(45) NULL,
`Last_Name` VARCHAR(45) NULL,
`Gender` VARCHAR(1) NULL,
`Nationality` VARCHAR(45) NULL,
`Phone` VARCHAR(45) NULL,
`Email` VARCHAR(45) NULL,
PRIMARY KEY (`Passenger_iD`))
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Ticket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Ticket` (
`Ticket_iD` INT NULL,
`Flight_Flight_iD` INT NOT NULL,
`Flight_FK_Aircraft_iD` INT NOT NULL,
`FK_Passenger_iD` INT NOT NULL,
`Seat_Number` INT NULL,
`Price` INT NULL,
`Class` VARCHAR(45) NULL,
PRIMARY KEY (`Ticket_iD`),
INDEX `fk_Ticket_Flight1_idx` (`Flight_Flight_iD` ASC, `Flight_FK_Aircraft_iD` ASC)
VISIBLE,
INDEX `fk_Ticket_Passenger1_idx` (`FK_Passenger_iD` ASC) VISIBLE,
CONSTRAINT `fk_Ticket_Flight1`
FOREIGN KEY (`Flight_Flight_iD` , `Flight_FK_Aircraft_iD`)
REFERENCES `phase#1`.`Flight` (`Flight_iD` , `FK_Aircraft_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION,
CONSTRAINT `fk_Ticket_Passenger1`
FOREIGN KEY (`FK_Passenger_iD`)
REFERENCES `phase#1`.`Passenger` (`Passenger_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION)
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Employee` (
`Employee_iD` INT NULL,
`FK_Airport_iD` INT NOT NULL,
`First_Name` VARCHAR(45) NULL,
`Last_Name` VARCHAR(45) NULL,
`Jop_title` VARCHAR(45) NULL,
`Salary` INT NULL,
PRIMARY KEY (`Employee_iD`),
INDEX `fk_Employee_Airport1_idx` (`FK_Airport_iD` ASC) VISIBLE,
CONSTRAINT `fk_Employee_Airport1`
FOREIGN KEY (`FK_Airport_iD`)
REFERENCES `phase#1`.`Airport` (`Airport_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION)
ENGINE = InnoDB;
-- -----------------------------------------------------
-- Table `phase#1`.`Employee_Address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `phase#1`.`Employee_Address` (
`Address_iD` INT NOT NULL,
`FK_Employee_iD` INT NOT NULL,
`Street` VARCHAR(45) NULL,
`City` VARCHAR(45) NULL,
`Zip_Code` VARCHAR(10) NULL,
PRIMARY KEY (`Address_iD`),
INDEX `fk_Employee_Address_Employee_idx` (`FK_Employee_iD` ASC) VISIBLE,
UNIQUE INDEX `FK_Employee_iD_UNIQUE` (`FK_Employee_iD` ASC) VISIBLE,
CONSTRAINT `fk_Employee_Address_Employee`
FOREIGN KEY (`FK_Employee_iD`)
REFERENCES `phase#1`.`Employee` (`Employee_iD`)
ON DELETE NO ACTION
ON UPDATE NO ACTION)
ENGINE = InnoDB;
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;