import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np
import re
import csv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_db_connection():
    """Create a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'postgres'),
        user=os.getenv('DB_USER'),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
    )

def create_tables(conn):
    """Create necessary tables if they don't exist."""
    with conn.cursor() as cur:
        # Create the vector extension if it doesn't exist
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Create the diary entries table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS diary (
                id SERIAL PRIMARY KEY,
                date TEXT,
                entry TEXT,
                embedding vector(1536)
            );
        """)
    conn.commit()

def generate_embedding(text):
    print('generating embedding')
    """Generate embedding for the given text using OpenAI's API."""
    if not text or pd.isna(text):
        print("Warning: No entry text - skipping entry")
        return None
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {str(e)}")
        print(f"Text that failed: {text[:200]}...")  # Print first 200 chars of the text
        return None

def process_csv_and_store():
    """Process the CSV file and store data in the database."""
    print("Starting to process CSV file...")
    data_rows = []
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'diary.csv')
    print(f"Reading CSV from: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Create CSV reader
        csv_reader = csv.reader(csvfile, quotechar='"', delimiter=',')
        
        # Skip the header row
        next(csv_reader)
        
        # Process each row
        for row in csv_reader:
            if len(row) == 2:
                date = row[0]
                entry = row[1]
                
                data_rows.append({
                    'date': date,
                    'entry': entry,
                })

    print(f"Found {len(data_rows)} entries in CSV")
    # Create DataFrame from parsed data
    df = pd.DataFrame(data_rows)
    
    # Connect to the database
    print("Connecting to database...")
    conn = get_db_connection()
    
    try:
        # Create tables
        print("Creating tables...")
        create_tables(conn)
        
        # Process each row
        print("Processing rows and generating embeddings...")
        with conn.cursor() as cur:
            for idx, row in df.iterrows():
                print(f"\nProcessing row {idx + 1}:")
                print(f"Date extracted: {row['date']}")
                print(f"Entry to embed: {row['entry'][:50]}...")
                
                # Generate embedding for the description
                embedding = generate_embedding(row['entry'])
                if embedding is None:
                    print("Warning: Could not generate embedding")
                    continue
                
                print("Embedding generated successfully")
                
                # Insert the data
                cur.execute("""
                    INSERT INTO diary (date, entry, embedding)
                    VALUES (%s, %s, %s)
                """, (
                    row['date'],
                    row['entry'],
                    embedding
                ))
                
                # Print progress message
                preview = row['entry'][:100] + "..." if len(row['entry']) > 100 else row['entry']
                print(f"Successfully stored embedding for '{row['date']}': {preview}")
        
        conn.commit()
        print("\nSuccessfully processed and stored all blog entries.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    process_csv_and_store() 
