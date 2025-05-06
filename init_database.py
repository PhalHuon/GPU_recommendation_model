# init_database.py

import mysql.connector
from mysql.connector import errorcode

def create_database():
    try:
        # Connect to MySQL server
        cnx = mysql.connector.connect(
            user='root',
            password='password',
            host='localhost'
        )
        cursor = cnx.cursor()
        
        # Create database
        print("Creating database gpu_tracker...")
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS gpu_tracker DEFAULT CHARACTER SET 'utf8'"
        )
        print("Database created successfully.")
        
        # Use the database
        cursor.execute("USE gpu_tracker")
        
        # Create table
        print("Creating table gpus...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gpus (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand VARCHAR(50),
                model VARCHAR(50),
                name VARCHAR(255),
                manufacturer VARCHAR(100),
                price FLOAT,
                currency VARCHAR(10),
                original_price FLOAT,
                retailer VARCHAR(50),
                url VARCHAR(1000),
                availability VARCHAR(100),
                shipping_cost VARCHAR(100),
                rating FLOAT,
                num_reviews INT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                specifications TEXT
            ) ENGINE=InnoDB
        """)
        print("Table created successfully.")
        
        # Close connection
        cursor.close()
        cnx.close()
        
        print("Database initialization completed successfully.")
        return True
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your MySQL username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist.")
        else:
            print(f"Error: {err}")
        return False

if __name__ == "__main__":
    create_database()