# ECE Retail Data Analysis Dashboard

This project analyzes retail data with an ECE (Electrical and Computer Engineering) focus, transforming traditional retail metrics into ECE domain-specific terminology and visualizations.

## Features

- Interactive data visualizations using Plotly
- ECE domain-specific terminology and metrics
- Comprehensive analysis of sales trends, customer behavior, and product performance
- Modern, responsive web dashboard

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ece_retail_analysis.git
cd ece_retail_analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the analysis:
```bash
python retail_analysis.py
```

5. Open the dashboard:
```bash
python -m http.server 8000
```
Then visit http://localhost:8000 in your browser.

## Project Structure

- `retail_analysis.py`: Main analysis script
- `update_products.py`: Script to update product names with ECE terminology
- `index.html`: Main dashboard page
- `online_retail_II_ece.csv`: ECE-modified dataset
- `requirements.txt`: Python dependencies

## Visualizations

The dashboard includes the following visualizations:
- Daily Sales Trends
- Top Products Analysis
- Customer Behavior Patterns
- Regional Sales Distribution
- Country Performance Metrics
- Product Performance Analysis
- Cohort Analysis
- Timeline Analysis

## License

This project is licensed under the MIT License - see the LICENSE file for details. 