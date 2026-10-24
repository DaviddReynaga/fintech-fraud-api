from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Motor antifraude")

# 1. Configurar la base de datos (crea el archivo y la tabla si no existen)
def setup_database():
    conn = sqlite3.connect("fraude.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id TEXT,
            amount REAL,
            merchant TEXT,
            location TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Ejecutamos la configuración al arrancar
setup_database()

class Transaction(BaseModel):
    account_id: str
    amount: float
    merchant: str
    location: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "API de Detección conectada a SQLite"}

@app.post("/validate")
def validate_transaction(transaction: Transaction):
    conn = sqlite3.connect("fraude.db")
    cursor = conn.cursor()
    
    # 2. Consultar historial en SQL (Velocity Check)
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE account_id = ?", (transaction.account_id,))
    intentos_previos = cursor.fetchone()[0] # Extraemos el número del resultado
    
    status = "APPROVED"
    reason = "Transacción legítima"

    # 3. Evaluamos las reglas
    if intentos_previos >= 3:
        status = "BLOCKED"
        reason = "Alerta de Velocity: Demasiadas transacciones en la base de datos"
    elif transaction.amount >= 5000:
        status = "REJECTED"
        reason = "El monto supera el límite automático"
    elif transaction.location.lower() in ["rusia", "corea del norte"]:
        status = "BLOCKED"
        reason = "Ubicación geográfica de alto riesgo"

    # 4. Guardamos el intento en la base de datos de forma permanente
    cursor.execute('''
        INSERT INTO transactions (account_id, amount, merchant, location, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (transaction.account_id, transaction.amount, transaction.merchant, transaction.location, status))
    
    conn.commit()
    conn.close()

    return {
        "status": status,
        "reason": reason,
        "intentos_historicos": intentos_previos + 1
    }