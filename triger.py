import mysql.connector

# Create a MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="gas_agency"
)

# Create a cursor
cursor = conn.cursor()

# SQL script to create the trigger
create_trigger_sql = """
CREATE TRIGGER update_to_out_of_stock
BEFORE UPDATE ON gascylinder
FOR EACH ROW
BEGIN
    IF NEW.quantity < 20 THEN
        SET NEW.status = 'Out of Stock';
    END IF;
END;
"""

# Execute the script
cursor.execute(create_trigger_sql)

# Commit the changes
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()