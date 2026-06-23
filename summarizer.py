from pydoc import text
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

import os

def get_llm():
    return ChatMistralAI(model="mistral-small-latest", mistral_api_key=os.getenv("MISTRAL_API_KEY"), temperature=0.3)

def split_transcript(transcript: str) -> str:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000, 
        chunk_overlap=200
    )

    return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarise this portion of a meeting transcript concisely."),
        ("human", "Summarize the following text:\n\n{text}")
    ])

    map_chain = prompt | llm | StrOutputParser()

    chunks = split_transcript(transcript)

    chunks_summaries = [map_chain.invoke({"text" : chunk}) for chunk in chunks]

    combined = "\n\n".join(chunks_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        ("system", "you are an expert meeting summarizer. Combine these partial summaries into one final professional meeting summary in bullet points."),
        ("human", "Summarize the following text:\n\n{text}")
    ])
    
    combined_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | combined_prompt | llm | StrOutputParser()
    )

    return combined_chain.invoke(combined)


def generate_title(transcript: str) -> str:
    llm = get_llm()

    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) | 
        ChatPromptTemplate.from_messages([
            ("system", "Based on the meeting transcript, generate a short professional meeting title (max 8 words). only return the title nothing else."),
            ("human", "Generate a title for the following text:\n\n{text}")
        ]) 
        | llm | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])