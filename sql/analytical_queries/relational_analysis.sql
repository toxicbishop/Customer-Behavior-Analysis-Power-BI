-- ==========================================================
-- Customer Behavior Relational Analysis Queries
-- These queries demonstrate how to join the Star Schema
-- created in the data/processed directory.
-- ==========================================================

-- 1. Combine Fact and Dimensions to see full sales records
-- Purpose: To get a human-readable "Full View" of every transaction.
SELECT 
    f.[Customer ID],
    c.[Age],
    c.[Gender],
    c.[Location],
    p.[Item Purchased],
    p.[Category],
    f.[Purchase Amount (USD)],
    f.[Review Rating]
FROM FACT_Sales f
INNER JOIN DIM_Customers c ON f.[Customer ID] = c.[Customer ID]
INNER JOIN DIM_Products p ON f.[Product ID] = p.[Product ID];

-- 2. Correlating Sentiment with Purchase Behavior
-- Purpose: See if customers who leave "Amazing" reviews spend more on average.
SELECT 
    CASE 
        WHEN r.[Review Text] LIKE '%Amazing%' OR r.[Review Text] LIKE '%Excellent%' THEN 'Positive'
        WHEN r.[Review Text] LIKE '%disappointed%' OR r.[Review Text] LIKE '%cheap%' THEN 'Negative'
        ELSE 'Neutral'
    END AS Sentiment,
    AVG(f.[Purchase Amount (USD)]) as AvgSpend,
    COUNT(f.[Customer ID]) as TotalTransactions
FROM FACT_Sales f
JOIN Customer_Reviews r ON f.[Customer ID] = r.[Customer ID]
GROUP BY 
    CASE 
        WHEN r.[Review Text] LIKE '%Amazing%' OR r.[Review Text] LIKE '%Excellent%' THEN 'Positive'
        WHEN r.[Review Text] LIKE '%disappointed%' OR r.[Review Text] LIKE '%cheap%' THEN 'Negative'
        ELSE 'Neutral'
    END;

-- 3. Inventory Status & Out of Stock Risk
-- Purpose: Show which products are in high demand but low stock.
-- High demand = Review Rating > 4.5 and Stock Level < 20.
SELECT 
    p.[Item Purchased],
    p.[Category],
    i.[Stock Level],
    AVG(f.[Review Rating]) as AvgRating
FROM FACT_Sales f
JOIN DIM_Products p ON f.[Product ID] = p.[Product ID]
JOIN Inventory_Logs i ON p.[Product ID] = i.[Product ID]
GROUP BY p.[Item Purchased], p.[Category], i.[Stock Level]
HAVING i.[Stock Level] < 20 AND AVG(f.[Review Rating]) > 4.5
ORDER BY i.[Stock Level] ASC;
