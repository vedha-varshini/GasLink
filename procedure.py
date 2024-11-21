import mysql.connector

conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
cursor = conn.cursor()
# Define the SQL statement to create the procedure
create_procedure_sql = """
CREATE PROCEDURE BookGasCylinder(
    IN p_user_id INT,
    IN p_gas_type VARCHAR(255),
    IN p_quantity INT,
    OUT p_total_price INT
)
BEGIN
    DECLARE available_cylinder_id INT;
    DECLARE gas_available INT DEFAULT 0;

    -- Find an available gas cylinder with the specified gas type
    SELECT CylinderID
    INTO available_cylinder_id
    FROM GasCylinder
    WHERE GasType = p_gas_type AND Status = 'In stock'
    LIMIT 1;
    
    IF available_cylinder_id IS NOT NULL THEN
        -- Create a new order
        INSERT INTO Orders (CustomerID, CylinderID, OrderDate, Status)
        VALUES (p_user_id, available_cylinder_id, CURDATE(), 'Pending');


        -- Update the GasCylinder table to reflect the change in stock
        UPDATE GasCylinder
        SET Quantity = Quantity - p_quantity  -- Subtract booked quantity
        WHERE CylinderID = available_cylinder_id;

        SET gas_available = 1;
    END IF;

    IF gas_available = 1 THEN
        SELECT Price * p_quantity INTO p_total_price FROM GasCylinder WHERE CylinderID = available_cylinder_id;
    ELSE
        SET p_total_price = 100; -- Indicate gas type not available
    END IF;
END;
"""

# Execute the SQL statement to create the procedure
cursor.execute(create_procedure_sql)
print("over")
cursor.close()
conn.close()