# Data Dictionary (Star Schema Edition)

This document describes the columns and relationships in the structured `data/processed` directory.

## 🏗 Schema Overview
The data is now structured in a **Star Schema** (Dim/Fact model), which is industry standard for analytical workloads.

---

## 🛒 DIM_Products (`dim_products.csv`)
| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Product ID** | Unique Identifier for each item/category combination. | Integer |
| **Item Purchased** | Name of the product (e.g., Sandals, Hoodie). | String |
| **Category** | High-level category (e.g., Clothing, Accessories). | String |

## 👥 DIM_Customers (`dim_customers.csv`)
| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Customer ID** | Unique identifier for the customer. | Integer |
| **Age** | Age of the customer. | Integer |
| **Gender** | Gender profile. | String |
| **Location** | Geographical state location. | String |
| **Subscription Status** | Loyalty program membership indicator. | String |

## 💰 FACT_Sales (`fact_sales.csv`)
| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Customer ID** | Key to `DIM_Customers`. | Integer |
| **Product ID** | Key to `DIM_Products`. | Integer |
| **Purchase Amount (USD)** | Total value of the transaction. | Float |
| **Size / Color / Season** | Line item specific attributes. | String |
| **Review Rating** | Numerical score given by customer. | Float |
| **Previous Purchases** | History of customer engagement. | Integer |

## 📝 Customer Reviews (`customer_reviews.csv`)
| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Customer ID** | Key to `DIM_Customers`. | Integer |
| **Review Text** | Unstructured feedback from the customer. | Text |
| **Review Date** | When the review was recorded. | Date |

## 📦 Inventory Logs (`inventory_logs.csv`)
| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Product ID** | Key to `DIM_Products`. | Integer |
| **Stock Level** | Current count of items in the warehouse. | Integer |
| **Last Restock Date** | Date of recent inventory replenishment. | Date |
