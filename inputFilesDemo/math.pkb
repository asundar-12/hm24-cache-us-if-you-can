-- Package Body for math_operations
CREATE OR REPLACE PACKAGE BODY math_operations IS

  -- Function to add two numbers
  FUNCTION add_numbers(a NUMBER, b NUMBER) RETURN NUMBER IS
  BEGIN
    -- Return the sum of the two numbers
    RETURN a + b;
  END add_numbers;

  -- Function to subtract two numbers
  FUNCTION subtract_numbers(a NUMBER, b NUMBER) RETURN NUMBER IS
  BEGIN
    -- Return the result of subtracting b from a
    RETURN a - b;
  END subtract_numbers;

END math_operations;
