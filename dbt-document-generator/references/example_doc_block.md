
{% docs customer_lifetime_value_doc %}
# Customer Lifetime Value Model

## Business Overview
This model calculates the predicted Customer Lifetime Value (CLV) for each customer based on their historical transaction patterns, purchase frequency, and engagement metrics. The CLV metric helps marketing teams identify high-value customers for targeted campaigns and retention strategies. Business stakeholders use this data to allocate marketing budgets, prioritize customer segments, and forecast long-term revenue potential.

## Technical Implementation
The model employs a cohort-based analysis approach, combining recency, frequency, and monetary (RFM) analysis with predictive modeling. Key transformations include:

- **Cohort Analysis**: Groups customers by their first purchase month to analyze retention patterns
- **RFM Scoring**: Calculates recency (days since last purchase), frequency (purchase count), and monetary (average order value) scores
- **Predictive Modeling**: Uses historical data to project future purchase behavior over 12 months
- **Materialization**: Configured as a table with daily refresh to ensure accuracy for marketing campaigns

The model handles data quality through null value treatment and outlier detection, ensuring reliable CLV calculations.

## Data Dictionary

| Column Name | Data Type | Business Description | Source Table/Calculation | Example Values | Data Quality Notes |
|-------------|-----------|---------------------|--------------------------|----------------|-------------------|
| customer_id | STRING | Unique customer identifier | customers.customer_id | 'CUST_12345' | Primary key, not null |
| clv_12_months | DECIMAL(10,2) | Predicted revenue over 12 months | Calculated from purchase history | 245.67 | Always positive |
| rfm_score | INTEGER | Combined RFM score (1-5 scale) | Calculated from recency, frequency, monetary | 4 | Range: 1-5 |
| cohort_month | DATE | Month of first purchase | MIN(orders.order_date) | '2023-01-01' | Format: YYYY-MM-DD |
| last_purchase_date | DATE | Date of most recent purchase | MAX(orders.order_date) | '2024-07-15' | May be null for inactive customers |
| total_orders | INTEGER | Total number of orders placed | COUNT(orders.order_id) | 8 | Minimum 1 |
| avg_order_value | DECIMAL(8,2) | Average order value | AVG(orders.total_amount) | 45.23 | Excludes refunds |
| customer_segment | STRING | Marketing segment classification | CASE WHEN clv_12_months > 500 THEN 'High Value' | 'Medium Value' | 4 segments: High, Medium, Low, New |

{% enddocs %}
