import redshift_connector
import boto3

# ============================================
# CONFIG
# ============================================

HOST = "ecommerce-workgroup.068256468930.us-east-1.redshift-serverless.amazonaws.com"
DATABASE = "dev"
PORT = 5439
S3_BUCKET = "ecommerce-data-platform-eugenioqs-2026"
S3_PREFIX = "star-schema"
REGION = "us-east-1"
IAM_ROLE = "arn:aws:iam::068256468930:role/service-role/AmazonRedshift-CommandsAccessRole-20260414T200903"

# ============================================
# CONNECT
# ============================================

print("Connecting to Redshift...")

session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()

conn = redshift_connector.connect(
    host=HOST,
    database=DATABASE,
    port=PORT,
    is_serverless=True,
    serverless_acct_id="068256468930",
    serverless_work_group="ecommerce-workgroup",
    iam=True,
    access_key_id=credentials.access_key,
    secret_access_key=credentials.secret_key,
    session_token=credentials.token,
    region=REGION
)

conn.autocommit = True
cursor = conn.cursor()
print("Connected!")

# ============================================
# CREATE TABLES
# ============================================

print("Creating tables...")

statements = [
    "DROP TABLE IF EXISTS fact_sales",
    "DROP TABLE IF EXISTS dim_products",
    "DROP TABLE IF EXISTS dim_customers",
    "DROP TABLE IF EXISTS dim_country",
    "DROP TABLE IF EXISTS dim_date",
    """CREATE TABLE dim_products (
        product_id   INT,
        stockcode    VARCHAR(20),
        description  VARCHAR(255)
    )""",
    """CREATE TABLE dim_customers (
        customer_id  INT
    )""",
    """CREATE TABLE dim_country (
        country_id  INT,
        country     VARCHAR(100)
    )""",
    """CREATE TABLE dim_date (
        date_id   INT,
        date      DATE,
        year      INT,
        month     INT,
        day       INT,
        weekday   VARCHAR(20)
    )""",
    """CREATE TABLE fact_sales (
        invoice_no  VARCHAR(20),
        product_id  INT,
        customer_id INT,
        country_id  INT,
        date_id     INT,
        quantity    INT,
        unit_price  DECIMAL(10, 2),
        revenue     DECIMAL(10, 2)
    )"""
]

for stmt in statements:
    cursor.execute(stmt)

print("Tables created!")

# ============================================
# LOAD DATA FROM S3
# ============================================

tables = {
    "dim_products": "(product_id, stockcode, description)",
    "dim_customers": "(customer_id)",
    "dim_country": "(country_id, country)",
    "dim_date": "(date, date_id, year, month, day, weekday)",
    "fact_sales": "(invoice_no, product_id, customer_id, country_id, date_id, quantity, unit_price, revenue)"
}

for table, columns in tables.items():
    print(f"Loading {table}...")
    s3_path = f"s3://{S3_BUCKET}/{S3_PREFIX}/{table}.csv"
    copy_sql = f"""
        COPY {table} {columns}
        FROM '{s3_path}'
        IAM_ROLE '{IAM_ROLE}'
        FORMAT AS CSV
        IGNOREHEADER 1
        REGION '{REGION}'
    """
    cursor.execute(copy_sql)
    print(f"  {table} loaded!")

print("\nAll tables loaded successfully!")

# ============================================
# VERIFY
# ============================================

print("\nRow counts:")
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count:,} rows")

cursor.close()
conn.close()
print("\nDone!")
