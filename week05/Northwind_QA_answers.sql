--Throughout the week write SQL queries to answer the questions below

--#1.Get the names and the quantities in stock for each product.
SELECT productname, sum(unitsinstock) as total_stock_units
FROM products
group by productname
order by total_stock_units DESC;

--#2.Get a list of current products (Product ID and name).
SELECT productid, productname
FROM products
ORDER BY productid;

--#3.Get a list of the most and least expensive products (name and unit price).
SELECT productname, unitprice
FROM products
ORDER BY unitprice DESC;

--#4.Get products that cost less than $20.
SELECT productname, unitprice
FROM products WHERE unitprice < 20;

--#5.Get products that cost between $15 and $25.
SELECT productname, unitprice
FROM products WHERE ((unitprice >= 15) AND (unitprice <=25));

--#6.Get products above average price.
SELECT productname, unitprice
FROM products
WHERE unitprice < (SELECT avg(unitprice) FROM products);


--#7.Find the ten most expensive products.
SELECT productname, unitprice
FROM products
ORDER BY unitprice DESC
LIMIT 10;

--#8.Get a list of discontinued products (Product ID and name).
SELECT productid, productname
FROM products
WHERE discontinued = 1;

--#9.Count current and discontinued products.
SELECT discontinued, count(*)
FROM products
GROUP BY discontinued;

--#10.Find products with less units in stock than the quantity on order.
SELECT productname, unitsinstock, unitsonorder
FROM products
WHERE unitsinstock < unitsonorder;

--#11.Find the customer who had the highest order amount
---table 1: customers (customerid, contactname)
---table 2 : order (customerid, orderid)
---table 3: order_details (orderid, productid,quantity)

SELECT ct.customerid
     , ct.contactname
     , od. orderid
     , od.unitprice
     , od.quantity
     , od.discount
     , round((od.unitprice * od.quantity)*(1-od.discount)) as revenue
FROM customers ct
LEFT JOIN orders o ON ct.customerid = o.customerid
LEFT JOIN order_details od ON o.orderid = od.orderid
WHERE od.orderid IS NOT NULL
ORDER BY revenue DESC
LIMIT 1;

--#12.Get orders for a given employee and the according customer
--table 1: orders (order id, employee id, customerid )
--table 2: employee
--table 3:customer

--#13.Find the hiring age of each employee
--table 1: employee table
SELECT * FROM employees LIMIT 10;

--#14.Create views and/or named queries for some of these queries

