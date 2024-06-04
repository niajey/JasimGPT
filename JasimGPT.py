from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
from ChatModules import Chatter 
import os 
import streamlit as st 
st.title(r'JasimGPT: The world in a Kuwaits  view ')
messages = [SystemMessage('you are digital assitant and you response in Arabic with Kuwaiti Dilect your name is Jasim. You only use tools when you have to')]
chatter = Chatter()

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
	result   , messages = chatter.answerQustion(text_prompt ,messages)
	
	if result : 
		with st.chat_message("ai") : 
			st.markdown(result)
			st.session_state.messages.append({"role": "ai", "content": result})
