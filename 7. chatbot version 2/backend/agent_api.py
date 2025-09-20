from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent import chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # React dev server
    # "https://your-frontend-domain.com" for production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow Authorization header
)

class Message(BaseModel):
    text: str

@app.post('/')
async def chatEndpoint(message: Message):
    CONFIG = {'configurable':{'thread_id':'thread_id'}}
    res = chatbot.invoke({'messages':[HumanMessage(content=message.text)]}, config=CONFIG)
    return {'response':res['messages'][-1].content}