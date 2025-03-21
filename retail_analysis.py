import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import webbrowser
import os

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_and_preprocess_data(file_path):
    """Load and preprocess the retail data"""
    # Read CSV with low_memory=False to handle mixed types
    df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
    
    # Rename columns with ECE domain terminology
    df.rename(columns={
        'Invoice': 'Packet_ID',
        'StockCode': 'Sensor_ID',
        'Description': 'Sensor_Type',
        'Quantity': 'Signal_Strength',
        'Price': 'SNR',
        'Customer ID': 'Receiver_ID',
        'Country': 'Transmission_Zone',
        'Total': 'Effective_Throughput'
    }, inplace=True)
    
    # Convert to numeric and handle missing values
    df['SNR'] = pd.to_numeric(df['SNR'], errors='coerce')
    df['Signal_Strength'] = pd.to_numeric(df['Signal_Strength'], errors='coerce')
    df['Effective_Throughput'] = df['Signal_Strength'] * df['SNR']
    
    # Convert InvoiceDate to datetime with error handling
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%y %H:%M', errors='coerce')
    df = df.dropna(subset=['InvoiceDate'])  # Remove rows with invalid dates
    
    return df

def analyze_sales_trends(df):
    """Analyze and visualize sales trends"""
    # Daily sales trend
    daily_sales = df.groupby(df['InvoiceDate'].dt.date)['Effective_Throughput'].sum().reset_index()
    
    fig = px.line(daily_sales, x='InvoiceDate', y='Effective_Throughput',
                  title='Daily Sales Trend',
                  labels={'Effective_Throughput': 'Daily Sales Volume'})
    fig.write_html('daily_sales_trend.html')
    
    # Top products by sales
    top_products = df.groupby('Sensor_Type')['Effective_Throughput'].sum().sort_values(ascending=False).head(10)
    
    fig = px.bar(top_products, title='Top 10 Products by Sales',
                 labels={'value': 'Sales Volume', 'index': 'Product'})
    fig.write_html('top_products.html')

def analyze_customer_behavior(df):
    """Analyze customer purchasing patterns"""
    # Customer purchase frequency
    customer_freq = df.groupby('Receiver_ID').size().reset_index(name='Purchase_Frequency')
    
    fig = px.histogram(customer_freq, x='Purchase_Frequency',
                      title='Customer Purchase Frequency Distribution',
                      labels={'Purchase_Frequency': 'Number of Purchases'})
    fig.write_html('customer_frequency.html')
    
    # Geographic analysis
    country_sales = df.groupby('Transmission_Zone')['Effective_Throughput'].sum().reset_index()
    
    fig = px.pie(country_sales, values='Effective_Throughput', names='Transmission_Zone',
                 title='Sales Distribution by Region')
    fig.write_html('regional_sales.html')

