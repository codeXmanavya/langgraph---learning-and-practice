# workflow
# 1. We will take the coefficients a, b, c from the input
# 2. Format them into a nice equation string
# 3. Calculate the discriminant (b² - 4ac)
# 4. Then branch based on the result:
#    - If discriminant > 0: calculate two different real roots
#    - If discriminant = 0: calculate one repeated root
#    - If discriminant < 0: return "no real roots" message
# 5. Return the final result with all the state information

from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal

# state
class quad_state(TypedDict):
    a:int
    b:int
    c:int
    equation:str
    discriminant:float
    result:str

# graph
graph = StateGraph(quad_state)

# formating equation based on input
def showEquation(state:quad_state):
    equation = f'{state['a']}x2{state['b']}x{state['c']}'
    return {'equation':equation}

# calculating discriminant
def calculateDiscriminant(state:quad_state):
    discriminant = (state['b']*state['b']) - 4*state['a']*state['c']
    return {'discriminant':discriminant}

# calculating roots
def realRoots(state:quad_state):
    root1 = (-state['b']+(state['b']**2-(4*state['a']*state['c']))*0.5)/2*state['a']
    root2 = (-state['b']-(state['b']**2-(4*state['a']*state['c']))*0.5)/2*state['a']

    result = f'Two real roots are {root1} and {root2}'
    return {"result" : result}

def repeatedRoots(state:quad_state):
    root = (-state['b']+(state['b']**2-(4*state['a']*state['c']))*0.5)/2*state['a']
    result = f'Repeated roots is {root}'
    return {"result" : result}

def noRealRoots(state:quad_state):
    result = f'There are no real roots'
    return {"result" : result}

# check the condition
def checkCondition(state:quad_state) -> Literal['realRoots','repeatedRoots', 'noRealRoots']:
    if state['discriminant'] > 0:
        return "realRoots"
    elif state['discriminant'] == 0:
        return "repeatedRoots"
    else:
        return "noRealRoots"

# add nodes
graph.add_node("showEquation",showEquation)
graph.add_node("calculateDiscriminant", calculateDiscriminant)
graph.add_node("realRoots", realRoots)
graph.add_node("repeatedRoots", repeatedRoots)
graph.add_node("noRealRoots", noRealRoots)


# add edges
graph.add_edge(START, "showEquation")
graph.add_edge("showEquation", "calculateDiscriminant")
graph.add_conditional_edges('calculateDiscriminant', checkCondition)
graph.add_edge("realRoots", END)
graph.add_edge("repeatedRoots", END)
graph.add_edge("noRealRoots", END)

# compile
workflow = graph.compile()

#execute
result = workflow.invoke({"a":4, "b":2,"c":4})
print(result)