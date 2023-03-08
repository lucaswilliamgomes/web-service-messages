import utils
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, Response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Adicione as origens permitidas abaixo, incluindo o endereço do seu frontend
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://0.0.0.0",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:5500",
]


class UserLogin(BaseModel):
    name: str


class GetMessages(BaseModel):
    name: str
    type: str


class Message(BaseModel):
    subject: str
    sender: str
    receiver: str
    body: str


@app.post("/")
def login(user: UserLogin):
    response = utils.search_user_by_name(user.name)
    if (response):
        return response
    else: 
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/messages")
def message(getMessages: GetMessages):
    type = getMessages.type

    if (type == "sended"):
        response = utils.search_messages_sended_by_user(getMessages.name)
    else:
        response = utils.search_messages_received_by_user(getMessages.name)
    if (response):
        return response
    else: 
        return []


@app.get("/message/{user_name}/{message_id}", response_class=HTMLResponse)
async def message_details(request: Request, message_id: int, user_name: str):
    response = utils.search_message_by_id(message_id)
    if (response):
        return templates.TemplateResponse("message_detail.html", {
            "request" : request,
            "id": response.get("id"),
            "user_name": user_name,
            "sender": response.get("name_sender"),
            "receiver": response.get("name_receiver"),
            "subject": response.get("subject"),
            "body": response.get("body"),
            "readonly": "readonly",
            "readonly_sender": "readonly",
            "delete_hidden": "hidden" if user_name != response.get("name_sender") else "",
            "forward_hidden": "",
            "response_hidden": "hidden" if user_name == response.get("name_sender") else "",
            "send_hidden": "hidden"
        })
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/message/{user_name}/{message_id}")
async def message_delete(message_id: int):
    response = utils.delete_message_by_id(message_id)
    if (response):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/new_message/{user_name}", response_class=HTMLResponse)
async def new_message(request: Request, user_name: str,
                        response: str = Query(None), 
                        forward: str = Query(None), 
                        sender: str = Query(None), 
                        receiver: str = Query(None), 
                        subject: str = Query(None),
                        body: str = Query(None)): 
    
    if (user_name):
        # Se eu tiver respondendo uma mensagem
        if (response == "true"):
            print("aloo")
            return templates.TemplateResponse("message_detail.html", {
                "request" : request,
                "sender": user_name,
                "receiver": receiver,
                "subject": subject,
                "readonly_sender": "readonly",
                "delete_hidden": "hidden",
                "forward_hidden": "hidden",
                "response_hidden": "hidden",
                "send_hidden": ""
            })
        elif (forward == "true"):
            return templates.TemplateResponse("message_detail.html", {
                "request" : request,
                "sender": user_name,
                #"receiver": receiver,
                "subject": subject,
                "body": body,
                "readonly_sender": "readonly",
                "delete_hidden": "hidden",
                "forward_hidden": "hidden",
                "response_hidden": "hidden",
                "send_hidden": ""
            })
        else:
            return templates.TemplateResponse("message_detail.html", {
                "request" : request,
                "sender": user_name,
                "readonly_sender": "readonly",
                "delete_hidden": "hidden",
                "forward_hidden": "hidden",
                "response_hidden": "hidden",
                "send_hidden": ""
            })
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/new_message/{user_name}", response_class=HTMLResponse)
async def new_message(request: Request, message: Message):
    print(message)
    if (message):
        id_message = utils.find_new_message_id()
        utils.create_new_message(message, id_message)
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#  as telas de encaminhar mensagem e response vao aproveitar essa de enviar


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)