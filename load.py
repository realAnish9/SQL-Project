import sqlite3

#creating a connection
conn=sqlite3.connect('project.db') 
cursor=conn.cursor()

#creating CUSTOMER table 
cursor.execute("""CREATE TABLE IF NOT EXISTS CUSTOMER (
  CustID VARCHAR(10) NULL,
  Name VARCHAR(45) NOT NULL,
  Phone VARCHAR(45) NULL,
  UNIQUE(CustID))""")

#creating RATE table
cursor.execute("""CREATE TABLE IF NOT EXISTS RATE(
	Type VARCHAR(5) NOT NULL,
    Category VARCHAR(10) NOT NULL,
    Weekly DECIMAL(10,2) NOT NULL,
    Daily DECIMAL(10,2) NOT NULL,
	UNIQUE (Type,Category))""")

#creating VEHICLE table
cursor.execute("""CREATE TABLE IF NOT EXISTS VEHICLE(
	VehicleID VARCHAR(45) NOT NULL,
    Description VARCHAR(100) NOT NULL,
    Year VARCHAR(4) NOT NULL,
    Type VARCHAR(5) NOT NULL,
    Category VARCHAR(10) NOT NULL,
    PRIMARY KEY (VehicleID),
		FOREIGN KEY (Type,Category)
			REFERENCES RATE(Type,Category))""")

#creating RENTAL table
cursor.execute("""CREATE TABLE IF NOT EXISTS RENTAL(
	CustID VARCHAR(5) NULL,
	VehicleID VARCHAR(45) NOT NULL,
    StartDate DATE NOT NULL,
    OrderDate DATE NOT NULL,
    RentalType VARCHAR(1) NOT NULL,
    Qty INT NOT NULL, 
    ReturnDate DATE NOT NULL,
    TotalAmount INT NOT NULL, 
    PaymentDate DATE NULL,
		FOREIGN KEY (VehicleID)
			REFERENCES Vehicle(VehicleID),
		FOREIGN KEY (CustID)
			REFERENCES CUSTOMER(CustID))""")

#adding Returned row to RENTAL table
#cursor.execute("ALTER TABLE RENTAL ADD COLUMN Returned INT")


#updating values in Returned column
#change Returned to 0 if no PayementDate
cursor.execute('UPDATE RENTAL SET Returned=0 WHERE PaymentDate="NULL"')
#change Returned to 1 if there is PayementDate
cursor.execute('UPDATE RENTAL SET Returned=1 WHERE PaymentDate!="NULL"')

''' OUTPUT
cursor.execute("SELECT *FROM RENTAL")
custData=cursor.fetchall()
for row in custData:
	print(row)
'''

cursor.execute("DROP VIEW vRentalInfo")
cursor.execute('''CREATE VIEW vRentalInfo AS
SELECT RENTAL.OrderDate, RENTAL.StartDate, RENTAl.ReturnDate,
  RENTAL.qty*RENTAL.RentalType AS TotalDays,
  RENTAL.VehicleID AS VIN,
  VEHICLE.DESCRIPTION AS VEHICLE,
  CASE VEHICLE.Type
	WHEN 1 THEN 'Compact'
    WHEN 2 THEN 'Medium'
    WHEN 3 THEN 'Large'
    WHEN 4 THEN 'SUV'
    WHEN 5 THEN 'Truck'
    WHEN 6 THEN 'VAN'
END AS Type,
CASE VEHICLE.Category
	WHEN 1 THEN 'LUXURY'
    WHEN 0 THEN 'BASIC'
END AS Category,
CUSTOMER.CustID AS CustomerID,
CUSTOMER.Name AS CustomerName,
RENTAL.TotalAmount AS OrderAmount,
CASE 
	WHEN RENTAL.PaymentDate!="NULL" THEN 0
    ELSE Rental.TotalAmount
END AS RentalBalance
FROM VEHICLE, RENTAL,CUSTOMER
WHERE VEHICLE.VehicleID=RENTAL.VehicleID AND CUSTOMER.CustID=RENTAL.CustID
ORDER BY RENTAL.StartDate;
''')

cursor.execute("SELECT *FROM vRentalInfo")

data=cursor.fetchall()
for line in data:
  print(line)

conn.commit()
conn.close()
