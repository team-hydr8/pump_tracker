-- === Table Creation ===

CREATE TABLE Staff (
    StaffNo INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Region TEXT,
    Role TEXT,
    AccessLevel INTEGER CHECK (AccessLevel >= 0)
);

CREATE TABLE WaterPump (
    PumpID INTEGER PRIMARY KEY AUTOINCREMENT,
    StaffNo INTEGER,
    WaterUsage REAL CHECK (WaterUsage >= 0),
    Integrity REAL CHECK (Integrity BETWEEN 0 AND 100),
    Region TEXT,
    Active INTEGER DEFAULT 1,
    FOREIGN KEY (StaffNo) REFERENCES Staff(StaffNo)
);

CREATE TABLE WaterTank (
    TankID INTEGER PRIMARY KEY AUTOINCREMENT,
    StaffNo INTEGER,
    WaterLevel REAL CHECK (WaterLevel >= 0),
    Integrity REAL CHECK (Integrity BETWEEN 0 AND 100),
    Region TEXT,
    Active INTEGER DEFAULT 1,
    FOREIGN KEY (StaffNo) REFERENCES Staff(StaffNo)
);

CREATE TABLE Task (
    TaskNo INTEGER PRIMARY KEY AUTOINCREMENT,
    StaffNo INTEGER,
    PumpID INTEGER,
    TankID INTEGER,
    Description TEXT,
    Priority TEXT CHECK (Priority IN ('Low', 'Medium', 'High')),
    Completed INTEGER DEFAULT 0,
    FOREIGN KEY (StaffNo) REFERENCES Staff(StaffNo),
    FOREIGN KEY (PumpID) REFERENCES WaterPump(PumpID),
    FOREIGN KEY (TankID) REFERENCES WaterTank(TankID)
);

CREATE TABLE Customer (
    CustNo INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Region TEXT,
    Balance REAL DEFAULT 0 CHECK (Balance >= 0),
    WaterUsage REAL DEFAULT 0
);

CREATE TABLE Report (
    ReportID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustNo INTEGER,
    DateAndTime TEXT DEFAULT CURRENT_TIMESTAMP,
    Description TEXT,
    FOREIGN KEY (CustNo) REFERENCES Customer(CustNo)
);

-- === Views ===

CREATE VIEW ActiveInfrastructureByRegion AS
SELECT Region,
       SUM(ActivePumps) AS ActivePumps,
       SUM(ActiveTanks) AS ActiveTanks
FROM (
    SELECT Region,
           COUNT(PumpID) AS ActivePumps,
           0 AS ActiveTanks
    FROM WaterPump
    WHERE Active = 1
    GROUP BY Region
    UNION ALL
    SELECT Region,
           0 AS ActivePumps,
           COUNT(TankID) AS ActiveTanks
    FROM WaterTank
    WHERE Active = 1
    GROUP BY Region
)
GROUP BY Region;

CREATE VIEW StaffTaskSummary AS
SELECT
    s.StaffNo,
    s.Name,
    COUNT(t.TaskNo) AS TotalTasks,
    SUM(CASE WHEN t.Completed = 0 THEN 1 ELSE 0 END) AS PendingTasks
FROM Staff s
LEFT JOIN Task t ON s.StaffNo = t.StaffNo
GROUP BY s.StaffNo, s.Name;

CREATE VIEW CustomerReportSummary AS
SELECT
    c.CustNo,
    c.Name,
    COUNT(r.ReportID) AS ReportCount,
    MAX(r.DateAndTime) AS LastReported
FROM Customer c
LEFT JOIN Report r ON c.CustNo = r.CustNo
GROUP BY c.CustNo, c.Name;

CREATE VIEW RegionUsageSummary AS
SELECT
    Region,
    (SELECT SUM(WaterUsage) FROM WaterPump WHERE Region = r.Region) AS TotalPumpUsage,
    (SELECT SUM(WaterLevel) FROM WaterTank WHERE Region = r.Region) AS TotalTankLevel
FROM (
    SELECT Region FROM WaterPump
    UNION
    SELECT Region FROM WaterTank
) AS r;

-- === Triggers ===

CREATE TRIGGER check_task_staff_access
BEFORE INSERT ON Task
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (NEW.PumpID IS NOT NULL OR NEW.TankID IS NOT NULL)
             AND (SELECT AccessLevel FROM Staff WHERE StaffNo = NEW.StaffNo) < 2
        THEN RAISE (ABORT, 'Staff has insufficient access level to be assigned to Pump or Tank')
    END;
END;