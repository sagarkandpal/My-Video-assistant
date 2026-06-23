#actionable items, decision points, questions, and key points

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import os

def get_llm():
    return ChatMistralAI(model="mistral-small-latest", mistral_api_key=os.getenv("MISTRAL_API_KEY"), temperature=0.2)

def build_chain(system_prompt : str):
    llm = get_llm()

    return(RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) |
        ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}")
        ]) | llm | StrOutputParser()
    )

def extract_action_items(transcript: str) -> str:
    system_prompt = "you are an expert meeting analyst. from the meeting transcript,"
    "extract all action items. for each provide:\n"
    "- Task description\n"
    "- Owner (who is responsible)"
    "- Deadline (if mentioned, else write 'not mentioned')"
    "Format as a numbered list. if none found say 'No action items found'"

    chain = build_chain(system_prompt)
    return chain.invoke(transcript)


def extract_decision_points(transcript: str) -> str:
    system_prompt = "you are an expert meeting analyst. from the meeting transcript,"
    "extract all decision points. format as a numbered list."
    "if none found say 'No decision points found'."

    chain = build_chain(system_prompt)
    return chain.invoke(transcript)


def extract_questions(transcript: str) -> str:
    system_prompt = "from the meeting transcript, extract all questions that were raised during the meeting"
    "or topics needing follow-up. format as a numbered list."
    "if none found say 'No questions found'."

    chain = build_chain(system_prompt)
    return chain.invoke(transcript)





