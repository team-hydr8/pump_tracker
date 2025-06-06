-- === Table Creation ===

CREATE TABLE Staff (
    StaffNo SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Region VARCHAR(50),
    Role VARCHAR(50),
    AccessLevel INTEGER CHECK (AccessLevel >= 0)
);

CREATE TABLE WaterPump (
    PumpID SERIAL PRIMARY KEY,
    StaffNo INTEGER REFERENCES Staff(StaffNo),
    WaterUsage NUMERIC CHECK (WaterUsage >= 0),
    Integrity NUMERIC(5,2) CHECK (Integrity BETWEEN 0 AND 100),
    Region VARCHAR(50),
    Active BOOLEAN DEFAULT TRUE
);

CREATE TABLE WaterTank (
    TankID SERIAL PRIMARY KEY,
    StaffNo INTEGER REFERENCES Staff(StaffNo),
    WaterLevel NUMERIC CHECK (WaterLevel >= 0),
    Integrity NUMERIC(5,2) CHECK (Integrity BETWEEN 0 AND 100),
    Region VARCHAR(50),
    Active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Task (
    TaskNo SERIAL PRIMARY KEY,
    StaffNo INTEGER REFERENCES Staff(StaffNo),
    PumpID INTEGER REFERENCES WaterPump(PumpID),
    TankID INTEGER REFERENCES WaterTank(TankID),
    Description TEXT,
    Priority VARCHAR(20) CHECK (Priority IN ('Low', 'Medium', 'High')),
    Completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE Customer (
    CustNo SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Region VARCHAR(50),
    Balance NUMERIC(10, 2) DEFAULT 0 CHECK (Balance >= 0),
    WaterUsage NUMERIC DEFAULT 0
);

CREATE TABLE Report (
    ReportID SERIAL PRIMARY KEY,
    CustNo INTEGER REFERENCES Customer(CustNo),
    DateAndTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Description TEXT
);

-- === Views ===

CREATE VIEW ActiveInfrastructureByRegion AS
SELECT
    wp.Region AS Region,
    COUNT(DISTINCT wp.PumpID) AS ActivePumps,
    COUNT(DISTINCT wt.TankID) AS ActiveTanks
FROM WaterPump wp
FULL JOIN WaterTank wt ON wp.Region = wt.Region
WHERE wp.Active IS TRUE OR wt.Active IS TRUE
GROUP BY wp.Region;

CREATE VIEW StaffTaskSummary AS
SELECT
    s.StaffNo,
    s.Name,
    COUNT(t.TaskNo) AS TotalTasks,
    COUNT(*) FILTER (WHERE t.Completed = FALSE) AS PendingTasks
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

-- === Functions ===

-- Submit a customer report
CREATE OR REPLACE FUNCTION SubmitReport(
    customer_id INTEGER,
    report_text TEXT
) RETURNS VOID AS $$
BEGIN
    INSERT INTO Report (CustNo, Description)
    VALUES (customer_id, report_text);
END;
$$ LANGUAGE plpgsql;

-- Mark a task as completed
CREATE OR REPLACE FUNCTION CompleteTask(task_id INTEGER) RETURNS VOID AS $$
BEGIN
    UPDATE Task SET Completed = TRUE WHERE TaskNo = task_id;
END;
$$ LANGUAGE plpgsql;

-- Get total usage by region (tank + pump)
CREATE OR REPLACE FUNCTION RegionUsageSummary(region_name TEXT)
RETURNS TABLE (
    Region TEXT,
    TotalPumpUsage NUMERIC,
    TotalTankLevel NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        region_name,
        COALESCE(SUM(wp.WaterUsage), 0),
        COALESCE(SUM(wt.WaterLevel), 0)
    FROM WaterPump wp
    FULL JOIN WaterTank wt ON wp.Region = wt.Region
    WHERE wp.Region = region_name OR wt.Region = region_name;
END;
$$ LANGUAGE plpgsql;

-- Only allow access level 2 or higher to be assigned water pumps or tanks
CREATE OR REPLACE FUNCTION validate_task_assignment()
RETURNS TRIGGER AS $$
DECLARE
    staff_level INTEGER;
BEGIN
    -- Fetch staff access level
    SELECT AccessLevel INTO staff_level FROM Staff WHERE StaffNo = NEW.StaffNo;

    IF staff_level IS NULL THEN
        RAISE EXCEPTION 'StaffNo % does not exist.', NEW.StaffNo;
    END IF;

    -- Only enforce restriction if PumpID or TankID is specified
    IF (NEW.PumpID IS NOT NULL OR NEW.TankID IS NOT NULL) AND staff_level < 2 THEN
        RAISE EXCEPTION 'StaffNo % (access level %): insufficient access to be assigned WaterPump or WaterTank.',
            NEW.StaffNo, staff_level;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_task_staff_access
BEFORE INSERT OR UPDATE ON Task
FOR EACH ROW
WHEN (NEW.StaffNo IS NOT NULL)
EXECUTE FUNCTION validate_task_assignment();
