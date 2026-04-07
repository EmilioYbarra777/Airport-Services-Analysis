#!/usr/bin/env python3
import logging
import os
from dotenv import load_dotenv
from cassandra.cluster import Cluster

load_dotenv()

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'flights')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_AIRPORT_FLIGHTS = """
    CREATE TABLE IF NOT EXISTS airport_flights(
        origin_airport TEXT,
        destination_airport TEXT,
        year INT,
        month INT,
        day INT,
        airline TEXT,
        reason TEXT,
        stay TEXT,
        transit TEXT,
        connection TEXT,
        wait INT,
        age INT,
        gender TEXT,
        PRIMARY KEY((destination_airport), month, transit, airline, year, day )
    )
"""

CREATE_AIRPORT_FLIGHTS_TRANSIT = """
    CREATE TABLE IF NOT EXISTS airport_flights_transit(
        origin_airport TEXT,
        destination_airport TEXT,
        year INT,
        month INT,
        day INT,
        airline TEXT,
        reason TEXT,
        stay TEXT,
        transit TEXT,
        connection TEXT,
        wait INT,
        age INT,
        gender TEXT,
        PRIMARY KEY((destination_airport), transit, month, airline, year, day )
    )
"""


def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_AIRPORT_FLIGHTS)
    session.execute(CREATE_AIRPORT_FLIGHTS_TRANSIT)


if __name__ == '__main__':
    log.info("Connecting to Cassandra Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()
    
    create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)
    create_schema(session)
    
    log.info(f"Keyspace '{KEYSPACE}' and tables created successfully")
    cluster.shutdown()
