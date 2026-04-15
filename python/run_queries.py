import redshift_connector
import boto3

# ============================================
# CONFIG
# ============================================

HOST = "ecommerce-workgroup.068256468930.us-east-1.redshift-serverless.amazonaws.com"
DATABASE = "dev"
PORT = 5439
REGION = "us-east-1"

# ============================================
# CONNECT
# ============================================

print("Connecting to Redshift...")

creds = boto3.Session().get_credentials().get_frozen_credentials()

conn = redshift_connector.connect(
    host=HOST,
    database=DATABASE,
    port=PORT,
    is_serverless=True,
    serverless_acct_id="068256468930",
    serverless_work_group="ecommerce-workgroup",
    iam=True,
    access_key_id=creds.access_key,
    secret_access_key=creds.secret_key,
    session_token=creds.token,
    region=REGION
)

conn.autocommit = True
cursor = conn.cursor()
print("Connected!\n")

# ============================================
# QUERIES
# ============================================

queries = {
    "1. Total Revenue": """
        SELECT SUM(revenue) AS total_revenue
        FROM fact_sales
    """,
    "2. Revenue by Country (Top 10)": """
        SELECT c.country, SUM(f.revenue) AS revenue
        FROM fact_sales f
        JOIN dim_country c ON f.country_id = c.country_id
        GROUP BY c.country
        ORDER BY revenue DESC
        LIMIT 10
    """,
    "3. Top 10 Products by Units Sold": """
        SELECT p.description, SUM(f.quantity) AS total_units_sold
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY p.description
        ORDER BY total_units_sold DESC
        LIMIT 10
    """,
    "4. Top 10 Products by Revenue": """
        SELECT p.description, SUM(f.revenue) AS revenue
        FROM fact_sales f
        JOIN dim_products p ON f.product_id = p.product_id
        GROUP BY p.description
        ORDER BY revenue DESC
        LIMIT 10
    """,
    "5. Monthly Revenue Trend": """
        SELECT d.year, d.month, SUM(f.revenue) AS monthly_revenue
        FROM fact_sales f
        JOIN dim_date d ON f.date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month
    """,
    "6. Top 10 Customers by Spending": """
        SELECT cu.customer_id, SUM(f.revenue) AS total_spent
        FROM fact_sales f
        JOIN dim_customers cu ON f.customer_id = cu.customer_id
        GROUP BY cu.customer_id
        ORDER BY total_spent DESC
        LIMIT 10
    """,
    "7. Average Order Value": """
        SELECT AVG(order_total) AS average_order_value
        FROM (
            SELECT invoice_no, SUM(revenue) AS order_total
            FROM fact_sales
            GROUP BY invoice_no
        ) orders
    """,
    "8. Orders by Country (Top 10)": """
        SELECT c.country, COUNT(DISTINCT f.invoice_no) AS total_orders
        FROM fact_sales f
        JOIN dim_country c ON f.country_id = c.country_id
        GROUP BY c.country
        ORDER BY total_orders DESC
        LIMIT 10
    """,
    "9. Repeat vs One-Time Customers": """
        SELECT
            CASE WHEN order_count = 1 THEN 'One-Time Customer' ELSE 'Repeat Customer' END AS customer_type,
            COUNT(*) AS customer_count
        FROM (
            SELECT customer_id, COUNT(DISTINCT invoice_no) AS order_count
            FROM fact_sales
            GROUP BY customer_id
        ) customer_orders
        GROUP BY customer_type
    """,
    "10. Customer Lifetime Value (Top 10)": """
        SELECT customer_id, COUNT(DISTINCT invoice_no) AS total_orders, SUM(revenue) AS lifetime_value
        FROM fact_sales
        GROUP BY customer_id
        ORDER BY lifetime_value DESC
        LIMIT 10
    """
}

# ============================================
# RUN & PRINT
# ============================================

for title, query in queries.items():
    print(f"{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    cursor.execute(query)
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    print(" | ".join(col_names))
    print("-" * 50)
    for row in rows:
        print(" | ".join(str(round(v, 2)) if hasattr(v, 'is_integer') or hasattr(v, 'as_integer_ratio') else str(v) for v in row))
    print()

cursor.close()
conn.close()
print("Done!")
