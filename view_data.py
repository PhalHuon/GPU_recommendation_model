# view_data.py

from gpu_price_tracker.database import Database
import pandas as pd
import json
from sqlalchemy import create_engine
import pymysql

def display_database_info():
    # Create database connection
    db = Database()
    
    # Get all GPUs
    gpus = db.get_all_gpus()
    print(f"Total GPUs in database: {len(gpus)}")
    
    # Count by retailer
    retailers_df = pd.read_sql(
        "SELECT retailer, COUNT(*) as count FROM gpus GROUP BY retailer",
        db.engine
    )
    print("\nGPUs by retailer:")
    print(retailers_df)
    
    # Price statistics by model
    stats_df = pd.read_sql("""
        SELECT brand, model, 
               MIN(price) as min_price, 
               MAX(price) as max_price, 
               AVG(price) as avg_price, 
               COUNT(*) as count
        FROM gpus
        WHERE price IS NOT NULL
        GROUP BY brand, model
        ORDER BY brand, model
    """, db.engine)
    
    print("\nPrice statistics by model:")
    print(stats_df)
    
    # Display the 5 cheapest GPUs
    cheapest_df = pd.read_sql("""
        SELECT name, price, retailer, url
        FROM gpus
        WHERE price IS NOT NULL
        ORDER BY price ASC
        LIMIT 5
    """, db.engine)
    
    print("\nCheapest GPUs:")
    print(cheapest_df)
    
    return {
        "total_gpus": len(gpus),
        "by_retailer": retailers_df,
        "price_stats": stats_df,
        "cheapest": cheapest_df
    }

def export_to_csv():
    # Create database connection
    engine = create_engine("mysql+pymysql://root:password@localhost/gpu_tracker")
    
    # Query all GPUs
    query = "SELECT * FROM gpus"
    df = pd.read_sql(query, engine)
    
    # Export to CSV
    filename = "gpu_prices_export.csv"
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

if __name__ == "__main__":
    print("GPU Price Tracker Data Viewer")
    print("-----------------------------")
    
    try:
        info = display_database_info()
        
        # Ask if user wants to export to CSV
        choice = input("\nDo you want to export the data to CSV? (y/n): ")
        if choice.lower() == 'y':
            export_to_csv()
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure the MySQL database is set up correctly and the spiders have collected data.")
        print("You may need to create the database first:")
        print("CREATE DATABASE gpu_tracker;")