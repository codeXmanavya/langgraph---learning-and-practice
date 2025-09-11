# workflow
# 1. We will take basic batting statistics as input (runs, balls, fours, sixes)
# 2. Calculate three metrics in parallel:
#    - Strike Rate (runs per 100 balls)
#    - Balls Per Boundary (how often the batter hits boundaries)
#    - Boundary Percentage (what % of runs came from boundaries)
# 3. Combine all these stats into a single summary
# 4. Return the complete stats with the summary

from langgraph.graph import StateGraph, START,END
from typing import TypedDict

# state
class cricketState(TypedDict):
    runs:int
    balls:int
    fours:int
    sixs:int

    sr:float
    bpb:float
    boundary_percent:float
    summary:str

# graph
graph = StateGraph(cricketState)

# calculate strike rate
def CalculateSR(state:cricketState)->cricketState:
    runs = state['runs']
    balls = state['balls']
    sr = (runs/balls)*100
    return {'sr':sr}

# calculate Boundary per ball
def CalculateBPB(state:cricketState)-> cricketState:
    balls = state['balls']
    boundarys = state['fours'] + state['sixs']
    bpb = balls/boundarys
    return {'bpb':bpb}

# calculate the boundary percentage
def CalculateBP(state:cricketState)-> cricketState:
    runs = state['runs']
    boundaryRuns = state['fours']*4 + state['sixs']*6
    bp = (boundaryRuns/runs)*100
    return {'boundary_percent':bp}

# summarise all things
def Summary(state:cricketState)-> cricketState:
    sr = state['sr']
    bpb = state['bpb']
    bp = state['boundary_percent']
    summary = f'''strike rate is {sr}, boundary per balls is {bpb} and boundary percentage is {bp}'''
    return {'summary':summary}

# add nodes
graph.add_node("CalculateSR",CalculateSR)
graph.add_node("CalculateBPB",CalculateBPB)
graph.add_node("CalculateBP",CalculateBP)
graph.add_node("summary", Summary)

# add edges
graph.add_edge(START,"CalculateSR")
graph.add_edge(START,"CalculateBPB")
graph.add_edge(START,"CalculateBP")

graph.add_edge("CalculateSR","summary")
graph.add_edge("CalculateBPB","summary")
graph.add_edge("CalculateBP","summary")

graph.add_edge("summary", END)

# compile
workflow = graph.compile()

# execute
initial_state = {
    'runs':100,
    'balls':50,
    'fours':5,
    'sixs':5
}
result = workflow.invoke(initial_state)
print(result)
