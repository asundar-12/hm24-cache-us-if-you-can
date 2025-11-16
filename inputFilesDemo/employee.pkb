-- Package Body for employee_management
CREATE OR REPLACE PACKAGE BODY employee_management IS

  -- Procedure to add a new employee to the employees table
  PROCEDURE add_employee(emp_id NUMBER, emp_name VARCHAR2) IS
  BEGIN
    -- Insert the employee's id and name into the employees table
    INSERT INTO employees (id, name) VALUES (emp_id, emp_name);
  END add_employee;

  -- Procedure to remove an employee from the employees table
  PROCEDURE remove_employee(emp_id NUMBER) IS
  BEGIN
    -- Delete the employee record based on the provided employee id
    DELETE FROM employees WHERE id = emp_id;
  END remove_employee;

  -- Function to get the name of an employee based on their id
  FUNCTION get_employee_name(emp_id NUMBER) RETURN VARCHAR2 IS
    emp_name VARCHAR2(100); -- Variable to store employee's name
  BEGIN
    -- Select the employee's name from the employees table based on the employee id
    SELECT name INTO emp_name FROM employees WHERE id = emp_id;
    -- Return the employee's name
    RETURN emp_name;
  END get_employee_name;

END employee_management;
