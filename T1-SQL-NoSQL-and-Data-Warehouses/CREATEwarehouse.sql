-- Existing tables will be deleted
DROP TABLE IF EXISTS Facttab;
DROP TABLE IF EXISTS DCustomer;
DROP TABLE IF EXISTS DProduct;
DROP TABLE IF EXISTS DDate;

------------------------------------
-- Create tables:
------------------------------------

CREATE TABLE DCustomer (
    CSid         INTEGER     Constraint PK_DCustomer PRIMARY KEY,
    CustId       INTEGER,
    Name         VARCHAR(30),
    Place        VARCHAR(30),
    State        VARCHAR(30),
    Country      VARCHAR(20)        );

CREATE TABLE DProduct (
    PSid         INTEGER     Constraint PK_DProduct PRIMARY KEY,
    ArtId        INTEGER,
    Name         VARCHAR(40),
    ProdgrId     INTEGER,
    Prodgroup    VARCHAR(30),
    Color        VARCHAR(10),
    Price        Numeric(10,2)       );

CREATE TABLE DDate (
    DSid         INTEGER     Constraint PK_DDate PRIMARY KEY,
    SalesDate    Date,
    Day          INTEGER,
    Week         INTEGER,
    WeekInYear   INTEGER,
    Month        INTEGER,
    MonthInYear  INTEGER,
    Monthname    VARCHAR(15),
    Quarter      INTEGER,
    QuarterInYear INTEGER,
    Year         INTEGER           );

CREATE TABLE Facttab (
    FId          INTEGER     Constraint PK_Facttab PRIMARY KEY,
    PSid         INTEGER     Constraint FK_Facttab_P REFERENCES DProduct,
    CSid         INTEGER     Constraint FK_Facttab_C REFERENCES DCustomer,
    DSid         INTEGER     Constraint FK_Facttab_D References DDate,
    Price        NUMERIC(10,2),
    Quantity     INTEGER             );

COMMIT;
