CREATE DATABASE voter;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    password VARCHAR(100),
    is_staff BOOLEAN DEFAULT FALSE
);
use voter;
select * from users;
INSERT INTO users (name, email, phone_number, password, is_staff)
VALUES ('John Doe', 'john@example.com', '1234567890', 'password123', FALSE);
INSERT INTO users (name, email, phone_number, password, is_staff)
VALUES ('Sworaj Tadu', 'sworajtaduhappy@gmail.com', '9861224278', 'sworaj123', TRUE);
ALTER TABLE users
ADD COLUMN date_of_birth DATE,
ADD COLUMN age INT,
ADD COLUMN adhar VARCHAR(12);
UPDATE users
SET date_of_birth = '2002-04-01',
    age = 23,
    adhar = '987654321098'
WHERE email = 'sworajtaduhappy@gmail.com';
select * from users;
ALTER TABLE users
ADD COLUMN date_of_birth DATE,
ADD COLUMN age INT,
ADD COLUMN aadhar_number VARCHAR(12);
