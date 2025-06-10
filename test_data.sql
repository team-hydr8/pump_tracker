INSERT INTO Staff (Name, Password, Region, Role, AccessLevel) VALUES
('Pieter Botha', '$2b$12$FXnUQpDpKCd9QVDwj3XNWO70Gi.GoNdTIx0bYiyk/RUFtu9dZ35B6', 'Troyeville', 'Engineer', 2),
('Neo Mokgosi', '$2b$12$FXnUQpDpKCd9QVDwj3XNWO70Gi.GoNdTIx0bYiyk/RUFtu9dZ35B6', 'Bertrams', 'Engineer', 2),
('Sipho Maseko', '$2b$12$FXnUQpDpKCd9QVDwj3XNWO70Gi.GoNdTIx0bYiyk/RUFtu9dZ35B6', 'Johannesburg CBD', 'Developer', 1),
('Nandi Molefe', '$2b$12$FXnUQpDpKCd9QVDwj3XNWO70Gi.GoNdTIx0bYiyk/RUFtu9dZ35B6', 'Johannesburg CBD', 'Manager', 3);

INSERT INTO WaterPump (StaffNo, WaterUsage, Integrity, Region, Active) VALUES
(1, 1200.5, 92.5, 'Lorentzville', 1),
(2, 980.0, 76.0, 'Bertrams', 1),
(1, 150.0, 45.0, 'New Doornfontein', 1),
(NULL, 0, 0.0, 'Troyeville', 0);


INSERT INTO WaterTank (StaffNo, WaterLevel, Integrity, Region, Active) VALUES
(3, 2500.0, 99.0, 'Lorentzville', 1),
(2, 1800.0, 85.5, 'Bertrams', 1),
(3, 950.0, 95.0, 'New Doornfontein', 1),
(NULL, 0.0, 10.0, 'Bezuidenhout Valley', 0);

INSERT INTO Task (StaffNo, PumpID, TankID, Description, Priority, Completed) VALUES
(1, 1, 1, 'Inspect pump integrity and report status.', 'High', 0),
(2, 2, 2, 'Routine maintenance check on tank and pump.', 'Medium', 1),
(3, NULL, NULL, 'Fix app bug #5279.', 'High', 0);

INSERT INTO Customer (Name, Password, Region, Balance, WaterUsage) VALUES
('Ayanda Dlamini', '$2b$12$tLSx3XsAPtaPVuk4Wv7D8edUTqxAQF8h7EDrzRgLYgMmZmrhHzopm', 'New Doornfontein', 25.00, 500.0),
('Thando Khumalo', '$2b$12$tLSx3XsAPtaPVuk4Wv7D8edUTqxAQF8h7EDrzRgLYgMmZmrhHzopm', 'Bezuidenhout Valley', 10.50, 300.0),
('Lindiwe Mkhize', '$2b$12$tLSx3XsAPtaPVuk4Wv7D8edUTqxAQF8h7EDrzRgLYgMmZmrhHzopm', 'Troyeville', 0.00, 800.0);

INSERT INTO Report (CustNo, Description) VALUES
(1, 'Water pressure is too low since last week.'),
(2, 'Suspect water contamination, needs urgent attention.'),
(3, 'Billing issue: incorrect water usage shown.');

INSERT INTO Report (CustNo, Description) VALUES (1, 'Low water pressure.');

SELECT
    'Lorentzville' AS Region,
    (SELECT SUM(WaterUsage) FROM WaterPump WHERE Region = 'Lorentzville') AS TotalPumpUsage,
    (SELECT SUM(WaterLevel) FROM WaterTank WHERE Region = 'Lorentzville') AS TotalTankLevel;