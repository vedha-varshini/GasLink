import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="gas_agency"
)

cursor = connection.cursor()
# Create tables (Customer, Gas Cylinder, Employee, Orders, Payment) as previously explained.


connection.commit()
connection.close()

# Create the main application window
root = tk.Tk()
root.title("Gas Agency Database")

#funnctions for the admin window
def display_users_table():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customer")
        users = cursor.fetchall()
        conn.close()
        
        # Create a new window to display the user information
        new_window = tk.Tk()
        new_window.title("User Information")

        # Create a Text widget to display the information
        text_widget = tk.Text(new_window)
        text_widget.pack()

        for user in users:
            customer_id, name, address, phone_number, email = user
            user_info = f"Customer ID: {customer_id}\nName: {name}\nAddress: {address}\nPhone Number: {phone_number}\nEmail: {email}\n\n"
            text_widget.insert(tk.END, user_info)

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    new_window.mainloop()

def display_employee_table():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        ) 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()
    conn.close()

    # Display the employees in a new window
def edit_employee_table():
    # Create a new window for editing employee information
    edit_window = tk.Toplevel()
    edit_window.title("Edit Employee")

    # Create labels and entry fields to edit employee information
    name_label = tk.Label(edit_window, text="Name:")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(edit_window)
    name_entry.grid(row=0, column=1)

    role_label = tk.Label(edit_window, text="Role:")
    role_label.grid(row=1, column=0)
    role_entry = tk.Entry(edit_window)
    role_entry.grid(row=1, column=1)

    phone_label = tk.Label(edit_window, text="Phone Number:")
    phone_label.grid(row=2, column=0)
    phone_entry = tk.Entry(edit_window)
    phone_entry.grid(row=2, column=1)

    email_label = tk.Label(edit_window, text="Email:")
    email_label.grid(row=3, column=0)
    email_entry = tk.Entry(edit_window)
    email_entry.grid(row=3, column=1)

    # Function to update employee information
    def update_employee():
        new_name = name_entry.get()
        new_role = role_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()

        if new_name and new_role and new_phone and new_email:
            # Update the Employee table with the new information
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="gas_agency"
            )
            cursor = conn.cursor()
            cursor.execute("UPDATE Employee SET Name=%s, Role=%s, PhoneNumber=%s, Email=%s WHERE EmployeeID=%s", (new_name, new_role, new_phone, new_email, selected_employee_id))
            conn.commit()
            conn.close()
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    update_button = tk.Button(edit_window, text="Update Employee", command=update_employee)
    update_button.grid(row=4, column=0, columnspan=2)

    # Close the edit window
    def close_window():
        edit_window.destroy()

    close_button = tk.Button(edit_window, text="Close", command=close_window)
    close_button.grid(row=5, column=0, columnspan=2)

    # Retrieve the selected employee's information (e.g., from a listbox or database query)
    selected_employee_id = 1  # Replace with the actual ID of the selected employee
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Role, PhoneNumber, Email FROM Employee WHERE EmployeeID=%s", (selected_employee_id,))
    employee_info = cursor.fetchone()
    conn.close()

    if employee_info:
        # Display the employee information in the entry fields
        name_entry.insert(0, employee_info[0])
        role_entry.insert(0, employee_info[1])
        phone_entry.insert(0, employee_info[2])
        email_entry.insert(0, employee_info[3])
    else:
        messagebox.showerror("Error", "Employee not found.")

def display_stock_table():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GasCylinder")
    stock = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]  # Get the column names
    conn.close()

    # Create a new window to display stock
    stock_window = tk.Toplevel()
    stock_window.title("Stock Information")

    # Create a frame to contain the stock information
    stock_frame = tk.Frame(stock_window)
    stock_frame.pack()

    # Create labels to display column names
    for col_index, column_name in enumerate(column_names):
        label = tk.Label(stock_frame, text=column_name)
        label.grid(row=0, column=col_index)

    # Create labels to display stock information
    for row_index, item in enumerate(stock):
        for col_index, value in enumerate(item):
            label = tk.Label(stock_frame, text=str(value))
            label.grid(row=row_index + 1, column=col_index)  # Offset by 1 to skip the header row


