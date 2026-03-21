# DAX Measures Documentation

Since Power BI `.pbix` files are binary, this document provides visibility into the key analytical logic used in the `Customer Behavior Dashboard`.

## 📈 Sales Performance

### Total Sales (USD)
Calculates the absolute sum of all purchase amounts.
```dax
Total Sales = SUM('Sales'[Purchase Amount (USD)])
```

### Average Transaction Value (ATV)
The average spending per transaction.
```dax
ATV = AVERAGE('Sales'[Purchase Amount (USD)])
```

## 👥 Customer Loyalty

### Total Customers
Count of unique customer entries.
```dax
Total Customers = DISTINCTCOUNT('Sales'[Customer ID])
```

### High Value Customers (HVC)
Customers who have spent above $500 in total.
```dax
HVC Count = 
CALCULATE(
    [Total Customers],
    FILTER(
        VALUES('Sales'[Customer ID]),
        [Total Sales] > 500
    )
)
```

## 📊 Growth Metrics

### Sales WoW (Week over Week)
Comparison of sales against the previous week.
```dax
Sales WoW % = 
VAR CurrentWeekSales = [Total Sales]
VAR PreviousWeekSales = CALCULATE([Total Sales], DATEADD('Date'[Date], -7, DAY))
RETURN
DIVIDE(CurrentWeekSales - PreviousWeekSales, PreviousWeekSales)
```
