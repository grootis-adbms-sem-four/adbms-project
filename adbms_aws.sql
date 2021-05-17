USE mydb;

CREATE TABLE details_table(
Name_User VARCHAR(50),
email VARCHAR(50),
username VARCHAR(50) PRIMARY KEY,
age FLOAT,
gender ENUM('M','F','Other'),
address VARCHAR(200),
phno VARCHAR(50),
insert_date DATE 
);
CREATE TABLE login_table(
username VARCHAR(50) PRIMARY KEY,
pass VARCHAR(50),
FOREIGN KEY (username) REFERENCES details_table(username)
);
CREATE TABLE backup_table(
Name_User VARCHAR(50),
email VARCHAR(50),
username VARCHAR(50),
age FLOAT,
gender ENUM('M','F','Other'),
address VARCHAR(200),
phno VARCHAR(50),
insert_date DATE
);

DELIMITER $$
CREATE TRIGGER backup_trigger
AFTER INSERT ON details_table
FOR EACH ROW
BEGIN
	INSERT INTO backup_table VALUES (NEW.Name_User, NEW.email, NEW.username, NEW.age, NEW.gender, NEW.address, NEW.phno, NEW.insert_date);
END$$
DELIMITER ;

SELECT * FROM details_table;
SELECT * FROM login_table;
SELECT * FROM backup_table;
