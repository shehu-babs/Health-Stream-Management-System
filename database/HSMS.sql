#------CREATE CLINIC SQL----------
CREATE TABLE `clinic` (
  `Clinic_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Clinic_Address` varchar(255) DEFAULT NULL,
  `Number_of_Patient` varchar(15) DEFAULT NULL,
  `Supervisor` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Clinic_ID`)
);

#-------CREATE STAFF SQL--------------- 
CREATE TABLE `STAFF` (
  `Staff_ID` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Role` varchar(10) DEFAULT NULL,
  `Staff_Address` varchar(255) NOT NULL,
  `DateOfBirth` date NOT NULL,
  `Age` int(11) NOT NULL,
  `PhoneNumber` varchar(15) NOT NULL,
  `Gender` enum('Male','Female') NOT NULL,
  `ClinicID` int(11) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `User_Name` varchar(100) DEFAULT NULL,
  `Created_At` timestamp NOT NULL DEFAULT current_timestamp(),
  `Updated_At` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `USERID` varchar(10) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`Staff_ID`),
  KEY `ClinicID` (`ClinicID`),
  CONSTRAINT `STAFF_ibfk_1` FOREIGN KEY (`ClinicID`) REFERENCES `clinic` (`Clinic_ID`) ON DELETE CASCADE
);

#-----CREATE LOG SQL---------
CREATE TABLE `UserLoginLog` (
  `LogID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) NOT NULL,
  `User_Name` varchar(100) NOT NULL,
  `LastLogin` datetime DEFAULT current_timestamp(),
  `Role` varchar(100) NOT NULL,
  PRIMARY KEY (`LogID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `UserLoginLog_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `STAFF` (`Staff_ID`)
);



#-----CREATE PATIENT SQL-------------
CREATE TABLE `Patient` (
  `Patient_ID` int(11) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `DateOfBirth` date NOT NULL,
  `Age` int(11) NOT NULL,
  `PhoneNumber` varchar(15) NOT NULL,
  `Gender` enum('Male','Female') NOT NULL,
  `ClinicID` int(11) NOT NULL,
  `Emergency_Contact_Name` varchar(100) DEFAULT NULL,
  `Emergency_Contact` varchar(15) DEFAULT NULL,
  `USERID` varchar(15) DEFAULT NULL,
  `Created_At` timestamp NOT NULL DEFAULT current_timestamp(),
  `Updated_At` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`Patient_ID`),
  UNIQUE KEY `USERID` (`USERID`),
  KEY `ClinicID` (`ClinicID`),
  CONSTRAINT `Patient_ibfk_1` FOREIGN KEY (`ClinicID`) REFERENCES `clinic` (`Clinic_ID`) ON DELETE CASCADE
);

#------CREATE SERVICES SQL-------
CREATE TABLE `Services` (
  `ServiceID` int(11) NOT NULL AUTO_INCREMENT,
  `Service_Name` varchar(100) NOT NULL,
  `Service_Code` varchar(100) DEFAULT NULL,
  `Cost` decimal(10,2) NOT NULL,
  `Description` text DEFAULT NULL,
  `CreatedDate` timestamp NOT NULL DEFAULT current_timestamp(),
  `CreatedBy` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ServiceID`),
  UNIQUE KEY `Service_Code` (`Service_Code`)
);

#-------CREATE PATIENTVISIT SQL-------
CREATE TABLE `PatientVisit` (
  `VisitID` int(11) NOT NULL AUTO_INCREMENT,
  `Patient_ID` varchar(15) NOT NULL,
  `VisitDate` date DEFAULT curdate(),
  `Clinic_ID` int(11) DEFAULT NULL,
  `Diagnosis` varchar(255) DEFAULT NULL,
  `Services` varchar(255) DEFAULT NULL,
  `Symptoms` varchar(255) DEFAULT NULL,
  `CheckInBy` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`VisitID`),
  KEY `Patient_ID` (`Patient_ID`),
  KEY `Clinic_ID` (`Clinic_ID`),
  CONSTRAINT `PatientVisit_ibfk_1` FOREIGN KEY (`Patient_ID`) REFERENCES `Patient` (`USERID`),
  CONSTRAINT `PatientVisit_ibfk_2` FOREIGN KEY (`Clinic_ID`) REFERENCES `clinic` (`Clinic_ID`)
);


#-------CREATE BILLS SQL---------
CREATE TABLE `Bills` (
  `BillID` int(11) NOT NULL AUTO_INCREMENT,
  `VisitID` int(11) NOT NULL,
  `TotalCost` decimal(10,2) NOT NULL,
  `BillDate` date DEFAULT curdate(),
  `Netpay` decimal(10,2) DEFAULT 0.00,
  `Tax` decimal(10,2) DEFAULT 0.00,
  `Subtotal` decimal(10,2) DEFAULT 0.00,
  `PaymentType` varchar(255) DEFAULT 'NotPaid',
  PRIMARY KEY (`BillID`),
  KEY `VisitID` (`VisitID`),
  CONSTRAINT `Bills_ibfk_1` FOREIGN KEY (`VisitID`) REFERENCES `PatientVisit` (`VisitID`)
);

#------------CREATE MESSAGE-------
CREATE TABLE `Message` (
  `Message_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Sender` varchar(50) NOT NULL,
  `Receiver` varchar(50) NOT NULL,
  `Message_Content` text NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `Is_Read` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`Message_ID`)
);




