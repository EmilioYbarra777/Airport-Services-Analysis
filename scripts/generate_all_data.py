#!/usr/bin/env python3
"""
Unified data generator for both services.
Generates consistent data in all required formats:
- data.cql for Cassandra (car rental)
- flight_passengers.csv for MongoDB (food & beverage)
"""
import csv
import datetime
import json
import random
from random import choice, randint, randrange

# Output files
CQL_FILE = 'data/car_rental/data.cql'
CSV_FILE = 'data/food_beverage/flight_passengers.csv'

# Shared data
airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris", "United Airlines", "British Airways", "Air France", "Emirates", "Qatar Airways", "Singapore Airlines", "Korean Air", "Japan Airlines", "Turkish Airlines", "LATAM Airlines", "Air Canada", "Copa Airlines"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK", "ORD", "LHR", "CDG", "DXB", "DOH", "SIN", "ICN", "NRT", "IST", "SCL", "YYZ", "PTY"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

def generate_record(flight_id):
    from_airport = choice(airports)
    to_airport = choice(airports)
    while from_airport == to_airport:
        to_airport = choice(airports)
    
    date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
    day = date.day
    month = date.month
    year = date.year
    
    reason = choice(reasons)
    stay = choice(stays)
    connection = choice([True, False])
    wait = randint(30, 720)
    transit = choice(transits)
    airline = choice(airlines)
    gender = choice(genders)
    age = randint(1, 90)
    
    if not connection:
        wait = 0
        transit = ""
    
    if reason == "Back Home":
        stay = "Home"
        connection = False
        wait = 0
    
    return {
        'flightID': flight_id,
        'airline': airline,
        'from_airport': from_airport,
        'to_airport': to_airport,
        'day': day,
        'month': month,
        'year': year,
        'age': age,
        'gender': gender,
        'reason': reason,
        'stay': stay,
        'transit': transit,
        'connection': connection,
        'wait': wait
    }

def generate_all_formats(num_records=10000):
    print(f"Generating {num_records} records for both services...")
    
    # Generate all records once
    records = [generate_record(i + 1) for i in range(num_records)]
    
    # 1. Generate CSV for Food & Beverage
    with open(CSV_FILE, 'w', newline='') as fd:
        fieldnames = ['flightID', 'airline', 'from_airport', 'to_airport', 'day', 'month', 'year', 'age', 'gender', 'reason', 'stay', 'transit', 'connection', 'wait']
        writer = csv.DictWriter(fd, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"✓ Generated {CSV_FILE}")
    
    # 2. Generate CQL for Car Rental (Cassandra)
    acc_stmt = "INSERT INTO airport_flights (origin_airport, destination_airport, year, month, day, airline, reason, stay, transit, connection, wait, age, gender) VALUES ('{}', '{}', {}, {}, {}, '{}', '{}', '{}', '{}', '{}', {}, {}, '{}');"
    pos_stmt = "INSERT INTO airport_flights_transit (origin_airport, destination_airport, year, month, day, airline, reason, stay, transit, connection, wait, age, gender) VALUES ('{}', '{}', {}, {}, {}, '{}', '{}', '{}', '{}', '{}', {}, {}, '{}');"
    
    with open(CQL_FILE, 'w') as fd:
        car_rental_count = 0
        for rec in records:
            # Only include records matching car rental criteria:
            # - Age 21+ (legal requirement for car rental)
            # - Not going back home (need transportation)
            # - Not staying at home (need transportation)
            # - Has a connection (time to rent a car)
            # - Has actual transit method recorded
            if (rec['age'] >= 21 and 
                rec['reason'] != 'Back Home' and 
                rec['stay'] != 'Home' and 
                rec['connection'] == True and
                rec['transit'] not in ['Pickup', 'Own car', '']):
                
                fd.write(acc_stmt.format(
                    rec['from_airport'], rec['to_airport'], rec['year'], rec['month'], rec['day'],
                    rec['airline'], rec['reason'], rec['stay'], rec['transit'],
                    str(rec['connection']).lower(), rec['wait'], rec['age'], rec['gender']
                ))
                fd.write('\n\n')
                
                fd.write(pos_stmt.format(
                    rec['from_airport'], rec['to_airport'], rec['year'], rec['month'], rec['day'],
                    rec['airline'], rec['reason'], rec['stay'], rec['transit'],
                    str(rec['connection']).lower(), rec['wait'], rec['age'], rec['gender']
                ))
                fd.write('\n\n')
                car_rental_count += 1
    
    print(f"✓ Generated {CQL_FILE} ({car_rental_count} records matching car rental criteria)")
    print(f"\n✅ All data files generated with {num_records} records!")

if __name__ == "__main__":
    import sys
    num_records = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    generate_all_formats(num_records)
