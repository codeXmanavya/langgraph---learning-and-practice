from langgraph.graph import StateGraph, START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import os
from langgraph.checkpoint.memory import MemorySaver

#LLM
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
LLM = ChatGoogleGenerativeAI(model= model, api_key= api_key)

# state
class chatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages]

checkpointer = MemorySaver()
graph = StateGraph(chatState)
    
# generate function
def chatNode(state:chatState):
    messages = state["messages"]

    response = LLM.invoke(messages)

    return {"messages":[response]}



# nodes
graph.add_node('chatNode', chatNode)

# edges
graph.add_edge(START, 'chatNode')
graph.add_edge("chatNode", END)

# compile
chatbot = graph.compile(checkpointer=checkpointer)


# execute
# initial_state = {
#     'messages': [HumanMessage(content="what is the capital of India?")]
# }

# final_state = chatbot.invoke(initial_state)

# print(final_state['messages'][-1].content)

thread_id = '1'

while True:
    user_message = input('Type here: ')

    print("You: ",user_message)

    if user_message.strip().lower() in ['exit','quit', 'bye']:
        break

    config = {'configurable':{'thread_id':thread_id}}
    response = chatbot.invoke({
        'messages':[HumanMessage(content=user_message)]
    }, config=config)

    print("AI: ", response['messages'][-1].content )