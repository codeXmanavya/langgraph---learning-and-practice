from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")

llm = ChatGoogleGenerativeAI(model=model,api_key=gemini_api_key)

class state(TypedDict):
    topic:str
    outline:str
    blog:str

graph = StateGraph(state)

def generateOutline(state:state)->state:
    topic = state['topic']
    prompt = f'Generate a outline for a blog on this topic - {topic}'
    result = llm.invoke(prompt).content
    state["outline"] = result
    return state

def writeBlog(state:state)->state:
    topic = state['topic']
    outline = state['outline']
    prompt = f'Write a blog on this {topic} with this outline - {outline}'
    result = llm.invoke(prompt).content
    state["blog"] = result
    return state

graph.add_node("generateOutline", generateOutline)
graph.add_node("writeBlog", writeBlog)

graph.add_edge(START,"generateOutline")
graph.add_edge("generateOutline","writeBlog")
graph.add_edge("writeBlog", END)

workflow = graph.compile()

result = workflow.invoke({"topic":"Do god exists?"})
print(result['outline'])





