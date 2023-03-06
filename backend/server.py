import utils
import uvicorn
from fastapi import FastAPI, HTTPException, Request
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
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:5500",
]


class UserLogin(BaseModel):
    name: str


class GetMessages(BaseModel):
    name: str
    type: str


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
            "readonly": "readonly"
        })
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/message/{message_id}")
async def message_delete(message_id: int):
    response = utils.delete_message_by_id(message_id)
    if (response):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# Criar um endPoint get new_message que
# manda o um html com sender já preenchido
# manda uma lista de destinatário já disponivel
# essa tela só vai ter um botão de enviar mensagem depois de preencher
# todos os campos
@app.get("/message/{user_name}/new_message")
async def new_message(user_name: str):
    print(user_name)
    if (user_name):
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Criar um endpois post new_message, que vai receber os dados da mensagem
# e adicionar no json com o próximo id disponivel

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