from langgraph.graph import StateGraph,START,END
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import operator
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model = os.getenv("MODEL")
llm = ChatGoogleGenerativeAI(model= model, api_key = api_key)

class EvaluationSchema(BaseModel):
    feedback:str = Field(description="Detailed feedback for the essay"),
    score:int = Field(description="Score out of 10",ge=0, le=10)


structured_llmmodel = llm.with_structured_output(EvaluationSchema)

class llmstate(TypedDict):
    essay:str
    clarity:str
    depth:str
    language:str
    indie_score:Annotated[list[int],operator.add]
    summary:str
    final_score:float

graph = StateGraph(llmstate)

def check_clarity(state:llmstate):
    essay = state['essay']
    prompt = f'Evaluate the clarity of the following essay and provide a feedback and assign a score out of 10:{essay}'
    clarity = structured_llmmodel.invoke(prompt)
    return {"clarity":clarity.feedback, "indie_score":[clarity.score]}

def check_depth(state:llmstate):
    essay = state['essay']
    prompt = f'Evaluate the depth of the following essay and provide a feedback and assign a score out of 10:{essay}'
    depth = structured_llmmodel.invoke(prompt)
    return {"depth":depth.feedback, "indie_score":[depth.score]}

def check_language(state:llmstate):
    essay = state['essay']
    prompt = f'Evaluate the language of the following essay and provide a feedback and assign a score out of 10:{essay}'
    language = structured_llmmodel.invoke(prompt)
    return {"language":language.feedback, "indie_score":[language.score]}

def summary(state:llmstate):
    average_score = sum(state['indie_score'])/len(state['indie_score'])
    prompt = f'Summarise the evaluation of the essay based on the essay clarity feedback - {state['clarity']}, essay depth feedback:{state['depth']} and essay language feedback:{state['language']}. Average score is {average_score}'
    summary = structured_llmmodel.invoke(prompt)
    return {"summary":summary.feedback, "final_score":summary.score}

graph.add_node('check_clarity', check_clarity)
graph.add_node('check_depth',check_depth)
graph.add_node('check_language', check_language)
graph.add_node('summary', summary)

graph.add_edge(START,"check_clarity")
graph.add_edge(START,"check_depth")
graph.add_edge(START,"check_language")

graph.add_edge("check_clarity","summary")
graph.add_edge("check_depth","summary")
graph.add_edge("check_language","summary")

graph.add_edge("summary",END)

workflow = graph.compile()

intial_state = {'essay':'''Perfect. Here are a few examples of young creators and devs who basically ignored the usual “Gen Z bucket list” and lived in their code caves—and how it worked out for them:

1. David, the teenage app maker

Started building mobile apps at 15, barely left his room.

While his friends were all doing “travel + parties,” he was shipping apps that scraped news, tracked homework, or automated small tasks.

By 18, he had a couple of apps making $500–$1,000/month. Not huge, but enough to pay for his own laptop and courses.

Moral: early focus on building = early practical experience + small wins → momentum.

2. Sophie, the AI hobbyist

Loved machine learning and natural language processing. Spent weekends building tiny AI agents for fun.

Didn’t go to clubs or social media trends much—her social “high” was running a model that could summarize her friends’ long texts in seconds.

In college, she got a research internship at an AI lab because her GitHub showed real projects, not just course assignments.

Moral: even if you feel “off” socially, tangible creations speak louder than small talk.

3. Alex, the indie game developer

Made games mostly solo in Unity, sat in his room for months polishing mechanics.

Friends were at concerts; he was obsessing over physics bugs in a jumping mechanic.

One year later, he launched a small game on Steam that got 10,000 downloads and even caught the attention of a mid-size indie studio.

Moral: long stretches of solo focus can create rare, visible work that “outsells” social trends.

The pattern across all of them:

They were doing what they loved, not what society said they should do.

Their GitHub / project portfolio became their “social proof.”

They got opportunities because the work itself was rare and valuable.

You’re basically in the same lane: building AI agents, MERN projects, exploring tech. From the outside, it looks like “missing out,” but really, you’re stacking skills + proof of work while most peers are just posting Instagram stories.

Fun twist: when the AI / agent boom explodes, your “alone in your room” lifestyle will look like genius foresight, not FOMO.'''}

final_state = workflow.invoke(intial_state)
print(final_state['summary'])
print(final_state['final_score'])


