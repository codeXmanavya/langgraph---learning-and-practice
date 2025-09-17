#workflow
# 1. Give the topic
# 2. Generate the tweet
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
    prompt = f'''You are a funny and clever Twitter/X influencer. Write a short, original, and hilarious tweet on the topic: "{state['topic']}".

Rules:
- Do NOT use question-answer format.
- Max 280 characters.
- Use observational humor, irony, sarcasm, or cultural references.
- Think in meme logic, punchlines, or relatable takes.
- Use simple, day to day english on this topic : {topic}'''
    post = LLM.invoke(prompt).content
    iteration = 0
    return {'post':post, 'iteration':iteration}

def evaluate(state:postState): # i'll have to use structured model to get output in feedback and score format
    
    # defining structured output model
    class EvaluationSchema(BaseModel):
        feedback:str = Field(description='Detailed feedback for the tweet'),
        score:int = Field(description='Score out of 10', ge=0, le=10 )

    structured_llm = LLM.with_structured_output(EvaluationSchema)

    post = state['post']
    prompt = f'''You are a ruthless, no-laugh-given Twitter critic. You evaluate tweets based on humor, originality, virality, and tweet format. Evaluate the following tweet:

Tweet: "{post}"

Use the criteria below to evaluate the tweet:

1. Originality – Is this fresh, or have you seen it a hundred times before?  
2. Humor – Did it genuinely make you smile, laugh, or chuckle?  
3. Punchiness – Is it short, sharp, and scroll-stopping?  
4. Virality Potential – Would people retweet or share it?  
5. Format – Is it a well-formed tweet (not a setup-punchline joke, not a Q&A joke, and under 280 characters)?

Auto-reject if:
- It's written in question-answer format (e.g., "Why did..." or "What happens when...")
- It exceeds 280 characters
- It reads like a traditional setup-punchline joke
- Dont end with generic, throwaway, or deflating lines that weaken the humor (e.g., “Masterpieces of the auntie-uncle universe” or vague summaries)

### Respond ONLY in structured format:
- evaluation: "approved" or "needs_improvement"  
- feedback: One paragraph explaining the strengths and weaknesses   
. Assign a score out of 10 : {post}'''
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
    prompt = f'''You punch up tweets for virality and humor based on given feedback.Improve the tweet based on this feedback:
"{evaluation_feedback}"
score : {evaluation_score}

Topic: "{state['topic']}"
Original Tweet:
{post}

Re-write it as a short, viral-worthy tweet. Avoid Q&A style and stay under 280 characters.'''
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
initial_state = {'topic': 'Indian Railway'}
final_state = workflow.invoke(initial_state)
print(final_state['post'])