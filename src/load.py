import sqlite3


def load_sql_query(path):
    with open(path, "r") as file:
        return file.read()


def load(df):
    conn = sqlite3.connect("weather_data.db")
    cursor = conn.cursor()

    try:
        # Create the table
        create_table_query = load_sql_query("./sql/create_table.sql")
        cursor.execute(create_table_query)
        conn.commit()
        print("Table created successfully.")

        # Insert data into the table
        insert_query = load_sql_query("./sql/insert_data.sql")
        print(f"Inserting {len(df)} records into the database...")
        cursor.executemany(insert_query, df.values.tolist())
        conn.commit()
        print(f"Successfully inserted {len(df)} records into the table.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()
        print("Database connection closed.")
