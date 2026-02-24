#!/usr/bin/env python3
import logging
import os
import random

from dotenv import load_dotenv
from cassandra.cluster import Cluster

import model

load_dotenv()

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('app.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost') #172.18.0.2
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'flights')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    print("Data has already been filtered\n")
    mm_options = {
        1: "Show all flights by airport",
        2: "Show all flights by airport and month",
        3: "Show recommended month/s for car rental service by airport",
        4: "Show airport flights by month and transit",
        5: "Exit",
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])





def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)


    while(True):
        print_menu()
        option = int(input('Enter your choice: '))

        if option == 1:
            model.get_airport_total_flights(session)

        if option == 2:
            model.get_airport_flights_by_month(session)

        if option == 3:
            model.get_car_rental_by_airport(session)
 
        if option == 4:
            airport = input("\nAirport code (XXX): ")
            model.get_airport_flights_by_month_transit(session, airport)

        
        if option == 5:
            exit(0)


if __name__ == '__main__':
    main()
