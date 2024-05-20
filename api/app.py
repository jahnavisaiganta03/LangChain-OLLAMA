
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms import Ollama
from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"]= 

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"

)
search = SerpAPIWrapper()


modeloa=ChatOpenAI(model = "gpt-3.5-turbo")
modelllama2=Ollama(model="llama2")
modelllama3=Ollama(model="llama3")

prompt1=ChatPromptTemplate.from_template("You are a helpful assistant. Please respond to user queries on {topic} and also provide them the 3 to 4 urls or resources from which you will answer them ")
prompt2=ChatPromptTemplate.from_template("You are a helpful assistant. Please respond to user queries on {topic} and also provide them the 3 to 4 urls or resources from which you will answer them ")
prompt3=ChatPromptTemplate.from_template("You are a helpful assistant. Please respond to user queries on {topic} and also provide them the 3 to 4 urls or resources from which you will answer them ")
add_routes(
    app,
    prompt1|modeloa,
    path="/openai"


)

add_routes(
    app,
    prompt2|modelllama2,
    path="/llama2"


)


add_routes(
    app,
    prompt2|modelllama3,
    path="/llama3"


)


if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)

