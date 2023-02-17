DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
USE test;

CREATE TABLE make (
	makeId 	SMALLINT 		PRIMARY KEY AUTO_INCREMENT,
    name 	VARCHAR(45) 	NOT NULL
);

CREATE TABLE model (
	modelId	SMALLINT 		PRIMARY KEY AUTO_INCREMENT,
    name	VARCHAR(45)		NOT NULL
);

CREATE TABLE lmodel (
	lmodelId SMALLINT 		PRIMARY KEY AUTO_INCREMENT,
    name 	VARCHAR(45)		NOT NULL
);

CREATE TABLE states (
	stateID			SMALLINT		PRIMARY KEY,
    stateAbbr		VARCHAR(5)		NOT NULL,
    stateName		VARCHAR(45)		NOT NULL,
    stateCountry	VARCHAR(45)		NOT NULL
);

CREATE TABLE location (
	yardNumber 		SMALLINT 		PRIMARY KEY,
    yardName		VARCHAR(45)		NOT NULL,
	stateId			SMALLINT		NOT NULL,
    yardCity		VARCHAR(45)		 NULL,
    gmFullName		VARCHAR(45)		 NULL,
    yardPhoneAreaCode CHAR(3)		 NULL,
    yardPhoneNumber	CHAR(20)		 NULL,
    yardAddress1	VARCHAR(45)		 NULL,
    yardZip			VARCHAR(20)		 NULL,
    yardLatitude	DOUBLE			 NULL,
    yardLongitude	DOUBLE			 NULL,
    CONSTRAINT fk_states FOREIGN KEY (stateId)
		REFERENCES states (stateId)
        ON DELETE RESTRICT
);

CREATE TABLE lots (
	lotId 			INT 			PRIMARY KEY,
    VIN				CHAR(18)		NOT NULL,	
    yardNumber		SMALLINT		NULL,
    makeId 			SMALLINT		NULL,
    modelId			SMALLINT 		NULL,
    lmodelId		SMALLINT		NULL,
    CONSTRAINT fk_location FOREIGN KEY (yardNumber)
		REFERENCES location (yardNumber)
        ON DELETE RESTRICT,
	CONSTRAINT fk_make	   FOREIGN KEY (makeId)
		REFERENCES make	(makeId)
        ON DELETE RESTRICT,
	CONSTRAINT fk_model FOREIGN KEY (modelId)
		REFERENCES model (modelId)
        ON DELETE RESTRICT,
	CONSTRAINT fk_lmodel FOREIGN KEY (lmodelId)
		REFERENCES lmodel (lmodelId)
        ON DELETE RESTRICT
);

SELECT * FROM states;
SELECT * FROM make;
SELECT * FROM model;
SELECT * FROM lmodel;
SELECT * FROM make;
SELECT * FROM location;
SELECT * FROM lots;