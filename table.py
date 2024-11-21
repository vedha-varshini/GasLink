import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="gas_agency"
)

cursor = connection.cursor()

# Create UserCredentials Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserCredentials (
        UserID INTEGER AUTO_INCREMENT PRIMARY KEY,
        Username TEXT,
        Password TEXT,
        Role TEXT
    )
''')

# Create Customer Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(255)
)
''')


# Create Employee Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        EmployeeID INTEGER AUTO_INCREMENT PRIMARY KEY,
        Name TEXT,
        Role TEXT,
        PhoneNumber TEXT,
        Email TEXT
    )
''')

# Create GasCylinder Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS GasCylinder (
        CylinderID INTEGER PRIMARY KEY,
        GasType TEXT,
        Status TEXT,
        ExpiryDate DATE,
        Price REAL,
        Quantity INTEGER
    )
''')

# Create Orders Table (Now that GasCylinder table exists)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER AUTO_INCREMENT PRIMARY KEY,
        CustomerID INTEGER,
        CylinderID INTEGER,
        OrderDate DATE,
        Status TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerID),
        FOREIGN KEY (CylinderID) REFERENCES GasCylinder (CylinderID)
    )
''')

# Create Payment Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Payment (
        PaymentID INTEGER AUTO_INCREMENT PRIMARY KEY,
        OrderID INTEGER,
        Amount REAL,
        PaymentDate DATE,
        FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
    )
''')

connection.commit()
connection.close()
print("Completed")