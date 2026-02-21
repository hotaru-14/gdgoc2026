from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel

# firebaseの初期化
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)

# firestoreの初期化
db = firestore.client()

# web appの定義
app = FastAPI()

# Htmlファイルの場所指定
templates = Jinja2Templates(directory="templates")

class Todo(BaseModel):
    name: str

# ルートページ
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# TODO一覧取得
@app.get("/todos")
def get_todos():
    docs = db.collection("todos").stream()
    todos_list = [{"id": d.id, "name": d.to_dict()["name"]}for d in docs]
    return {"todos": todos_list}
 
@app.post("/todos") #クエリパラメータ
def add_todo(todo: Todo):
    updated_time, doc_ref = db.collection("todos").add({"name": todo.name})
    return {
        "result": "ok",
        "todo": {
            "id": doc_ref.id,
            "name": todo.name,
        }
    }

@app.put("/todos/{id}") #パスパラメータ
def update_todo(id: str, todo: Todo):
    db.collection("todos").document(id).update({"name": todo.name})
    return {"result": "ok", "id": id}

@app.delete("/todos/{id}")
def delete_todo(id: str):
    db.collection("todos").document(id).delete()
    return {"result": "ok", "id": id}