selected_cylinder_id = 1  # Replace this with the default cylinder ID you want to edit

def edit_stock_table():
    # Create a new window for editing stock information
    edit_window = tk.Toplevel()
    edit_window.title("Edit Stock")

    # Create labels and entry fields to edit stock information
    gas_type_label = tk.Label(edit_window, text="Gas Type:")
    gas_type_label.grid(row=0, column=0)

    # Retrieve gas types from the database
    gas_types = populate_gas_types()

    # Create a tkinter StringVar to hold the selected gas type
    selected_gas_type = tk.StringVar()
    selected_gas_type.set(gas_types[0])  # Set the default gas type

    # Create a dropdown menu for gas types
    gas_type_dropdown = tk.OptionMenu(edit_window, selected_gas_type, *gas_types)
    gas_type_dropdown.grid(row=0, column=1)

    status_label = tk.Label(edit_window, text="Status:")
    status_label.grid(row=1, column=0)
    status_entry = tk.Entry(edit_window)
    status_entry.grid(row=1, column=1)

    expiry_date_label = tk.Label(edit_window, text="Expiry Date:")
    expiry_date_label.grid(row=2, column=0)
    expiry_date_entry = tk.Entry(edit_window)
    expiry_date_entry.grid(row=2, column=1)

    price_label = tk.Label(edit_window, text="Price:")
    price_label.grid(row=3, column=0)
    price_entry = tk.Entry(edit_window)
    price_entry.grid(row=3, column=1)

    quantity_label = tk.Label(edit_window, text="Quantity:")
    quantity_label.grid(row=4, column=0)
    quantity_entry = tk.Entry(edit_window)
    quantity_entry.grid(row=4, column=1)

    # Function to update stock information
    def update_stock():
        new_gas_type = selected_gas_type.get()
        new_status = status_entry.get()
        new_expiry_date = expiry_date_entry.get()
        new_price = price_entry.get()
        new_quantity = quantity_entry.get()

        if any([new_gas_type, new_status, new_expiry_date, new_price, new_quantity]):
            # Update the GasCylinder table with the new information
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="gas_agency"
            )
            cursor = conn.cursor()

            # Create the SQL update query based on the provided values
            update_query = "UPDATE GasCylinder SET "
            update_values = []

            if new_gas_type:
                update_query += "GasType=%s, "
                update_values.append(new_gas_type)
            if new_status:
                update_query += "Status=%s, "
                update_values.append(new_status)
            if new_expiry_date:
                update_query += "ExpiryDate=%s, "
                update_values.append(new_expiry_date)
            if new_price:
                update_query += "Price=%s, "
                update_values.append(new_price)
            if new_quantity:
                update_query += "Quantity=%s, "
                update_values.append(new_quantity)

            # Remove the trailing comma and add the WHERE clause
            update_query = update_query.rstrip(", ") + " WHERE CylinderID=%s"
            update_values.append(selected_cylinder_id)

            cursor.execute(update_query, tuple(update_values))
            conn.commit()
            conn.close()
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill in at least one field.")

    update_button = tk.Button(edit_window, text="Update Stock", command=update_stock)
    update_button.grid(row=5, column=0, columnspan=2)

    # Close the edit window
    def close_window():
        edit_window.destroy()

    close_button = tk.Button(edit_window, text="Close", command=close_window)
    close_button.grid(row=6, column=0, columnspan=2)

    # Retrieve the selected gas cylinder's information
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT GasType, Status, ExpiryDate, Price, Quantity FROM GasCylinder WHERE CylinderID=%s", (selected_cylinder_id,))
    cylinder_info = cursor.fetchone()
    conn.close()

    if cylinder_info:
        # Display the cylinder information in the entry fields and dropdown
        selected_gas_type.set(cylinder_info[0])  # Set the gas type in the dropdown
        status_entry.insert(0, cylinder_info[1])
        expiry_date_entry.insert(0, cylinder_info[2])
        price_entry.insert(0, cylinder_info[3])
        quantity_entry.insert(0, cylinder_info[4])
    else:
        messagebox.showerror("Error", "Cylinder not found.")

