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

# htmlファイルの場所指定
templates = Jinja2Templates(directory="templates")

# ルートページ
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# todo取得
@app.get("/todos")
def get_todos():
    docs = db.collection("todos").stream()
    return [{"id": d.id, "name": d.to_dict()["name"]} for d in docs]

