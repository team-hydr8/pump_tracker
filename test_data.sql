INSERT INTO Staff (Name, Region, Role, AccessLevel) VALUES
('Pieter Botha', 'Troyeville', 'Engineer', 2),
('Neo Mokgosi', 'Bertrams', 'Engineer', 2),
('Sipho Maseko', 'Johannesburg CBD', 'Developer', 1),
('Nandi Molefe', 'Johannesburg CBD', 'Manager', 3);

INSERT INTO WaterPump (StaffNo, WaterUsage, Integrity, Region, Active) VALUES
(1, 1200.5, 92.5, 'Lorentzville', TRUE),
(2, 980.0, 76.0, 'Bertrams', TRUE),
(1, 0, 0.0, 'New Doornfontein', FALSE);

INSERT INTO WaterTank (StaffNo, WaterLevel, Integrity, Region, Active) VALUES
(3, 2500.0, 99.0, 'Lorentzville', TRUE),
(2, 1800.0, 85.5, 'Bertrams', TRUE),
(3, 0.0, 10.0, 'New Doornfontein', FALSE);

INSERT INTO Task (StaffNo, PumpID, TankID, Description, Priority, Completed) VALUES
(1, 1, 1, 'Inspect pump integrity and report status.', 'High', FALSE),
(2, 2, 2, 'Routine maintenance check on tank and pump.', 'Medium', TRUE),
(3, NULL, NULL, 'Fix app bug #5279.', 'High', FALSE);

INSERT INTO Customer (Name, Region, Balance, WaterUsage) VALUES
('Ayanda Dlamini', 'New Doornfontein', 25.00, 500.0),
('Thando Khumalo', 'Bezuidenhout Valley', 10.50, 300.0),
('Lindiwe Mkhize', 'Troyeville', 0.00, 800.0);

INSERT INTO Report (CustNo, Description) VALUES
(1, 'Water pressure is too low since last week.'),
(2, 'Suspect water contamination – needs urgent attention.'),
(3, 'Billing issue: incorrect water usage shown.');

SELECT CompleteTask(1);

SELECT SubmitReport(1, 'Low water pressure.');

SELECT * FROM RegionUsageSummary('Lorentzville');