-- Create database
CREATE DATABASE flight_database;
USE flight_database;

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone VARCHAR(15)
);

-- Flights Table
CREATE TABLE Flights (
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    flight_name VARCHAR(50),
    origin VARCHAR(50),
    destination VARCHAR(50),
    price DECIMAL(10,2) DEFAULT 5000,
    seats_available INT CHECK (seats_available >= 0),
    seats INT
);

-- Bookings Table
CREATE TABLE Bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    flight_id INT NOT NULL,
    booking_date DATE,
    tickets INT,
    passenger_fullname VARCHAR(50) NOT NULL,
    seat_no INT UNIQUE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);

-- Airlines Table
CREATE TABLE Airlines (
    airline_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_name VARCHAR(50),
    country VARCHAR(50)
);

-- Reviews Table
CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    flight_id INT,
    rating INT,
    comment VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);

-- Insert Users
INSERT INTO Users (name, email, phone) VALUES
('Alice', 'alice@gmail.com', '9000000001'),
('Bob', 'bob@gmail.com', '9000000002'),
('Charlie', 'charlie@gmail.com', '9000000003'),
('David', 'david@gmail.com', '9000000004'),
('Eva', 'eva@gmail.com', '9000000005');

-- Insert Flights
INSERT INTO Flights (flight_name, origin, destination, price, seats, seats_available) VALUES
('Airbus A320', 'Hyderabad', 'Bangalore', 3500, 150, 150),
('Boeing 737', 'Mumbai', 'Delhi', 4500, 200, 200),
('Embraer 190', 'Chennai', 'Kolkata', 3000, 100, 100),
('Airbus A380', 'Delhi', 'Dubai', 12000, 300, 300),
('Boeing 777', 'Bangalore', 'Singapore', 15000, 250, 250);

-- Insert Bookings
INSERT INTO Bookings (user_id, flight_id, booking_date, tickets, passenger_fullname, seat_no) VALUES
(1, 1, '2025-10-01', 2, 'Alice', 1),
(2, 2, '2025-10-02', 1, 'Bob', 2),
(3, 3, '2025-10-03', 3, 'Charlie', 3),
(4, 4, '2025-10-04', 1, 'David', 4),
(5, 5, '2025-10-05', 2, 'Eva', 5);

-- Insert Airlines
INSERT INTO Airlines (airline_name, country) VALUES
('IndiGo', 'India'),
('Air India', 'India'),
('Emirates', 'UAE'),
('Singapore Airlines', 'Singapore'),
('British Airways', 'UK');

-- Insert Reviews
INSERT INTO Reviews (user_id, flight_id, rating, comment) VALUES
(1, 1, 5, 'Excellent service'),
(2, 2, 4, 'Good flight'),
(3, 3, 3, 'Average experience'),
(4, 4, 5, 'Very comfortable'),
(5, 5, 4, 'Nice flight');

-- Sample Queries
-- SELECT
SELECT * FROM Flights;
SELECT * FROM Users WHERE name='Alice';

-- ORDER BY
SELECT * FROM Flights ORDER BY price DESC;

-- UPDATE
UPDATE Flights SET price=4000 WHERE flight_id=1;

-- DELETE
DELETE FROM Reviews WHERE review_id=3;

-- LIMIT
SELECT * FROM Users LIMIT 3;

-- MIN & MAX
SELECT MIN(price) AS MinPrice FROM Flights;
SELECT MAX(price) AS MaxPrice FROM Flights;

-- COUNT, AVG, SUM
SELECT COUNT(*) AS TotalBookings FROM Bookings;
SELECT AVG(price) AS AvgPrice FROM Flights;
SELECT SUM(seats) AS TotalSeats FROM Flights;

-- LIKE
SELECT * FROM Flights WHERE flight_name LIKE '%Air%';

-- IN
SELECT * FROM Users WHERE user_id IN (1, 3, 5);

-- BETWEEN
SELECT * FROM Flights WHERE price BETWEEN 3000 AND 10000;

-- JOINS
SELECT b.booking_id, u.name, f.flight_name, b.tickets
FROM Bookings b
JOIN Users u ON b.user_id = u.user_id
JOIN Flights f ON b.flight_id = f.flight_id;


--Left Join
SELECT f.flight_name, r.rating, r.comment
FROM Flights f
LEFT JOIN Reviews r ON f.flight_id = r.flight_id;


--Right Join
SELECT r.review_id, f.flight_name, r.rating
FROM Flights f
RIGHT JOIN Reviews r ON f.flight_id = r.flight_id;


--Full Outer Join
SELECT f.flight_name, r.rating
FROM Flights f
LEFT JOIN Reviews r ON f.flight_id = r.flight_id
UNION
SELECT f.flight_name, r.rating
FROM Flights f
RIGHT JOIN Reviews r ON f.flight_id = r.flight_id;


-- GROUP BY & HAVING
SELECT flight_id, AVG(rating) AS AvgRating
FROM Reviews
GROUP BY flight_id
HAVING AVG(rating) >= 4;

-- TRANSACTION 
START TRANSACTION;

-- 1. Check seat availability
SELECT seats_available FROM Flights WHERE flight_id = 1;

-- 2. Update seat availability
UPDATE Flights SET seats_available = seats_available - 1 WHERE flight_id = 1;

-- 3. Insert booking
INSERT INTO Bookings (flight_id, passenger_fullname, seat_no, user_id, booking_date, tickets)
VALUES (1, 'David', 23, 4, '2025-10-10', 1);

-- Commit changes
COMMIT;
ROLLBACK;

-- ALTER TABLE 
ALTER TABLE Users ADD COLUMN age INT DEFAULT 25;
ALTER TABLE Flights RENAME COLUMN seats TO total_seats;


-- RENAME Table 
RENAME TABLE Airlines TO Airline_Info;


-- TRUNCATE Table  (remove all data)
TRUNCATE TABLE Reviews;
