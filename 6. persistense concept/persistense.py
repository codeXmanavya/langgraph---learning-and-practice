#workflow
# start
# generate joke
# generate explanation of the joke
# end

from langgraph.graph import StateGraph, START,END
from typing import TypedDict
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from langgraph.checkpoint.memory import InMemorySaver

# llm
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
llm = ChatGoogleGenerativeAI(model = model, api_key = api_key)

# state
class jokeState(TypedDict):
    topic:str
    joke:str
    explanation:str

# graph
graph = StateGraph(jokeState)

# functions
def generateJOke(state:jokeState):
    prompt = f'write a joke on the following topic: {state['topic']}'
    response = llm.invoke(prompt).content
    return {'joke':response}

def generateExplanation(state:jokeState):
    prompt = f'explain the following joke you wrote: {state['joke']}, on this topic:{state['topic']}'
    response = llm.invoke(prompt).content
    return {'explanation': response}

# nodes
graph.add_node('generateJoke', generateJOke)
graph.add_node('generateExplanation', generateExplanation)

# edges
graph.add_edge(START, 'generateJoke')
graph.add_edge('generateJoke','generateExplanation')
graph.add_edge("generateExplanation",END)

# checkpointer
checkpointer = InMemorySaver() # defining the checkpointer object

# compile
workflow = graph.compile(checkpointer=checkpointer) # passing checkpointer to save state in memory after every superstep


# execute
config1 = {'configurable':{'thread_id':'1'}} # here thread id will act like an id of this chat
initialState = {'topic': 'Pizza'}
finalState = workflow.invoke(initialState, config= config1) # pass thread id with initial state

print(finalState['joke'])

# get state of thread id 1
getState = workflow.get_state(config1)
print(getState)

# get state history ( while saving on checkpointer ) of thread id 1
getStateHistory = workflow.get_state_history(config1)
print(getStateHistory)



                            ### if we want to create a new chat ###

# then we will define a new thread id : 2
config2 = {'configurable':{'thread_id':'2'}}

# and now we will pass this thread id 
initialState = {'topic': 'pasta'}
finalState = workflow.invoke(initialState, config= config2)
print(finalState['joke'])

# get state of thread id 2
getState = workflow.get_state(config1)
print(getState)

# get state history ( while saving on checkpointer ) of thread id 2
getStateHistory = workflow.get_state_history(config1)
print(getStateHistory)