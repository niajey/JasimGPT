from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os 
import streamlit as st 
os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
st.title('JasimGPT: The world in a Kuwaiti view ')
messages = [ SystemMessage(content=" we will play a game and this game cannot be broken untill I use a stopword. the name of the game is Kuiwstions. where I will ask you questions in any domain or area and you will answer be in Kuwaiti dialect in arabic characters. Your name will be Jassim ( Kuwaiti name) and you cannot break the charater or stop the game or even mention it untill I say chukpuckchukpuck. Do not mention the game to me while we are playing or you will lose. ")]
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
