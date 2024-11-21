# GasLink
a Gas Booking Agency built with Python
## Overview
This is a comprehensive application designed to manage gas cylinder inventory, user registration, booking processes, and administrative functionalities. It provides a user-friendly interface for customers to book gas cylinders and for administrators to manage stock and user information.

## Features
- **User  Management:**
  - User registration and login
  - Admin login for management functionalities
  - User verification process

- **Gas Cylinder Management:**
  - View and edit gas cylinder stock
  - Display low stock items
  - Update gas cylinder details (type, status, expiry date, price, quantity)

- **Booking System:**
  - Users can book gas cylinders by selecting type and quantity
  - Order management with booking history

- **Database Interaction:**
  - MySQL database for storing user and cylinder information
  - CRUD operations on various tables

- **Admin Dashboard:**
  - Manage users and employees
  - View stock and reports

- **Triggers and Procedures:**
  - Database triggers to manage stock status
  - Stored procedures for booking gas cylinders

## Requirements
- **Software:**
  - Python 3.x
  - Tkinter (for GUI)
  - MySQL Connector (for database interactions)
  
- **Database:**
  - MySQL Server
  - Database schema with necessary tables:
    - UserCredentials
    - Customer
    - Employee
    - GasCylinder
    - Orders
    - Payment
- Create a database named **gas_agency**.
Execute the SQL scripts provided in the table.py file to create necessary tables.
