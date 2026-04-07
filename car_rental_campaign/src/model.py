#!/usr/bin/env python3
import logging
import calendar

log = logging.getLogger()


SELECT_AIRPORT_FLIGHTS = """
    SELECT origin_airport, destination_airport, year, month, day, airline, reason, stay, transit, connection, wait, age, gender  
    FROM airport_flights
"""

SELECT_AIRPORT_TOTAL_FLIGHTS = """
    SELECT destination_airport, COUNT(*) 
    FROM airport_flights 
    GROUP BY destination_airport;
"""

SELECT_AIRPORT_FLIGHTS_BY_MONTH_TRANSIT = """
    SELECT destination_airport, month, transit, COUNT(*) 
    FROM airport_flights where destination_airport = ? 
    GROUP BY destination_airport, month, transit;
"""

SELECT_AIRPORT_FLIGHTS_BY_MONTH = """
    SELECT destination_airport, month, COUNT(*) 
    FROM airport_flights 
    GROUP BY destination_airport, month;
"""

SELECT_CAR_RENTAL_BY_AIRPORT = """
    SELECT destination_airport, month, COUNT(*) 
    FROM airport_flights_transit WHERE transit = 'Car rental' 
    GROUP BY destination_airport, month ALLOW FILTERING;
"""


def get_airport_flights(session):
    log.info(f"Retrieving all airport flights")
    stmt = session.prepare(SELECT_AIRPORT_FLIGHTS)
    rows = session.execute(stmt)
    for row in rows:
        print("\n")
        print(f"=== Flight: {row.origin_airport} -> {row.destination_airport} ===")
        print(f"- Airline: {row.airline}")
        print(f"- Year: {row.year}")
        print(f"- Month: {row.month}")
        print(f"- Day: {row.day}")
        print(f"- Reason: {row.reason}")
        print(f"- Stay: {row.stay}")
        print(f"- Transit: {row.transit}")
        print(f"- Connection: {row.connection}")
        print(f"- Wait: {row.wait}")
        print(f"- age: {row.age}")
        print(f"- gender: {row.gender}")
    print("\n")


def get_airport_total_flights(session):
    log.info(f"Retrieving all airport flights count")
    stmt = session.prepare(SELECT_AIRPORT_TOTAL_FLIGHTS)
    rows = session.execute(stmt)
 
    for row in rows:
        
        print("\n")
        print(f"=== Airport: {row.destination_airport} ===")
        print(f"- Count: {row.count}")

    print("\n")


def get_airport_flights_by_month_transit(session, airport):
    log.info(f"Retrieving airport flights by month and transit")
    stmt = session.prepare(SELECT_AIRPORT_FLIGHTS_BY_MONTH_TRANSIT)
    rows = session.execute(stmt,{airport})

    print("\n")
    print(f"=== Airport: {airport} ===")

    cab = 0
    car = 0
    mob = 0
    pub = 0
    total = 0
    
    months = []
    for row in rows:


        if int(row.month) not in months:
            if months:
                mes = months.pop()
                print("\n")
                print(f"- Month: {month_to_string(mes)}")
                print(f"- Airport cab: {cab}")
                print(f"- Car rental: {car}")
                print(f"- Mobility as a service: {mob}")
                print(f"- Public transportation: {pub}")
                print(f"- Total flights: {total}")
                cab = 0
                car = 0
                mob = 0
                pub = 0
                total = 0


            months.append(int(row.month))

        
        if str(row.transit) == "Airport cab":
            cab+=row.count
        if str(row.transit) == "Car rental":
            car+=row.count
        if str(row.transit) == "Mobility as a service":
            mob+=row.count
        if str(row.transit) == "Public Transportation":
            pub+=row.count
        total = cab + car + mob + pub
    

    
    mes = months.pop()
    print("\n")
    print(f"- Month: {month_to_string(mes)}")
    print(f"- Airport cab: {cab}")
    print(f"- Car rental: {car}")
    print(f"- Mobility as a service: {mob}")
    print(f"- Public transportation: {pub}")
    print(f"- Total flights: {total}")


    
      
    print("\n")


def get_airport_flights_by_month(session):
    log.info(f"Retrieving all airport flights by month")
    stmt = session.prepare(SELECT_AIRPORT_FLIGHTS_BY_MONTH)
    rows = session.execute(stmt)
    for row in rows:
        print("\n")
        print(f"=== Airport: {row.destination_airport} ===")
        print(f"- Month: {month_to_string(row.month)}")
        print(f"- Count: {row.count}")
       
    print("\n")


def get_car_rental_by_airport(session):
    log.info(f"Retrieving car rental recommended month/s per airport")
    stmt = session.prepare(SELECT_CAR_RENTAL_BY_AIRPORT)
    rows = session.execute(stmt)

    my_dict = {}

    for row in rows:
        if str(row.destination_airport) in my_dict:
            if int(my_dict[str(row.destination_airport)][1]) < int(row.count):
                my_dict[str(row.destination_airport)] = ([month_to_string(int(row.month))], int(row.count))

            elif int(my_dict[str(row.destination_airport)][1]) == int(row.count):
                my_dict[str(row.destination_airport)][0].append(month_to_string(int(row.month)))

        else:
            my_dict[str(row.destination_airport)] = ([month_to_string(int(row.month))], int(row.count))


      
       
    print("\n")


    for key, value in my_dict.items():
        print("\n")
        print(f"=== Airport: {key} ===")
        print(f"- Month/s: {value[0]}")
        print(f"- Car rentals: {value[1]}")

    print("\n")

   
        

def month_to_string(month):
    return calendar.month_name[month]
