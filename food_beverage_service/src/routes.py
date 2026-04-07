#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId
import sys

from src.model import Flight, Flight_info

router = APIRouter()

@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight)
def create_flight(request: Request, flight: Flight = Body(...)):
    flight = jsonable_encoder(flight)
    new_flight = request.app.database["passengers"].insert_one(flight)
    created_flight = request.app.database["passengers"].find_one(
        {"_id": new_flight.inserted_id}
    )

    return created_flight


@router.get("/", response_description="Get all flights", response_model=List[Flight_info])
def list_flights(request: Request, wait: int = 0, sort: int = 1, airport: str = ''):


    if sort == 2:
        sort_string = "Ratio"
    elif sort == 3:
        sort_string = "Average Wait Hours"
    else:
        sort_string = "Connection Flights"
        


    if airport:
        

        flights = list(request.app.database["passengers"].aggregate([
        { "$match": { "from": airport } },
            { "$group": {
                "_id": "$from",
                "Total Flights": { "$sum": 1 },
                "Connection Flights": { "$sum": { "$cond": [{ "$eq": ["$connection", True] }, 1, 0] } },
                "AVG_Wait": { "$avg": { "$cond": [{ "$gt": ["$wait", 0] }, "$wait", 0] } }
            } },
            { "$match": { "AVG_Wait": { "$ne": 0 } } },
            { "$project": {
                "_id": 0,
                "Total Flights": 1,
                "Airport": "$_id",
                "Connection Flights": 1,
                "Ratio": { "$round": [{ "$divide": ["$Connection Flights", "$Total Flights"] }, 4] },
                "Average Waiting Hours": { "$round": [{ "$divide": ["$AVG_Wait", 60] }, 2] }
            } }
        ]))




    else:
   
        flights = list(request.app.database["passengers"].aggregate([ { "$group": { "_id": "$from", 
            "Total Flights": { "$sum": 1 }, 
            "Connection Flights": { "$sum": { "$cond": [{ "$eq": ["$connection", True] }, 1, 0] } }, 
            "AVG_Wait": { "$avg": { "$cond": [ { "$gt": ["$wait", 0] }, "$wait", 0] } } } }, 
            { "$match": { "AVG_Wait": { "$ne": 0 } } }, 
            { "$project": { "_id": 0, "Airport": "$_id", "Total Flights": 1, 
            "Connection Flights": 1, "Ratio": { "$round": [{ "$divide": ["$Connection Flights", "$Total Flights"] }, 4] }, 
            "Average Waiting Hours": { "$round": [{ "$divide": ["$AVG_Wait", 60] }, 2] } } }, 
            { "$sort": { sort_string: -1 } }]))
    
            
    return flights