def populate_gas_types():
    # Function to retrieve gas types from the database
    gas_types = []
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT GasType FROM GasCylinder")
    gas_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return gas_types


def display_low_stock():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    ) 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GasCylinder WHERE Status = 'Out of Stock'")
    low_stock = cursor.fetchall()
    column_names = [i[0] for i in cursor.description]  # Get the column names
    conn.close()

    # Create a new window to display low stock
    low_stock_window = tk.Toplevel()
    low_stock_window.title("Low Stock Items")

    # Create a frame to contain the low stock information
    low_stock_frame = tk.Frame(low_stock_window)
    low_stock_frame.pack()

    # Create labels to display column names
    for col_index, column_name in enumerate(column_names):
        label = tk.Label(low_stock_frame, text=column_name)
        label.grid(row=0, column=col_index)

    # Create labels to display low stock information
    for row_index, item in enumerate(low_stock):
        for col_index, value in enumerate(item):
            label = tk.Label(low_stock_frame, text=str(value))
            label.grid(row=row_index + 1, column=col_index)  # Offset by 1 to skip the header row

    # Close the low stock window
    def close_window():
        low_stock_window.destroy()

# Functions for the user block

# Function to update user details in the Customers table
def update_user_details(user_id, name, address, phone, email):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )

        cursor = conn.cursor()

        # Update the user's information in the Customers table
        cursor.execute("UPDATE Customer SET Name=%s, Address=%s, PhoneNumber=%s, Email=%s WHERE CustomerID=%s",
                       (name, address, phone, email, user_id))

        conn.commit()
        conn.close()
        messagebox.showinfo("Update Successful", "User details updated successfully.")
    except mysql.connector.Error as e:
        print("MySQL error:", e)
        messagebox.showerror("Update Failed", "Failed to update user details.")

# Function to open the user details update form
def open_update_user_details_form(user_id):
    update_form = tk.Toplevel()
    update_form.title("Update User Details")

    # Create labels and entry fields for user details
    name_label = tk.Label(update_form, text="Name:")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(update_form)
    name_entry.grid(row=0, column=1)

    address_label = tk.Label(update_form, text="Address:")
    address_label.grid(row=1, column=0)
    address_entry = tk.Entry(update_form)
    address_entry.grid(row=1, column=1)

    phone_label = tk.Label(update_form, text="Phone Number:")
    phone_label.grid(row=2, column=0)
    phone_entry = tk.Entry(update_form)
    phone_entry.grid(row=2, column=1)

    email_label = tk.Label(update_form, text="Email:")
    email_label.grid(row=3, column=0)
    email_entry = tk.Entry(update_form)
    email_entry.grid(row=3, column=1)

    # Function to handle the update of user details
    def handle_update():
        new_name = name_entry.get()
        new_address = address_entry.get()
        new_phone = phone_entry.get()
        new_email = email_entry.get()

        # Check each field before updating
        if new_name:
            update_name(user_id, new_name)
        if new_address:
            update_address(user_id, new_address)
        if new_phone:
            update_phone(user_id, new_phone)
        if new_email:
            update_email(user_id, new_email)
        print("Updated")
        update_form.destroy()

    update_button = tk.Button(update_form, text="Update", command=handle_update)
    update_button.grid(row=4, column=0, columnspan=2)

    # Close the update form
    close_button = tk.Button(update_form, text="Close", command=update_form.destroy)
    close_button.grid(row=5, column=0, columnspan=2)



