# Customer Behavior Analysis & API

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=flat&logo=Jupyter&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2.svg?style=flat&logo=MLflow&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=Power-BI&logoColor=black)
![Build Status](https://github.com/toxicbishop/Customer-Behavior-Analysis-Power-BI/actions/workflows/python-test.yml/badge.svg)

This project demonstrates a complete end-to-end data analytics and machine learning workflow. It includes data processing, exploratory analysis, relational SQL querying, star schema modeling, and a Django REST API for serving ML models.

## Project Structure

```text
customer_behavior_analysis/
├── .github/workflows/         # CI/CD Automation (Python Testing)
├── api/                       # Django REST API
│   ├── manage.py
│   ├── customer_behavior_django_api/
│   └── ml_models/             # ML endpoints & models
├── data/                      # Raw and Processed Datasets
│   ├── processed/             # Star Schema (Fact/Dim tables)
│   └── data_dictionary.md     # Documentation of dataset columns
├── notebooks/                 # Jupyter Analysis & EDA
├── powerbi/                   # Visualization & Dashboarding
│   ├── dashboard.pbix         # Main Power BI Report
│   └── DAX_Measures.md        # Documentation of analytical logic
├── scripts/                   # Utility Scripts (Data Diversification)
├── sql/                       # SQL Scripts (Analysis & Joins)
├── requirements.txt           # Versioned project dependencies
└── README.md                  # This file
```

## Analytics Workflow

1.  **Data Diversification**: Original CSV is processed via `scripts/data_diversification.py` into a Star Schema.
2.  **Relational Modeling**: Clean Dimension (`DIM_Customers`, `DIM_Products`) and Fact (`FACT_Sales`) tables are created.
3.  **Advanced Analytics**:
    *   **Sentiment Analysis**: Integration of customer review data.
    *   **Inventory Tracking**: Monitoring stock levels versus purchase frequency.
4.  **SQL Relational Analysis**: Complex joins and aggregations performed in `sql/relational_analysis.sql`.
5.  **Power BI Dashboard**: Interactive visualizations including WoW growth and high-value customer segments.

## Machine Learning API

Serve predictions via Django REST Framework.

### Endpoints

- `/segment/` : Customer segmentation
- `/predict/` : Purchase prediction
- `/churn/` : Churn prediction
- `/recommend/` : Product recommendation

### Features

- MLflow integration for model tracking.
- Modular pipeline for training and deployment.
- Automatic testing via GitHub Actions.

## Setup & Installation

1.  **Clone the Repository**

    ```bash
    git clone <repo_url>
    cd customer_behavior_analysis
    ```

2.  **Environment Setup**

    ```bash
    python -m venv .venv
    # On Windows: .venv\Scripts\activate
    # On Unix: source .venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Running the API**

    ```bash
    cd api
    python manage.py migrate
    python manage.py runserver
    ```

## Dashboard Preview

![Power BI Dashboard Screenshot](powerbi/dashboard.png)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
