CREATE TABLE airport
(
  state   CHAR(2) NOT NULL,
  country VARCHAR(10) NOT NULL,
  name    VARCHAR(200) NOT NULL,
  IATA    CHAR(3) NOT NULL,
  PRIMARY KEY (IATA)
);

CREATE TABLE airline
(
  name        VARCHAR(200) NOT NULL,
  Country     VARCHAR(120) NOT NULL,
  AirlineCode CHAR(10) NOT NULL,
  PRIMARY KEY (AirlineCode)
);

CREATE TABLE customer
(
  firstName       VARCHAR(200) NOT NULL,
  middle_Name     VARCHAR(200) NOT NULL,
  lastName        VARCHAR(200) NOT NULL,
  email           VARCHAR(200) NOT NULL,
  password        VARCHAR(200) NOT NULL,
  IATA            CHAR(3) NOT NULL,
  PRIMARY KEY (email),
  FOREIGN KEY (IATA) REFERENCES airport(IATA)
);

CREATE TABLE address
(
  StreetNumber      INT NOT NULL,
  zipcode           NUMERIC(5) NOT NULL,
  Street            VARCHAR(300) NOT NULL,
  PRIMARY KEY(StreetNumber, zipcode, street)
 );

CREATE TABLE creditcard
(
  CreditCard        INT NOT NULL,
  CVV               NUMERIC(4) NOT NULL,
  Type              VARCHAR(7) NOT NULL,
  Expiration_Date   DATE NOT NULL,
  StreetNumber      INT NOT NULL,
  zipcode           NUMERIC(5) NOT NULL,
  Street            VARCHAR(300) NOT NULL,
  Email             VARCHAR(200) NOT NULL,
  PRIMARY KEY (CreditCard),
  FOREIGN KEY (StreetNumber,zipcode,Street) REFERENCES address(StreetNumber,zipcode,Street),
  FOREIGN KEY (Email) REFERENCES customer(email)
);

CREATE TABLE liveat
(
  Email               VARCHAR(200) NOT NULL,
  StreetNumber        INT NOT NULL,
  zipcode             NUMERIC(5) NOT NULL,
  Street              VARCHAR(300) NOT NULL,
  PRIMARY KEY (Email,StreetNumber,zipcode,Street),
  FOREIGN KEY (Email) REFERENCES customer(email),
  FOREIGN KEY (StreetNumber,zipcode,Street) REFERENCES address(StreetNumber,zipcode,Street)
);

CREATE TABLE flight
(  
  firstClassCapcity             INT NOT NULL,
  economyClassCapcity           INT NOT NULL,
  arrivalTime                   TIME NOT NULL, # timesteam without time stemp  Figure Out
  departureTime                 TIME NOT NULL, # timesteam without time stemp  Figure Out 
  Flight_Number                 INT NOT NULL,
  dateOfFilght                  DATE NOT NULL,
  AirlineCode                   VARCHAR(10) NOT NULL,
  IATA                          CHAR(3) NOT NULL,
  Arrives_FromIATA              CHAR(3) NOT NULL,
  PRIMARY KEY (Flight_Number, AirlineCode, dateOfFilght),
  FOREIGN KEY (AirlineCode)         REFERENCES airline(AirlineCode),
  FOREIGN KEY (IATA)                REFERENCES airport(IATA),
  FOREIGN KEY (Arrives_FromIATA)    REFERENCES airport(IATA)

);

CREATE TABLE price
(
  class 						VARCHAR(15) NOT NULL,
  Amount 						INT NOT NULL,
  Flight_Number 		INT NOT NULL,
  AirlineCode 			VARCHAR(10) NOT NULL,
  dateOfFilght      DATE NOT NULL,
  PRIMARY KEY (class, Flight_Number, AirlineCode,dateOfFilght),
  FOREIGN KEY (Flight_Number, AirlineCode,dateOfFilght) REFERENCES flight(Flight_Number, AirlineCode, dateOfFilght)
  CHECK (class = 'economy' or class = 'first')
);

CREATE TABLE booking
(
  BookingID 				VARCHAR(120) NOT NULL,
  Email 					  VARCHAR(200) NOT NULL,
  CreditCard 			  INT NOT NULL,
  PRIMARY KEY (BookingID),
  FOREIGN KEY (Email) 		REFERENCES customer(email),
  FOREIGN KEY (CreditCard) 	REFERENCES creditcard(CreditCard)
);

CREATE TABLE Includes
( 
  BookingID 				  VARCHAR(120) NOT NULL,
  Class 					    VARCHAR(15) NOT NULL,
  Flight_Number 			INT NOT NULL,
  AirlineCode 				CHAR(10) NOT NULL,
  dateOfFilght        DATE NOT NULL,
  
  PRIMARY KEY (BookingID, Class, Flight_Number, AirlineCode,dateOfFilght),
  FOREIGN KEY (BookingID) 						  REFERENCES booking(BookingID),
  FOREIGN KEY (Class, Flight_Number, AirlineCode,dateOfFilght) REFERENCES price(class, Flight_Number, AirlineCode,dateOfFilght)
);
