from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import firebase_admin
from firebase_admin import credentials, firestore

# firebaseの初期化
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# firestoreの初期化
db = firestore.client()

# web appの定義
app = FastAPI()

# Htmlファイルの場所指定
templates = Jinja2Templates(directory="templates")

# ルートページ
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TODO一覧取得
@app.get("/todos")
def get_todos():
    docs = db.collection("todos").stream()
    return [{"id": d.id, "name": d.to_dict()["name"]}for d in docs]
 
@app.post("/todos")
def add_todo(name: str):
    db.collection("todos").add({"name": name})
    return {"result": "ok"}

@app.put("/todos/{id}")
def update_todo(id: str, name: str):
    db.collection("todos").document(id).update({"name": name})
    return {"result": "ok"}

@app.delete("/todos/{id}")
def delete_todo(id: str):
    db.collection("todos").document(id).delete()
    return {"result": "ok"}
