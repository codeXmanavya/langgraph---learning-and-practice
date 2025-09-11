#workflow
#---User gives an input---
#---llm will check sentiment of the review---
#---If review is -- Postivive -> --- LLM will reply something like thanks for support
#---if review is -- Negative -> --- LLM will check recheck the review and extract three things from review -- issue type,tone and urgency and then reply


from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel,Field

load_dotenv()


# state
class review_state(TypedDict):
    review:str
    sentiment:str
    analysis:dict
    reply:str

graph = StateGraph(review_state)

# defining structured model
class EvaluationSchema(BaseModel):
    sentiment:str = Field(description='sentiment of the review, give me anwer in one word either "Postivie" or "Negative" ')

api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
llm = ChatGoogleGenerativeAI(model= model, api_key = api_key)

structured_llm = llm.with_structured_output(EvaluationSchema)

# checks sentiment
def check_sentiment(state:review_state):
    review = state['review']
    review_sentiment = structured_llm.invoke(review).sentiment
    return {"sentiment":review_sentiment}

# checks the condition based on the sentiment
def check_sentiment_condition(state:review_state) -> Literal['reply_thanks', 'analyze_review']:
    if state['sentiment'] == "Postive":
        return "reply_thanks"
    else:
        return "analyze_review"

# reply for postive review
def reply_thanks(state:review_state):
    prompt = f'Write a thanks reply for this review: {state['review']}'
    reply = llm.invoke(prompt)
    return {"reply":reply}

# analyze the negative review
def analyze_review(state:review_state):
    analysis_LLM = ChatGoogleGenerativeAI(model=model,api_key= api_key)
    class EvaluationSchema(BaseModel):
        issue_type:str = Field(description="Evaluate the issue type of the review"),
        tone:str = Field(description="Evaluate the tone of the review"),
        urgency:str = Field(description="Evaluate urgency for the review")
    
    structured_analysis_llm = analysis_LLM.with_structured_output(EvaluationSchema)

    prompt = f'Evaluate this negative review based on issue_type,tone and ugency; {state['review']}'
    analysis = structured_analysis_llm.invoke(prompt)
    return {'analysis':analysis}

# reply for negative review
def reply_sorry(state:review_state):
    prompt = f'Based on the analysis of issue type : {state['analysis'].issue_type}, tone: {state['analysis'].tone} and urgency: {state["analysis"].urgency} of this negative {state['review']}. Write a reply for the review'
    reply = llm.invoke(prompt)
    return {"reply":reply}


# add nodes
graph.add_node("check_sentiment", check_sentiment)
graph.add_node("reply_thanks",reply_thanks)
graph.add_node("analyze_review",analyze_review)
graph.add_node("reply_sorry", reply_sorry)

# add graphs
graph.add_edge(START,"check_sentiment")
graph.add_conditional_edges("check_sentiment",check_sentiment_condition)
graph.add_edge("reply_thanks",END)
graph.add_edge("analyze_review","reply_sorry")
graph.add_edge("reply_sorry",END)

# compile
workflow = graph.compile()

# execute
initial_state = {'review':'''The iPhone’s software has been surprisingly buggy lately. I’ve experienced random app crashes, occasional freezes, and inconsistent Bluetooth connections. Even simple tasks like switching between apps sometimes cause noticeable lag. For a premium device, these recurring glitches are frustrating and make the overall experience feel less polished than it should be.'''}

final_state = workflow.invoke(initial_state)
print(final_state['reply'].content)