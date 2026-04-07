#!/usr/bin/env python3
import os
import csv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'iteso')

def main():
    print("Connecting to MongoDB...")
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    
    db.passengers.drop()
    print("Cleared existing data")
    
    documents = []
    with open("../data/food_beverage/flight_passengers.csv") as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            doc = {
                "airline": row["airline"],
                "from": row["from_airport"],
                "to": row["to_airport"],
                "day": int(row["day"]),
                "month": int(row["month"]),
                "year": int(row["year"]),
                "gender": row["gender"],
                "reason": row["reason"],
                "stay": row["stay"],
                "transit": row["transit"],
                "connection": row["connection"].lower() == "true",
                "wait": int(row["wait"]) if row["wait"] else None
            }
            documents.append(doc)
    
    print(f"Inserting {len(documents)} documents...")
    result = db.passengers.insert_many(documents)
    print(f"✓ Successfully inserted {len(result.inserted_ids)} documents")
    
    client.close()

if __name__ == "__main__":
    main()
