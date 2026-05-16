from datetime import datetime
import os

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI()

# Configuración de CORS para permitir peticiones desde cualquier cliente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================
# Configuración de Base de Datos
# ==========================================

# NOTA: Para despliegue, utilice la variable de entorno MONGO_URI:
#client = MongoClient(os.environ["mongodb://ISIS2304J24202610:XPPziwUGMqG0@157.253.236.88:8087"])

# TODO: Conectarse al cluster Admonsis para desarrollo local
client = MongoClient("mongodb://ISIS2304J24202610:XPPziwUGMqG0@157.253.236.88:8087")

# TODO: Especificar el nombre de la base de datos asignada
# db = client["ISIS*******"]
db = client["ISIS2304J24202610"]

# ==========================================
# Endpoints
# ==========================================

@app.get("/")
def inicio():
    """Endpoint de verificación de estado."""
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    """Retorna la lista de comentarios asociados a un bar."""
    cursor = db.comentarios.find({"bar_id": bar_id})
    
    comentarios = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"]) 
        comentarios.append(doc)
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict = Body(...)):
    """Crea un nuevo comentario para un bar específico."""
    datos['bar_id'] = bar_id
    datos['fecha'] = datetime.now().isoformat()
  
    db.comentarios.insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

# Retornar todos los eventos de un bar desde la colección 'eventos'
@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    cursor = db.eventos.find({"bar_id": bar_id})
    
    eventos = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"]) 
        eventos.append(doc)
    return eventos

# Insertar un evento en la colección 'eventos'
@app.post('/bares/{bar_id}/eventos')
def post_evento(bar_id: int, datos: dict = Body(...)):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    db.eventos.insert_one(datos)
    return {'mensaje': 'Evento guardado'}



