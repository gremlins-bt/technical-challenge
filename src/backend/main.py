import os
import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(
    title="Order Processing Service",
    description="Backend microservice for DevOps Technical Challenge",
    version="1.0.0"
)

# Configuration from Environment Variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres_secret")
DB_NAME = os.getenv("DB_NAME", "ecommerce_db")

class OrderCreate(BaseModel):
    customer_name: str
    item: str
    amount: float

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    item: str
    amount: float
    status: str
    created_at: Optional[str] = None

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            connect_timeout=3
        )
        return conn
    except Exception as e:
        return None

@app.get("/")
def root():
    return {
        "service": "order-backend",
        "status": "healthy",
        "version": "1.0.0"
    }

# Liveness probe: checks if container process is responsive
@app.get("/healthz")
def healthz():
    return {"status": "alive"}

# Readiness probe: verifies downstream database connectivity
@app.get("/ready")
def ready():
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not ready"
        )
    conn.close()
    return {"status": "ready", "database": "connected"}

@app.get("/api/v1/orders", response_model=List[dict])
def list_orders():
    conn = get_db_connection()
    if conn is None:
        # Fallback dummy list if DB is temporarily disconnected
        return [
            {"id": 1, "customer_name": "Demo Client", "item": "Cloud Server", "amount": 149.99, "status": "COMPLETED"}
        ]
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, customer_name, item, amount, status, created_at::text FROM orders ORDER BY id DESC LIMIT 50;")
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        conn.close()

@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=503, detail="Database unavailable")
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO orders (customer_name, item, amount, status) VALUES (%s, %s, %s, 'PENDING') RETURNING id, customer_name, item, amount, status;",
                (order.customer_name, order.item, order.amount)
            )
            created = cur.fetchone()
            conn.commit()
            return dict(created)
    except Exception as err:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        conn.close()