def analyze_country_performance(df):
    """Analyze country performance metrics"""
    # Total purchase amount by country
    country_purchases = df.groupby(['Transmission_Zone'], as_index=False)['Effective_Throughput'].agg('sum')
    
    # Top and bottom 10 countries by purchase amount
    top_countries = country_purchases.nlargest(10, 'Effective_Throughput')
    bottom_countries = country_purchases.nsmallest(10, 'Effective_Throughput')
    
    # Plot top countries
    fig = go.Figure(data=[go.Bar(
        name='Top Countries',
        x=top_countries['Transmission_Zone'],
        y=top_countries['Effective_Throughput'],
        marker={'color': top_countries['Effective_Throughput'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Top 10 Countries by Purchase Amount',
        xaxis_title="Countries",
        yaxis_title="Total Amount",
        plot_bgcolor='white'
    )
    fig.write_html('top_countries.html')
    
    # Plot bottom countries
    fig = go.Figure(data=[go.Bar(
        name='Bottom Countries',
        x=bottom_countries['Transmission_Zone'],
        y=bottom_countries['Effective_Throughput'],
        marker={'color': bottom_countries['Effective_Throughput'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Bottom 10 Countries by Purchase Amount',
        xaxis_title="Countries",
        yaxis_title="Total Amount",
        plot_bgcolor='white'
    )
    fig.write_html('bottom_countries.html')
    
    # Unique customers by country
    country_customers = df.groupby(['Transmission_Zone'], as_index=False)['Receiver_ID'].agg({'Receiver_ID': 'nunique'})
    country_customers.rename(columns={'Receiver_ID': 'Customer_Count'}, inplace=True)
    
    # Top and bottom 10 countries by unique customers
    top_customers = country_customers.nlargest(10, 'Customer_Count')
    bottom_customers = country_customers.nsmallest(10, 'Customer_Count')
    
    # Plot countries with most unique customers
    fig = go.Figure(data=[go.Bar(
        name='Top Countries by Customers',
        x=top_customers['Transmission_Zone'],
        y=top_customers['Customer_Count'],
        marker={'color': top_customers['Customer_Count'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Top 10 Countries by Unique Customers',
        xaxis_title="Countries",
        yaxis_title="Number of Unique Customers",
        plot_bgcolor='white'
    )
    fig.write_html('top_countries_customers.html')
    
    # Plot countries with least unique customers
    fig = go.Figure(data=[go.Bar(
        name='Bottom Countries by Customers',
        x=bottom_customers['Transmission_Zone'],
        y=bottom_customers['Customer_Count'],
        marker={'color': bottom_customers['Customer_Count'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Bottom 10 Countries by Unique Customers',
        xaxis_title="Countries",
        yaxis_title="Number of Unique Customers",
        plot_bgcolor='white'
    )
    fig.write_html('bottom_countries_customers.html')

def analyze_product_performance(df):
    """Analyze product performance metrics"""
    # Group by product descriptions
    product_quantities = df.groupby(['Sensor_Type'], as_index=False)['Signal_Strength'].agg('sum')
    
    # Top and bottom 10 products
    top_products = product_quantities.nlargest(10, 'Signal_Strength')
    bottom_products = product_quantities.nsmallest(10, 'Signal_Strength')
    
    # Plot bestselling products
    fig = go.Figure(data=[go.Bar(
        name='Bestselling Products',
        x=top_products['Sensor_Type'],
        y=top_products['Signal_Strength'],
        marker={'color': top_products['Signal_Strength'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Top 10 Bestselling Products',
        xaxis_title="Products",
        yaxis_title="Total Quantity Sold",
        plot_bgcolor='white'
    )
    fig.write_html('top_products_quantity.html')
    
    # Plot products with most returns
    fig = go.Figure(data=[go.Bar(
        name='Products with Most Returns',
        x=bottom_products['Sensor_Type'],
        y=bottom_products['Signal_Strength'],
        marker={'color': bottom_products['Signal_Strength'], 'colorscale': 'Rainbow'}
    )])
    fig.update_layout(
        title='Top 10 Products with Most Returns',
        xaxis_title="Products",
        yaxis_title="Total Quantity Returned",
        plot_bgcolor='white'
    )
    fig.write_html('bottom_products_quantity.html')

def analyze_cohort_retention(df):
    """Perform cohort analysis for customer retention"""
    # Extract quarter and year
    df['InvoiceQuarter'] = ('Q' + df['InvoiceDate'].dt.quarter.astype(str) + '/' + 
                          df['InvoiceDate'].dt.year.astype(str))
    
    # Create cohort mapping
    quarters_map = dict(zip(df['InvoiceQuarter'].unique(), 
                          range(len(df['InvoiceQuarter'].unique()))))
    df['InvoiceQuarterID'] = df['InvoiceQuarter'].map(quarters_map)
    
    # Create cohort identifiers
    df['CohortQuarterID'] = df.groupby('Receiver_ID')['InvoiceQuarterID'].transform('min')
    df['CohortQuarter'] = df['CohortQuarterID'].map(
        dict(zip(quarters_map.values(), quarters_map.keys())))
    df['CohortIndex'] = df['InvoiceQuarterID'] - df['CohortQuarterID']
    
    # Calculate retention
    cohort_retention = df.groupby(['CohortQuarterID', 'CohortIndex'])['Receiver_ID'].apply(
        pd.Series.nunique).reset_index()
    cohort_retention.rename(columns={'Receiver_ID': 'Customer_Count'}, inplace=True)
    
    # Create pivot table
    cohort_retention_count = cohort_retention.pivot_table(
        index='CohortQuarterID',
        columns='CohortIndex',
        values='Customer_Count'
    )
    
    # Map cohort quarters
    cohort_retention_count['Cohort Quarter'] = cohort_retention_count.index.map(
        dict(zip(quarters_map.values(), quarters_map.keys())))
    cohort_retention_count = cohort_retention_count.set_index('Cohort Quarter')
    
    # Calculate retention rates
    cohort_size = cohort_retention_count.iloc[:, 0]
    retention = cohort_retention_count.divide(cohort_size, axis=0)
    retention = (retention * 100).round(2)
    retention = retention.iloc[::-1]
    
    # Plot cohort retention heatmap
    fig = go.Figure(data=go.Heatmap(
        z=retention,
        y=retention.index,
        colorscale='Greens',
        text=retention,
        texttemplate="%{text}%",
        colorbar_title='Retention Rate, %',
        xgap=3,
        ygap=3
    ))
    fig.update_layout(
        title="Cohort Analysis: Customer Retention Rate",
        xaxis_title="Cohorts",
        yaxis_title="Quarters",
        plot_bgcolor='white'
    )
    fig.write_html('cohort_retention.html')

def analyze_timeline_sales(df):
    """Analyze sales trends over time"""
    # Quarterly sales
    df['InvoiceQuarter'] = ('Q' + df['InvoiceDate'].dt.quarter.astype(str) + '/' + 
                          df['InvoiceDate'].dt.year.astype(str))
    quarterly_sales = df.groupby(['InvoiceQuarter'], as_index=False)['Effective_Throughput'].agg('sum')
    
    # Plot quarterly sales
    fig = go.Figure(data=[go.Bar(
        name='Quarterly Sales',
        x=quarterly_sales['InvoiceQuarter'],
        y=quarterly_sales['Effective_Throughput'],
        marker={'color': quarterly_sales['Effective_Throughput'], 'colorscale': 'Portland'}
    )])
    fig.update_layout(
        title="Quarterly Sales Analysis",
        xaxis_title="Quarters",
        yaxis_title="Total Amount",
        plot_bgcolor='white'
    )
    fig.write_html('quarterly_sales.html')
    
    # Monthly sales
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')
    monthly_sales = df.groupby(['InvoiceMonth'], as_index=False)['Effective_Throughput'].agg('sum')
    
    # Plot monthly sales
    fig = go.Figure(data=[go.Bar(
        name='Monthly Sales',
        x=monthly_sales['InvoiceMonth'].astype(str),
        y=monthly_sales['Effective_Throughput'],
        marker={'color': monthly_sales['Effective_Throughput'], 'colorscale': 'Portland'}
    )])
    fig.update_layout(
        title="Monthly Sales Analysis",
        xaxis_title="Months",
        yaxis_title="Total Amount",
        plot_bgcolor='white'
    )
    fig.write_html('monthly_sales.html')

def main():
    # Load data
    print("Loading data...")
    df = load_and_preprocess_data('online_retail_II_ece.csv')
    
    # Generate analyses
    print("Generating sales trend analysis...")
    analyze_sales_trends(df)
    
    print("Analyzing customer behavior...")
    analyze_customer_behavior(df)
    
    print("Analyzing country performance...")
    analyze_country_performance(df)
    
    print("Analyzing product performance...")
    analyze_product_performance(df)
    
    print("Performing cohort analysis...")
    analyze_cohort_retention(df)
    
    print("Analyzing timeline sales...")
    analyze_timeline_sales(df)
    
    print("Analysis complete! Opening dashboard in your default browser...")
    
    # Open the index page in the default browser
    index_path = os.path.abspath('index.html')
    webbrowser.open('file://' + index_path)

if __name__ == "__main__":
    main() 