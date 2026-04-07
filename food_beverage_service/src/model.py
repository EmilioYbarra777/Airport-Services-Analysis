#!/usr/bin/env python3
import uuid
from typing import Optional
from pydantic import BaseModel, Field



class Flight(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_airport: str = Field(...)
    to_airport: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: str = Field(...)
    wait: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "Aeromexico",
                "from_airport": "JFK",
                "to_airport": "LAX",
                "day": 11,
                "month": 3,
                "year": 2021,
                "age": 78,
                "gender": "male",
                "reason": "Business/Work",
                "stay": "Home",
                "transit": "",
                "connection": "True",
                "wait": 287
            }
        }


class Flight_info(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    Airport: str = Field(...)
    Total_Flights: int = Field(alias = "Total Flights")
    Connection_Flights: int = Field(alias = "Connection Flights")
    Ratio: float = Field(...)
    AVG_Conn_Wait_Hours: float = Field(alias = "Average Waiting Hours")
    
 
