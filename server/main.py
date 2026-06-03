# backend/main.py
import sqlite3
import hashlib
import secrets
import uvicorn 
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DB_FILE = "expenses.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                salt TEXT NOT NULL,
                session_token TEXT UNIQUE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()

init_db()

app = FastAPI(title="Futuristic Offline Core API", version="4.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    enc_payload = (password + salt).encode('utf-8')
    hashed = hashlib.sha256(enc_payload).hexdigest()
    return hashed, salt

def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    target_hash, _ = hash_password(plain_password, salt)
    return secrets.compare_digest(target_hash, hashed_password)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    category: str
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    description: Optional[str] = None
    created_at: str

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token session",
        headers={"WWW-Authenticate": "Bearer"},
    )
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users WHERE session_token = ?", (token,))
        user = cursor.fetchone()
    if user is None:
        raise unauthorized_exception
    return dict(user)

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    hashed_pwd, salt = hash_password(user.password)
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", (user.username, hashed_pwd, salt))
            conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username unavailable")
    return {"message": "Success"}

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
        user = cursor.fetchone()
    if not user or not verify_password(form_data.password, user["hashed_password"], user["salt"]):
        raise HTTPException(status_code=400, detail="Bad credentials")
    session_token = secrets.token_urlsafe(32)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET session_token = ? WHERE id = ?", (session_token, user["id"]))
        conn.commit()
    return {"access_token": session_token, "token_type": "bearer"}

@app.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, title, amount, category, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (current_user["id"], expense.title, expense.amount, expense.category, expense.description, timestamp)
        )
        conn.commit()
        expense_id = cursor.lastrowid
    return {**expense.model_dump(), "id": expense_id, "created_at": timestamp}

@app.get("/expenses", response_model=List[ExpenseResponse])
def read_expenses(current_user: Dict[str, Any] = Depends(get_current_user)):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, amount, category, description, created_at FROM expenses WHERE user_id = ? ORDER BY created_at DESC", (current_user["id"],))
        rows = cursor.fetchall()
    return [dict(row) for row in rows]

# --- OFFLINE ALGORITHMIC DATA EXPLANATION ENGINE ---
@app.get("/expenses/analytics")
def get_analytics(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    u_id = int(current_user["id"])
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM expenses WHERE user_id = ? ORDER BY created_at ASC", (u_id,))
        expenses = [dict(r) for r in cursor.fetchall()]
        
    if not expenses:
        return {
            "total": 0, "breakdown": {}, "highest_category": "None",
            "timeframes": {"minute": [], "hour": [], "day": [], "month": [], "year": []},
            "explanation": "No data pipelines initialized. Submit expenses to spin up AI mapping."
        }

    total = sum(e["amount"] for e in expenses)
    
    # Process Category Distributions
    breakdown = {}
    for e in expenses:
        breakdown[e["category"]] = breakdown.get(e["category"], 0.0) + e["amount"]
    highest_cat = max(breakdown, key=breakdown.get) if breakdown else "None"

    # Multi-Timeframe Structural Bucketing
    tf_maps = {"minute": "%Y-%m-%d %H:%M", "hour": "%Y-%m-%d %H:00", "day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}
    timeframes_data = {}
    
    for tf_key, tf_format in tf_maps.items():
        bucket = {}
        for e in expenses:
            dt_obj = datetime.strptime(e["created_at"], "%Y-%m-%d %H:%M:%S")
            time_str = dt_obj.strftime(tf_format)
            bucket[time_str] = bucket.get(time_str, 0.0) + e["amount"]
        timeframes_data[tf_key] = [{"date": k, "amount": round(v, 2)} for k, v in sorted(bucket.items())]

    # Deterministic Local Analysis Logic (Offline Explainer)
    highest_single = max(expenses, key=lambda x: x["amount"])
    avg_transaction = total / len(expenses)
    
    explanation = (
        f"🌌 FINANCIAL TERMINAL ANALYTICAL LOG\n\n"
        f"• System has mapped total capital outflow of ${total:,.2f} spread across {len(expenses)} individual transaction indices.\n"
        f"• Primary resource drain vector identified as '{highest_cat}', totaling ${breakdown.get(highest_cat, 0):,.2f}.\n"
        f"• Outflow anomaly vector detected on transaction '{highest_single['title']}' peaking single-point strain at ${highest_single['amount']:,.2f}.\n"
        f"• Pipeline transactional density is currently resolving an mean transaction load of ${avg_transaction:,.2f}.\n"
    )
    if len(expenses) >= 2:
        explanation += f"• Longitudinal timeline velocity tracks standard activity span between system index marker {expenses[0]['created_at']} and final transaction timestamp {expenses[-1]['created_at']}."
    else:
        explanation += "• Constructing baseline trend lines. Feed additional transaction logs to calculate burn rates."

    return {
        "total": round(total, 2),
        "breakdown": {k: round(v, 2) for k, v in breakdown.items()},
        "highest_category": highest_cat,
        "timeframes": timeframes_data,
        "explanation": explanation
    }

# Start server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)