-- Package Body for inventory_management
CREATE OR REPLACE PACKAGE BODY inventory_management IS

  -- Procedure to add a new item to the inventory table
  PROCEDURE add_item(item_id NUMBER, item_name VARCHAR2, quantity NUMBER) IS
  BEGIN
    -- Insert the item id, name, and quantity into the inventory table
    INSERT INTO inventory (id, name, qty) VALUES (item_id, item_name, quantity);
  END add_item;

  -- Procedure to remove an item from the inventory table
  PROCEDURE remove_item(item_id NUMBER) IS
  BEGIN
    -- Delete the item record from the inventory table based on the provided item id
    DELETE FROM inventory WHERE id = item_id;
  END remove_item;

  -- Function to get the quantity of an item based on its id
  FUNCTION get_item_quantity(item_id NUMBER) RETURN NUMBER IS
    qty NUMBER; -- Variable to store the item quantity
  BEGIN
    -- Select the item quantity from the inventory table based on the item id
    SELECT qty INTO qty FROM inventory WHERE id = item_id;
    -- Return the item quantity
    RETURN qty;
  END get_item_quantity;

END inventory_management;
