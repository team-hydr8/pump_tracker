INSERT INTO Staff (Name, Region, Role, AccessLevel) VALUES
('Pieter Botha', 'Troyeville', 'Engineer', 2),
('Neo Mokgosi', 'Bertrams', 'Engineer', 2),
('Sipho Maseko', 'Johannesburg CBD', 'Developer', 1),
('Nandi Molefe', 'Johannesburg CBD', 'Manager', 3);

INSERT INTO WaterPump (StaffNo, WaterUsage, Integrity, Region, Active) VALUES
(1, 1200.5, 92.5, 'Lorentzville', 1),
(2, 980.0, 76.0, 'Bertrams', 1),
(1, 0, 0.0, 'New Doornfontein', 0);

INSERT INTO WaterTank (StaffNo, WaterLevel, Integrity, Region, Active) VALUES
(3, 2500.0, 99.0, 'Lorentzville', 1),
(2, 1800.0, 85.5, 'Bertrams', 1),
(3, 0.0, 10.0, 'New Doornfontein', 0);

INSERT INTO Task (StaffNo, PumpID, TankID, Description, Priority, Completed) VALUES
(1, 1, 1, 'Inspect pump integrity and report status.', 'High', 0),
(2, 2, 2, 'Routine maintenance check on tank and pump.', 'Medium', 1),
(3, NULL, NULL, 'Fix app bug #5279.', 'High', 0);

INSERT INTO Customer (Name, Region, Balance, WaterUsage) VALUES
('Ayanda Dlamini', 'New Doornfontein', 25.00, 500.0),
('Thando Khumalo', 'Bezuidenhout Valley', 10.50, 300.0),
('Lindiwe Mkhize', 'Troyeville', 0.00, 800.0);

INSERT INTO Report (CustNo, Description) VALUES
(1, 'Water pressure is too low since last week.'),
(2, 'Suspect water contamination – needs urgent attention.'),
(3, 'Billing issue: incorrect water usage shown.');

-- Simulate stored procedure calls (replaced with SQLite-compatible statements)
UPDATE Task SET Completed = 1 WHERE TaskNo = 1;

INSERT INTO Report (CustNo, Description) VALUES (1, 'Low water pressure.');

-- Region usage summary query (example)
-- You can run this directly in SQLite:
-- SELECT * FROM RegionUsageSummary('Lorentzville');
SELECT 
    'Lorentzville' AS Region,
    (SELECT SUM(WaterUsage) FROM WaterPump WHERE Region = 'Lorentzville') AS TotalPumpUsage,
    (SELECT SUM(WaterLevel) FROM WaterTank WHERE Region = 'Lorentzville') AS TotalTankLevel;
