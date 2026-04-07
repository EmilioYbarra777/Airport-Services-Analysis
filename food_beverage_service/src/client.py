#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json



# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")





def print_flight(flight):
    for k in flight.keys():
        if not(k == "_id"):
            print(f"{k}: {flight[k]}")
    print("="*50)



def list_flights(wait,sort,airport):
    suffix = "/flight"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "wait": wait,
        "sort":sort,
        "airport":airport
       
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()

        print("\n")
        
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")




def main():
    log.info(f"Welcome to fligts catalog. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search", "get", "update", "delete"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the books library")

   
    parser.add_argument("--wait",
            help ="Minimum wait time", default = None )
    
    parser.add_argument("--sort",
            help ="Sort documents. 1: Connection Flights, 2: Ratio (connection flights/total flights), 3: Average wait time", default = None )
    
    parser.add_argument("--airport",
            help ="Retrieve info from x airport", default = None )

    args = parser.parse_args()



    if (args.wait or args.sort or args.airport) and args.action != "search":
        log.error("args can only be used with search action")
        exit(1)

 
   
    if args.action == "search":
        list_flights(args.wait,args.sort, args.airport)

   

if __name__ == "__main__":
    main()