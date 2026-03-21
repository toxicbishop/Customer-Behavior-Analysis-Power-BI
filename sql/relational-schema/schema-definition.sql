-- ==========================================================
-- Star Schema Creation Script
-- This script outlines the Logical DDL for the project.
-- ==========================================================

-- 1. Product Dimension
CREATE TABLE DIM_Products (
    ProductID INT PRIMARY KEY,
    ItemName VARCHAR(100),
    Category VARCHAR(50)
);

-- 2. Customer Dimension
CREATE TABLE DIM_Customers (
    CustomerID INT PRIMARY KEY,
    Age INT,
    Gender VARCHAR(20),
    Location VARCHAR(100),
    IsSubscriber BIT
);

-- 3. Sales Fact Table
CREATE TABLE FACT_Sales (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES DIM_Customers(CustomerID),
    ProductID INT FOREIGN KEY REFERENCES DIM_Products(ProductID),
    PurchaseAmount DECIMAL(10,2),
    PurchaseDate DATETIME,
    ReviewRating FLOAT,
    PaymentMethod VARCHAR(50)
);

-- 4. Unstructured Feedback
CREATE TABLE Customer_Reviews (
    ReviewID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES DIM_Customers(CustomerID),
    ReviewText TEXT,
    ReviewDate DATETIME
);
