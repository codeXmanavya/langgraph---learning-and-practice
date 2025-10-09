from tokenize import Ignore
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

mongo_uri = os.getenv('DB_URI')

client = MongoClient(mongo_uri)

db = client['pydata']

class Summary(BaseModel):
    thread_id: str
    summaries:list[str] 

    class Config:
        extra= "ignore"

api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
Summary_LLM = ChatGoogleGenerativeAI(model= model, api_key= api_key)

async def sumarise_and_update_memory(message,res):
    msg_dict = {
        "userMessage" : message.text,
        "AIMessage": res
    }
    prompt = f''' Summarise this conversation in one very short sentence in a way that you don't leave important detail {msg_dict} '''
    # send to llm to summarise
    summary = Summary_LLM.invoke(prompt).content
    thread_id = message.thread_id
    new_summary = db.summary.update_one({"thread_id":thread_id},{"$push":{"summaries":summary}}, upsert=True)
    return new_summary



def get_summary(message):
    thread_id = message.thread_id
    summary = db.summary.find_one({"thread_id":thread_id})
    if not summary:
        return 'right now, there is no any summary'
    summary_model = Summary(**summary)
    return ' '.join(summary_model.summaries)


