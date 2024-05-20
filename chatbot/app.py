from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import load_tools,Tool,AgentExecutor
from langchain.agents import initialize_agent
from langchain_community.utilities import SerpAPIWrapper

from langchain.prompts import PromptTemplate

import streamlit as st 
import os
from dotenv import load_dotenv

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# Langsmith Tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["SERPAPI_API_KEY"]= "e1c3a53b813485490ef4daea3b35406de134e328b2db2ce511c53cad83e7bb38"
 
## Prompt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to user queries and also provide them the 3 to 4 urls or resources from which you will answer them . Generate as much as many words they want if given excluding the urls or sources "),
        ("user","Question:{question}")
    ]
)



## streamlit framework

st.title('Langchain Demo with OPENAI')
input_text = st.text_input("Question or Topic of interest:")



search = SerpAPIWrapper()



llm = ChatOpenAI(model = "gpt-3.5-turbo")



ouput_parser = StrOutputParser()

chain = prompt|llm|ouput_parser



if input_text:
    st.write(chain.invoke({'question':search.run(input_text)}))


