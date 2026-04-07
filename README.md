# Airport Analysis

Multi-database NoSQL project analyzing airport data using Cassandra and MongoDB.

## Prerequisites

- Docker Desktop running
- Python 3.8+

## Complete Setup - Car Rental Service

Follow these steps in order:

### 1. Start Databases
```bash
docker-compose up -d
```

### 2. Generate Data
```bash
python3 scripts/generate_all_data.py 1000  # Windows: python scripts\generate_all_data.py 1000 (can be a different number)
```

### 3. Setup Car Rental Service
```bash
cd car_rental_campaign
python3 -m venv venv  # Windows: python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Initialize Cassandra Schema
```bash
python3 src/schema.py  # Windows: python src\schema.py
```

### 5. Load Data into Cassandra (root level)
```bash
docker cp data/car_rental/data.cql cassandra:/data.cql
docker exec cassandra cqlsh -k flights -f /data.cql
```

### 6. Run Car Rental App
```bash
python3 src/app.py  # Windows: python src\app.py
```

You should see a menu with options to query flight data.

---

## Food & Beverage Service

### 1. Load MongoDB Data
```bash
cd food_beverage_service
python3 -m venv venv  # Windows: python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 src/populate_bulk.py  # Windows: python src\populate_fast.py
```

### 2. Run Service
```bash
uvicorn src.main:app --reload
```

API available at: http://localhost:8000  
Docs: http://localhost:8000/docs

### 3. Query the API

**Get all airport statistics:**
```bash
curl http://localhost:8000/flight/
```

**Filter by specific airport:**
```bash
curl http://localhost:8000/flight/?airport=LAX
```

**Sort results:**
- `sort=1` - By connection flights (default)
- `sort=2` - By ratio (connections/total)
- `sort=3` - By average wait hours

```bash
curl http://localhost:8000/flight/?sort=2
```

**Add a new passenger record:**
```bash
curl -X POST http://localhost:8000/flight/ \
  -H "Content-Type: application/json" \
  -d '{
    "airline": "Delta Airlines",
    "from": "LAX",
    "to": "JFK",
    "day": 15,
    "month": 3,
    "year": 2023,
    "gender": "male",
    "reason": "Business/Work",
    "stay": "Hotel",
    "transit": "Car rental",
    "connection": true,
    "wait": 120
  }'
```

Or use the interactive Swagger UI at http://localhost:8000/docs

---

## Project Structure

```
airport-analysis/
├── car_rental_campaign/     # Cassandra-based service
├── food_beverage_service/   # MongoDB-based service
├── scripts/                 # Setup and data generation
├── data/                    # Generated data files
└── docker-compose.yml       # Database containers
```

## Stopping Services

```bash
docker-compose down         # Stop databases
docker-compose down -v      # Stop and remove all data
```
