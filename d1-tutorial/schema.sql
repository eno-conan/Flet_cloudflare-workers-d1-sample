DROP TABLE IF EXISTS Customers;
CREATE TABLE IF NOT EXISTS Customers (CustomerId INTEGER PRIMARY KEY AUTOINCREMENT, CompanyName TEXT, ContactName TEXT);
INSERT INTO Customers (CompanyName, ContactName) VALUES ('Alfreds Futterkiste', 'Maria Anders'), ('Around the Horn', 'Thomas Hardy'), ('Bs Beverages', 'Victoria Ashworth'), ('Bs Beverages', 'Random Name');