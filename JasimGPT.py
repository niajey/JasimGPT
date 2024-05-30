from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os 
import streamlit as st 
os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
st.title('JasimGPT: The world in a Kuwaiti view ')
messages = [ SystemMessage(content="you an an Arabic speaking personal assitant and AI chatbot. You use Arabic langauge with Kuwaiti Dialect when you converse with a user. all infromatio you provide must be correct and you should provide misleading information")]
parser = StrOutputParser()
llm = ChatOpenAI(model='gpt-4o')
chain = llm | parser
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if text_prompt := st.chat_input("whats on your mind") : 
	messages.append(HumanMessage(content=text_prompt))
	with st.chat_message("user") : 
		st.markdown(text_prompt)
	st.session_state.messages.append({"role": "user", "content": text_prompt})
	result = chain.invoke(messages)
	
	if result : 
		with st.chat_message("ai") : 
			st.markdown(result)
			st.session_state.messages.append({"role": "ai", "content": result})
