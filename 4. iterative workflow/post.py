#workflow
# 1. Give the topic
# 2. Generate the post
# 3. Evaluate and give some feedback and score
# 4. Based on Evaluation score 
# -- if score is good then -- end
# -- if  not then geraterate again with improvement and send to evaluation score till it hit the desired score -- in loop

from langgraph.graph import StateGraph, START,END
from typing import TypedDict, Literal, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field
import operator
import os

class postState(TypedDict):
    topic: str
    post: str
    evaluation_feedback:list = Annotated[list[str], operator.add]
    evaluation_score: list = Annotated[list[int], operator.add]
    iteration:int

# LLM
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
LLM = ChatGoogleGenerativeAI(model = model, api_key = api_key)

# graph
graph = StateGraph(postState)


def generatePost(state:postState):
    topic = state['topic']
    prompt = f'Generate a post for LinkedIn on this topic : {topic}'
    post = LLM.invoke(prompt).content
    iteration = 0
    return {'post':post, 'iteration':iteration}

def evaluate(state:postState): # i'll have to use structured model to get output in feedback and score format
    
    # defining structured output model
    class EvaluationSchema(BaseModel):
        feedback:str = Field(description='Detailed feedback for the essay'),
        score:int = Field(description='Score out of 10', ge=0, le=10 )

    structured_llm = LLM.with_structured_output(EvaluationSchema)

    post = state['post']
    prompt = f'Evaluate the post based on relevance, uniqueness and language and assign a score out of 10 : {post}'
    evaluation = structured_llm.invoke(prompt)
    return {'evaluation_feedback':[evaluation.feedback], 'evaluation_score':[evaluation.score]}

def evaluation_condition(state:postState):
    if state["evaluation_score"][-1] >= 9 or state['iteration'] == 3:
        return 'approved'
    else :
        return 'improve'

def improvePost(state:postState):
    evaluation_feedback = state['evaluation_feedback']
    evaluation_score = state["evaluation_score"]
    post = state['post']
    prompt = f'Based on latest feedback and score and keeping all previous feedback and score as a context(if available) respectively. Improve the Post : {post, evaluation_feedback, evaluation_score} '
    improved_post = LLM.invoke(prompt).content
    iteration = state['iteration'] + 1
    return {"post": improved_post, "iteration": iteration}



# add nodes
graph.add_node("generatePost", generatePost)
graph.add_node("evaluate", evaluate)
graph.add_node("improvePost", improvePost)

# add edges
graph.add_edge(START, "generatePost")
graph.add_edge("generatePost","evaluate")
graph.add_conditional_edges('evaluate', evaluation_condition, {'approved': END, 'improve': 'improvePost'}) 
graph.add_edge('improvePost', 'evaluate')


# compile
workflow = graph.compile()

# execute
initial_state = {'topic': 'Future of Artificial Intelligence'}
final_state = workflow.invoke(initial_state)
print(final_state)