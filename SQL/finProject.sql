/*CREATE SCHEMA `finproject` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;

CREATE TABLE `finproject`.`stock_aapl` (
  `date` DATETIME NULL,
  `open` DECIMAL(10,4) NULL,
  `high` DECIMAL(10,4) NULL,
  `low` DECIMAL(10,4) NULL,
  `close` DECIMAL(10,4) NULL,
  `adj_close` DECIMAL(10,4) NULL,
  `volume` INT NULL);

CREATE TABLE `finproject`.`stock_x` (
  `date` DATETIME NULL,
  `open` DECIMAL(10,4) NULL,
  `close` DECIMAL(10,4) NULL);

*/

--select * from stock_aapl

--ALTER TABLE finproject.stock_aapl
--MODIFY adj_close DECIMAL(10,4);
--commit;