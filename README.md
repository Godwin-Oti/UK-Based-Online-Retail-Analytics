# UK-Based Online Retail Analysis, Customer Behaviour & Price Prediction
## Overview

This project focuses on the analysis of a UK-based online retail dataset containing transactional data from a non-store retailer. The dataset spans transactions between December 1, 2010, and December 9, 2011, and includes customer behaviors, product performance, and sales trends. The analysis also delves into customer segmentation, spending habits, and geographic revenue distribution, while utilizing predictive models to provide actionable insights.

## Business Objectives

### The primary goal of this project is to derive actionable insights and recommendations to:

* Optimize business strategies.

* Enhance customer experience and retention.

* Identify high-demand products and areas for improvement.

* Enable data-driven decision-making for stakeholders.

## Key Findings

1. **Seasonal Sales Trends**

* Insight: November has the highest sales (holiday season), while February experiences the lowest sales.

* Action: Ramp up marketing and promotions in October-November.

2. **Daily and Weekly Sales Patterns**

* Insight: Sales peak during the first week of the month and on weekdays (especially Thursdays), with no sales on Saturdays.

* Action: Introduce first-week promotions and create incentives for Saturdays.

3. **Geographic Revenue Distribution**

* Insight: The UK contributes the highest revenue, while Ireland, Iceland, and Singapore have the highest average spending per customer.

* Action: Focus targeted campaigns on high-spending countries while maintaining competitive pricing in the UK.

4. **Top Products and Cancellations**

* Insight: The WHITE HANGING HEART T-LIGHT HOLDER generates the most revenue, while the REGENCY CAKESTAND 3 TIER has the highest cancellation rate.

* Action: Monitor product quality for high-cancellation items and promote high-demand items during peak seasons.

## Methodology

### The project follows these steps:

1. **Data Cleaning:**

* Handled missing values, Outliers, and inconsistent data.

* Converted data types and extracted relevant date-time features.

2. **Exploratory Data Analysis (EDA):**

* Analyzed sales trends by time, geography, and product.

* Identified customer segments and spending patterns.

3. **Customer Segmentation:**

* Used RFM (Recency, Frequency, Monetary) analysis to classify customers into categories such as high-value and low-value segments.

4. **Predictive Modeling:**

* Built models to predict customer churn, product demand, and pricing strategies.

* Utilized techniques such as random forest, K-means clustering, and scaling.

## Tools and Technologies

* Python: For data cleaning, analysis, and modeling.

* Pandas, NumPy: Data manipulation and preprocessing.

* Matplotlib, Seaborn: Data visualization.

* Scikit-learn: Machine learning models.
  
* Excel: Data Evaluation

* Git: Version control.

## How to Run the Project

* Clone the repository:
```bash
   git clone https://github.com/Godwin-Oti/UK-Based-Online-Retail-Analytics.git
```
* Navigate to the project directory:
```bash
   cd UK-Based-Online-Retail-Analytics
```

* Install the required dependencies:
```bash
  pip install -r requirements.txt
```
* Run the analysis notebook or scripts to reproduce the findings.

## Recommendations

* Seasonal Promotions: Leverage November’s peak sales by offering holiday discounts.

* Target High-Spending Customers: Design exclusive loyalty programs for top spenders in high-value regions (e.g., Ireland).

* Reduce Cancellations: Enhance product quality control and provide clearer descriptions for frequently canceled products.

* Promotions for Off-Peak Days: Offer deals on Saturdays and the last week of the month to balance sales trends.

## Results

The project successfully identifies sales trends, customer behaviors, and product insights that can help the business make data-driven decisions to enhance profitability and customer satisfaction.

## Future Work

* Incorporate more advanced models for dynamic pricing strategies.

* Expand the analysis to include external factors (e.g., economic conditions or competitor data).

* Integrate real-time dashboards for continuous monitoring.

## License

This project is licensed under the MIT License. See the [LICENSE](License) file for details.