def update_name(user_id, new_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = connection.cursor()

    update_query = "UPDATE customer SET name = %s WHERE CustomerID = %s"
    data = (new_name, user_id)

    cursor.execute(update_query, data)
    connection.commit()
    connection.close()

def update_address(user_id, new_address):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = connection.cursor()

        update_query = "UPDATE customer SET address = %s WHERE CustomerID = %s"
        data = (new_address, user_id)

        cursor.execute(update_query, data)
        connection.commit()
        connection.close()
        print("Address updated successfully")
    except mysql.connector.Error as error:
        print("Error updating address:", error)

# Example usage:
# You would call this function like this with the user_id and the new address:
# update_address(1, "123 Main St, City")

def update_phone(user_id, new_phone):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = connection.cursor()

        update_query = "UPDATE customer SET phone = %s WHERE CustomerID = %s"
        data = (new_phone, user_id)

        cursor.execute(update_query, data)
        connection.commit()
        connection.close()
        print("Phone number updated successfully")
    except mysql.connector.Error as error:
        print("Error updating phone number:", error)

# Example usage:
# You would call this function like this with the user_id and the new phone number:
# update_phone(1, "555-123-4567")

def update_email(user_id, new_email):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = connection.cursor()

        update_query = "UPDATE customer SET email = %s WHERE CustomerID = %s"
        data = (new_email, user_id)

        cursor.execute(update_query, data)
        connection.commit()
        connection.close()
        print("Email updated successfully")
    except mysql.connector.Error as error:
        print("Error updating email:", error)

# Example usage:
# You would call this function like this with the user_id and the new email:
# update_email(1, "newemail@example.com")


def user_verification():
    # Create a new window for user verification
    verification_window = tk.Toplevel()
    verification_window.title("User Verification")

    # Create labels and entry fields for username and password
    username_label = tk.Label(verification_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(verification_window)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(verification_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(verification_window, show="*")  # Show asterisks for password input
    password_entry.grid(row=1, column=1)

    # Function to verify user credentials
    def verify_user():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        # Query the UserCredentials table to check if the entered credentials match
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT UserID, Password FROM UserCredentials WHERE Username=%s", (entered_username,))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            stored_user_id, stored_password = result
            if entered_password == stored_password:
                messagebox.showinfo("Success", "User verified. Welcome!")
                verification_window.destroy()
                # Perform actions allowed for verified users, e.g., booking gas cylinders or viewing history
                # You can use the stored_user_id to identify the user for these actions
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "User not found.")

    verify_button = tk.Button(verification_window, text="Verify User", command=verify_user)
    verify_button.grid(row=2, column=0, columnspan=2)

    # Close the verification window
    def close_window():
        verification_window.destroy()

    close_button = tk.Button(verification_window, text="Close", command=close_window)
    close_button.grid(row=3, column=0, columnspan=2)

def display_booking_history(user_id):
    # Create a new window for displaying booking history
    history_window = tk.Toplevel()
    history_window.title("Booking History")

    # Create a listbox or a text widget to display the booking history
    history_listbox = tk.Listbox(history_window, width=50, height=10)
    history_listbox.grid(row=0, column=0, padx=10, pady=10)

    # Function to retrieve and display the booking history
    def load_booking_history():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT OrderID, OrderDate, Status FROM Orders WHERE CustomerID=%s", (user_id,))
        booking_history = cursor.fetchall()
        conn.close()

        if booking_history:
            for order in booking_history:
                order_id, order_date, status = order
                history_listbox.insert(tk.END, f"Order ID: {order_id}, Order Date: {order_date}, Status: {status}")
        else:
            history_listbox.insert(tk.END, "No booking history found.")

    load_booking_history()

    # Close the booking history window
    def close_window():
        history_window.destroy()

    close_button = tk.Button(history_window, text="Close", command=close_window)
    close_button.grid(row=1, column=0)


# Create a function to populate the gas type dropdown


def place_booking(user_id, gas_type, quantity, booking_window):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()
        result = 0  # Initialize result variable
        cursor.execute(
            "CALL BookGasCylinder(%s, %s, %s, @p_total_price)",
                (user_id, gas_type, quantity)
        )
        cursor.nextset()  # Move to the next result set

        # Execute a SELECT statement to retrieve the result from the @p_total_price variable
        cursor.execute("SELECT @p_total_price")
        result_set = cursor.fetchall()

        if result_set and result_set[0][0] > 0:
            total_price = result_set[0][0]
            messagebox.showinfo("Success", f"Order placed successfully. Total price: ${total_price:.2f}")
            booking_window.destroy()
        elif result_set and result_set[0][0] == 0:
            messagebox.showerror("Error", "Gas type not available in stock or insufficient quantity.")
        else:
            messagebox.showerror("Error", "Failed to place the order. Please try again later.")

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to place the order: {str(e)}")

def book_gas_cylinder(user_id):
    booking_window = tk.Toplevel()
    booking_window.title("Book Gas Cylinder")

    gas_type_label = tk.Label(booking_window, text="Gas Type:")
    gas_type_label.grid(row=0, column=0)

    gas_types = populate_gas_types()
    gas_type_var = tk.StringVar(booking_window)
    gas_type_var.set(gas_types[0] if gas_types else "No gas types available")
    gas_type_dropdown = tk.OptionMenu(booking_window, gas_type_var, *gas_types)
    gas_type_dropdown.grid(row=0, column=1)

    quantity_label = tk.Label(booking_window, text="Quantity:")
    quantity_label.grid(row=1, column=0)
    quantity_entry = tk.Entry(booking_window)
    quantity_entry.grid(row=1, column=1)


    def confirm_booking():
        gas_type = gas_type_var.get()
        quantity = quantity_entry.get()
        place_booking(user_id, gas_type, quantity, booking_window)

    confirm_button = tk.Button(booking_window, text="Confirm Booking", command=confirm_booking)
    confirm_button.grid(row=4, column=0, columnspan=2)

    def close_window():
        booking_window.destroy()

    close_button = tk.Button(booking_window, text="Close", command=close_window)
    close_button.grid(row=5, column=0, columnspan=2)
# Call book_gas_cylinder with the appropriate user_id to open the booking window
# Example: book_gas_cylinder(123)

  
def register_user(username, password):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )

        cursor = conn.cursor()

        # Check if the username is already in use
        cursor.execute("SELECT COUNT(*) FROM UserCredentials WHERE Username=%s", (username,))
        count = cursor.fetchone()[0]
        if count > 0:
            print("Username already exists. Please choose a different username.")
            return False

        # Insert the user's information into the UserCredentials table
        cursor.execute("INSERT INTO UserCredentials (Username, Password, Role) VALUES (%s, %s, %s)", (username, password, 'User'))

        conn.commit()
        conn.close()
        print("User registered successfully.")
        return True
    except mysql.connector.Error as e:
        print("MySQL error:", e)
        return False

# Example usage:
# register_user("user123", "password123")

def register_admin(username, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()

        # Check if the username is already in use
        cursor.execute("SELECT COUNT(*) FROM UserCredentials WHERE Username=%s", (username,))
        count = cursor.fetchone()[0]
        if count > 0:
            print("Username already exists. Please choose a different username.")
            return False

        # Insert the admin's information into the UserCredentials table with the role 'Admin'
        cursor.execute("INSERT INTO UserCredentials (Username, Password, Role) VALUES (%s, %s, %s)", (username, password, 'Admin'))

        conn.commit()
        conn.close()
        print("Admin registered successfully.")
        return True
    except mysql.connector.Error as e:
        print("MySQL error:", e)
        return False

# Example usage:
# register_admin("admin123", "adminpassword123")

# Function to check if a user is an admin
def is_admin(username):
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
    cursor = conn.cursor()
    cursor.execute("SELECT Role FROM UserCredentials WHERE Username = %s", (username,))
    role = cursor.fetchone()
    conn.close()
    return role and role[0] == "Admin"

# Function to verify user credentials
def verify_user(username, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="gas_agency"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Password, UserID FROM UserCredentials WHERE Username=%s", (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data and user_data[1] == password:
            return user_data[2]
        else:
            return None
    except mysql.connector.Error as e:
        print("MySQL error:", e)
        return None
    
# Function to open the user login window
def open_user_login_window():
    user_login_window = tk.Toplevel()
    user_login_window.title("User Login")

    # Create labels and entry fields for username and password
    username_label = tk.Label(user_login_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(user_login_window)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(user_login_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(user_login_window, show="*")  # Show asterisks for password input
    password_entry.grid(row=1, column=1)

    def handle_user_login():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        user_id = verify_user(entered_username, entered_password)

        if user_id:
            if is_admin(entered_username):
                open_admin_window()
            else:
                open_user_window(user_id)
            user_login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_button = tk.Button(user_login_window, text="Login", command=handle_user_login)
    login_button.grid(row=2, column=0, columnspan=2)

# Function to open the admin login window
def open_admin_login_window():
    admin_login_window = tk.Toplevel()
    admin_login_window.title("Admin Login")

    # Create labels and entry fields for username and password
    username_label = tk.Label(admin_login_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(admin_login_window)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(admin_login_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(admin_login_window, show="*")
    password_entry.grid(row=1, column=1)

    def handle_admin_login():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        user_id = verify_user(entered_username, entered_password)

        if user_id and is_admin(entered_username):
            open_admin_window()
            admin_login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials.")

    login_button = tk.Button(admin_login_window, text="Login", command=handle_admin_login)
    login_button.grid(row=2, column=0, columnspan=2)

# Function to open the admin window
def open_admin_window():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")

    # Create buttons for admin actions
    button1 = tk.Button(admin_window, text="Display Users", command=display_users_table)
    button1.pack()

    button2 = tk.Button(admin_window, text="Display Employees", command=display_employee_table)
    button2.pack()

    button3 = tk.Button(admin_window, text="Edit Employee", command=edit_employee_table)
    button3.pack()  # Add an "Edit Employee" button here
    
    button4 = tk.Button(admin_window, text="Display Stock", command=display_stock_table)
    button4.pack() 

    button5 = tk.Button(admin_window, text="Edit Stock", command=edit_stock_table)
    button5.pack()

    button6 = tk.Button(admin_window, text="Display Low Stock", command=display_low_stock)
    button6.pack()

    # You can add more buttons for other admin functionalities

    # Close the admin window
    close_button = tk.Button(admin_window, text="Close", command=admin_window.destroy)
    close_button.pack()

def open_user_window(user_id):
    user_window = tk.Toplevel()
    user_window.title("User Dashboard")

    # Create buttons for user actions
    button1 = tk.Button(user_window, text="Book Gas Cylinder", command=lambda: book_gas_cylinder(user_id))
    button1.pack()

    button2 = tk.Button(user_window, text="View Booking History", command=lambda: display_booking_history(user_id))
    button2.pack()

    update_user_details_button = tk.Button(user_window, text="Update User Details", command=lambda: open_update_user_details_form(user_id))
    update_user_details_button.pack()

    # Close the user window
    close_button = tk.Button(user_window, text="Close", command=user_window.destroy)
    close_button.pack()

def open_user_registration():
    user_registration_window = tk.Toplevel()
    user_registration_window.title("User Registration")

    # Create labels and entry fields for user details
    name_label = tk.Label(user_registration_window, text="Name:")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(user_registration_window)
    name_entry.grid(row=0, column=1)

    address_label = tk.Label(user_registration_window, text="Address:")
    address_label.grid(row=1, column=0)
    address_entry = tk.Entry(user_registration_window)
    address_entry.grid(row=1, column=1)

    phone_label = tk.Label(user_registration_window, text="Phone Number:")
    phone_label.grid(row=2, column=0)
    phone_entry = tk.Entry(user_registration_window)
    phone_entry.grid(row=2, column=1)

    email_label = tk.Label(user_registration_window, text="Email:")
    email_label.grid(row=3, column=0)
    email_entry = tk.Entry(user_registration_window)
    email_entry.grid(row=3, column=1)

    username_label = tk.Label(user_registration_window, text="Username:")
    username_label.grid(row=4, column=0)
    username_entry = tk.Entry(user_registration_window)
    username_entry.grid(row=4, column=1)

    password_label = tk.Label(user_registration_window, text="Password:")
    password_label.grid(row=5, column=0)
    password_entry = tk.Entry(user_registration_window, show="*")
    password_entry.grid(row=5, column=1)

    # Function to handle user registration
    def handle_user_registration():
        entered_name = name_entry.get()
        entered_address = address_entry.get()
        entered_phone = phone_entry.get()
        entered_email = email_entry.get()
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        if entered_name and entered_address and entered_phone and entered_email and entered_username and entered_password:
            # Register user in the UserCredentials table
            register_user(entered_username, entered_password)
            # Insert customer details into the Customer table
            insert_customer_details(entered_name, entered_address, entered_phone, entered_email)
            messagebox.showinfo("Registration Successful", "User registered successfully.")
            user_registration_window.destroy()
        else:
            messagebox.showerror("Registration Failed", "Please fill in all fields.")

    register_button = tk.Button(user_registration_window, text="Register", command=handle_user_registration)
    register_button.grid(row=6, column=0, columnspan=2)

# Function to insert customer details into the Customer table
def insert_customer_details(name, address, phone, email):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Customer (Name, Address, PhoneNumber, Email) VALUES (%s, %s, %s, %s)",
                   (name, address, phone, email))
    connection.commit()
    connection.close()

# Function to register a user in the UserCredentials table
def register_user(username, password):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="gas_agency"
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO UserCredentials (Username, Password, Role) VALUES (%s, %s, %s)",
                   (username, password, "user"))
    connection.commit()
    connection.close()
# Function to open the admin registration window
def open_admin_registration():
    admin_registration_window = tk.Toplevel()
    admin_registration_window.title("Admin Registration")

    # Create labels and entry fields for username and password
    username_label = tk.Label(admin_registration_window, text="Username:")
    username_label.grid(row=0, column=0)
    username_entry = tk.Entry(admin_registration_window)
    username_entry.grid(row=0, column=1)

    password_label = tk.Label(admin_registration_window, text="Password:")
    password_label.grid(row=1, column=0)
    password_entry = tk.Entry(admin_registration_window, show="*")
    password_entry.grid(row=1, column=1)

    def handle_admin_registration():
        entered_username = username_entry.get()
        entered_password = password_entry.get()

        if entered_username and entered_password:
            register_admin(entered_username, entered_password)
            messagebox.showinfo("Registration Successful", "Admin registered successfully.")
            admin_registration_window.destroy()
        else:
            messagebox.showerror("Registration Failed", "Please fill in all fields.")

    register_button = tk.Button(admin_registration_window, text="Register", command=handle_admin_registration)
    register_button.grid(row=2, column=0, columnspan=2)

# Create buttons to open the login windows
user_login_button = tk.Button(root, text="User Login", command=open_user_login_window)
user_login_button.pack()

admin_login_button = tk.Button(root, text="Admin Login", command=open_admin_login_window)
admin_login_button.pack()

# Create buttons to open registration forms
user_registration_button = tk.Button(root, text="User Registration", command=open_user_registration)
user_registration_button.pack()

admin_registration_button = tk.Button(root, text="Admin Registration", command=open_admin_registration)
admin_registration_button.pack()

# Run the Tkinter main loop
tk.mainloop()