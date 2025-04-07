-- Create the database
CREATE DATABASE IF NOT EXISTS security_demo;
USE security_demo;

-- Create the tables
CREATE TABLE IF NOT EXISTS user_data (
    userid VARCHAR(10) PRIMARY KEY,
    firstname VARCHAR(20),
    lastname VARCHAR(20),
    ssn VARCHAR(9),
    history VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS user_auth (
    userid VARCHAR(10) PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    pass VARCHAR(40),
    sessionid VARCHAR(12),
    FOREIGN KEY (userid) REFERENCES user_data(userid)
);

-- Insert sample data
INSERT INTO user_data (userid, firstname, lastname, ssn, history) VALUES
('user001', 'John', 'Doe', '123456789', 'This user has a long history with our company. Joined in 2010.'),
('user002', 'Jane', 'Smith', '987654321', 'VIP customer since 2015. Has premium subscription.'),
('user003', 'Admin', 'User', '111223333', 'System administrator account created at installation.'),
('user004', 'Bob', 'Johnson', '444556666', 'Customer support representative. Access level: medium.');

INSERT INTO user_auth (userid, username, pass, sessionid) VALUES
('user001', 'johnd', 'password123', ''),
('user002', 'janes', 'smith2022', ''),
('user003', 'admin', 'admin123', ''),
('user004', 'bobj', 'support2023', ''); 