# workflow
# 1. take a topic
# 2. generate an outline for the blog post
# 3. then use that outline to write the full blog content
# 4. return complete blog

from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
import os

load_dotenv()

# define llm
gemini_api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")

llm = ChatGoogleGenerativeAI(model=model,api_key=gemini_api_key)

# state
class state(TypedDict):
    topic:str
    outline:str
    blog:str

# graph
graph = StateGraph(state)

# generate the outline based on the topic
def generateOutline(state:state)->state:
    topic = state['topic']
    prompt = f'Generate a outline for a blog on this topic - {topic}'
    result = llm.invoke(prompt).content
    state["outline"] = result
    return state

# generate the blog based on the outline
def writeBlog(state:state)->state:
    topic = state['topic']
    outline = state['outline']
    prompt = f'Write a blog on this {topic} with this outline - {outline}'
    result = llm.invoke(prompt).content
    state["blog"] = result
    return state

# add nodes
graph.add_node("generateOutline", generateOutline)
graph.add_node("writeBlog", writeBlog)

# add edges
graph.add_edge(START,"generateOutline")
graph.add_edge("generateOutline","writeBlog")
graph.add_edge("writeBlog", END)

# compile
workflow = graph.compile()

# execute
result = workflow.invoke({"topic":"Do god exists?"})
print(result['blog'])





