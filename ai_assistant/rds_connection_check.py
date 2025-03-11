import psycopg2

# AWS RDS PostgreSQL Connection Details
DB_HOST = "afta-ai-agent-db-instance-1.ctyc8muwyysc.ap-southeast-2.rds.amazonaws.com"
DB_PORT = "5432"
DB_USER = "postgres_admin"
DB_PASSWORD = "Super_admin_2025!"

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )

    conn.autocommit = True
    cursor = conn.cursor()
    print("Connected to PostgreSQL RDS")

    # # Example Query
    # cursor.execute("insert into users (username,email,password_hash) values ('Udhaya20', 'udhaya20@yahoo.com', 'Suresh#try20');")
    #
    # # Check if insert was successful
    # if cursor.rowcount > 0:
    #     print("✅ Insert successful! Rows inserted:", cursor.rowcount)
    # else:
    #     print("⚠️ No rows were inserted.")
    #
    # cursor.execute("SELECT * FROM users;")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # # Close Connection
    cursor.close()
    conn.close()

except Exception as e:
    print("Error:", e)
