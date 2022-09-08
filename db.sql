USE `car_inventory`;

CREATE TABLE `users` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(400) DEFAULT NULL,
  `firstName` varchar(255) DEFAULT NULL,
  `lastName` varchar(255) DEFAULT NULL,
  `accType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`userID`)
);

CREATE TABLE `cars` (
  `transactionID` int NOT NULL AUTO_INCREMENT,
  `regplate` varchar(255) DEFAULT NULL,
  `kmDistance` decimal(8,5) DEFAULT NULL,
  `fuelAmount` decimal(8,5) DEFAULT NULL,
  `fuelCOST` decimal(8,3) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`transactionID`)
);



INSERT INTO `users`(`username`,`password`,`accType`) VALUES ("ADMIN","$5$rounds=535000$F.FmnbeDpVLB.1NP$CPfQKwG28dozpO/G4sFwo7oDTxXewp.hPG1G3d.79Z9","ADMIN");