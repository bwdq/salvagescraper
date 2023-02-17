DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
USE test;

CREATE TABLE make (
	makeId 	SMALLINT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
    name 	VARCHAR(45) 		NOT NULL
);


CREATE TABLE model (
	modelId	SMALLINT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
    name	VARCHAR(45)			NOT NULL
);

CREATE TABLE lmodel (
	lmodelId SMALLINT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
    name 	VARCHAR(45)			NOT NULL
);

CREATE TABLE location (
	yardNumber 		SMALLINT UNSIGNED	PRIMARY KEY,
    yardName		VARCHAR(45)			NOT NULL,
    yardStateName	VARCHAR(45)			NOT NULL,
    yardStateCode	CHAR(3)			 	NOT NULL,
    yardCity		VARCHAR(45)		 	NOT NULL,
    gmFullName		VARCHAR(45)		 	NOT NULL,
    yardPhoneAreaCode CHAR(3)		 	NOT NULL,
    yardPhoneNumber	CHAR(20)		 	NOT NULL,
    yardAddress1	VARCHAR(45)		 	NOT NULL,
    yardZip			VARCHAR(20)		 	NOT NULL,
    yardLatitude	DOUBLE			 	NOT NULL,
    yardLongitude	DOUBLE			 	NOT NULL
);

CREATE TABLE lots (
	lotId 			INT UNSIGNED			PRIMARY KEY,
    VIN				CHAR(18)				NOT NULL,	
    yardNumber		SMALLINT UNSIGNED		NULL,
    makeId 			SMALLINT UNSIGNED		NULL,
    modelId			SMALLINT UNSIGNED		NULL,
    lmodelId		SMALLINT UNSIGNED		NULL,
    CONSTRAINT fk_location FOREIGN KEY (yardNumber)
		REFERENCES location (yardNumber)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
	CONSTRAINT fk_make	   FOREIGN KEY (makeId)
		REFERENCES make	(makeId)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
	CONSTRAINT fk_model FOREIGN KEY (modelId)
		REFERENCES model (modelId)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
	CONSTRAINT fk_lmodel FOREIGN KEY (lmodelId)
		REFERENCES lmodel (lmodelId)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

CREATE TABLE bid (
	bidId INT UNSIGNED			PRIMARY KEY AUTO_INCREMENT,
    lotId INT UNSIGNED			NOT NULL,
    bidAmount MEDIUMINT			NOT NULL,
    scrapetime DATETIME			NOT NULL,
    CONSTRAINT fk_lots FOREIGN KEY (lotId)
		REFERENCES lots (lotId)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

/*
INSERT DATA
Add the Insert_$name.sql files in this order:
1. make
2. model
3. lmodel
4. location
5. lots
6. bid
*/

/*
QUERIES
*/
#1. bad VIN
SELECT * 
FROM lots
WHERE LENGTH(VIN) > 17;
#2. lots with full lot details (~30k)
SELECT lotId, VIN, make.name AS MakeName, model.name AS ModelName, lmodel.name AS lModelName, yardNumber, yardName
FROM lots
	JOIN make USING (makeId)
    JOIN model USING (modelId)
    JOIN lmodel USING (lmodelId)
    JOIN location USING (yardNumber)
WHERE yardNumber IS NOT NULL;
#3. stats
SELECT AVG(bidAmount) AS 'Average Bid', MAX(bidAmount) AS 'Max Bid' FROM bid;
#4. highest bid lot
SELECT lotId, VIN, make.name AS MakeName, model.name AS ModelName, lmodel.name AS lModelName, yardName 
FROM lots 
	JOIN make USING (makeId)
    JOIN model USING (modelId)
    JOIN lmodel USING (lmodelId)
    JOIN location USING (yardNumber)
WHERE lotId = (
	SELECT lotId 
    FROM bid 
    WHERE bidAmount = (
		SELECT MAX(bidAmount) 
		FROM bid
	)
);
#5. Get list yards and contact info for locations where they have leaf cars
SELECT DISTINCT(yardName), yardCity AS City, location.yardStateName AS State, location.gmFullName AS ManagerName, location.yardPhoneNumber
FROM lots
    JOIN make USING (makeId)
    JOIN model USING (modelId)
    JOIN lmodel USING (lmodelId)
    JOIN location USING (yardNumber)
WHERE model.name LIKE '%leaf%' OR lmodel.name LIKE '%leaf%'
ORDER BY location.yardStateName;

/*
VIEWS
*/
#1. all cars in Cali
CREATE OR REPLACE VIEW CaliCars AS
SELECT lotId, VIN, make.name AS MakeName, model.name AS ModelName, lmodel.name AS lModelName, yardName
FROM lots
	JOIN make USING (makeId)
    JOIN model USING (modelId)
    JOIN lmodel USING (lmodelId)
    JOIN location USING (yardNumber)
WHERE yardStateCode = 'CA'
ORDER BY yardName ASC;

SELECT * FROM CaliCars;

#2. find my leaf battery nearby
CREATE OR REPLACE VIEW WaLeaf AS
SELECT lotId, VIN, make.name AS MakeName, model.name AS ModelName, lmodel.name AS lModelName, yardName, bidAmount, scrapetime AS BidTime
FROM lots
	JOIN make USING (makeId)
    JOIN model USING (modelId)
    JOIN lmodel USING (lmodelId)
    JOIN location USING (yardNumber)
    JOIN bid USING (lotId)
WHERE yardStateCode = 'WA' AND model.name LIKE '%leaf%'
ORDER BY bidAmount ASC;

SELECT * FROM WaLeaf;
