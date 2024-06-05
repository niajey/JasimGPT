from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel , Field
import os  
from langchain_core.tools import Tool , tool
from langchain_core.messages import AIMessage , SystemMessage , HumanMessage
from langchain_core.output_parsers import   StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_react_agent , AgentExecutor , create_structured_chat_agent
from langchain import hub
from Tools import getInternetSearch , getProductsListFromSuperMarkets , getProductPriceBybarcodeWrapperFormLLM , getTivSearchResult
import streamlit as st 
os.environ['OPENAI_API_KEY'] =  st.secrets["OPENAI_API_KEY"]
os.environ['SUPERMARKETS_API_KEY'] =  st.secrets["SUPERMARKETS_API_KEY"]
os.environ['TAVILY_API_KEY']  =  st.secrets["TAVILY_API_KEY"]
os.environ['LANGCHAIN_API_KEY']  =  st.secrets["LANGCHAIN_API_KEY"]
os.environ['LANGCHAIN_TRACING_V2']  = "true"
os.environ['LANGCHAIN_PROJECT']  = "JasimGPT"
chatHistory=[]



class Chatter : 
    def __init__(self) :
        text_template = """ given a person name {person_name} I need you to get me the linkedIn profile Page. your answer should contain URLs only. """
        llm = ChatOpenAI(temperature=0 , model='gpt-4o')
        agent_tools = [  
        Tool(
            name='get product prices from supermarket by bardcode' , 
            description = """ this tool is usefull to get products price from supermarket based on Product barcode. Important arguments to this function must be product barcode such as 6271100990018""",
            func=getProductPriceBybarcodeWrapperFormLLM
        
        ) , Tool(
            name='LinkedIn Search' , 
            description = """ this tool is usefull to search user linkedIn profiles. Important arguments to this function must be of the formt {"name":"person name" , "hits":" number of url hits"}""",
            func=getTivSearchResult      
        )  
            , getProductsListFromSuperMarkets
        ]

        react_prompt = hub.pull('hwchase17/structured-chat-agent')
        react_agent = create_structured_chat_agent(llm = llm , tools=agent_tools , prompt=react_prompt)
        self.agent_executer = AgentExecutor(agent = react_agent , tools = agent_tools , verbose = False , handle_parsing_errors=False ,   maxIterations= 2 ) 

    def  answerQustion(self , question, history) : 
        if history !=None : 
            human = HumanMessage(content =question)
            history.append(human)
            out = self.agent_executer.invoke({'input':question , 'chat_history':history})
            ai = AIMessage(content=out['output'])
            history.append(ai)
        else : 
            out = self.agent_executer.invoke({'input':question })
        return out['output'] , history 
