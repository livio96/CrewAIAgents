from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
#from langchain_groq import ChatGroq
import streamlit as st
import logging
from datetime import datetime
#from flask import Flask, render_template, request, jsonify
#from flask_socketio import SocketIO, emit
from crewai import Agent, Task, Crew
import os
#from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool

# Set up logging
#logging.basicConfig(filename='chat_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to update chat history in session state
def update_chat_history(user_input, response):
    st.session_state.chat_history.append({"user": user_input, "bot": response})

# Function to generate context from chat history
def generate_context(history):
    context = ""
    for entry in history:
        if 'user' in entry:
            context += f"User: {entry['user']}\n"
        if 'bot' in entry:
            context += f"Bot: {entry['bot']}\n"
    return context



# Define the agents and tasks
support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful support representative in your team, remember user interactions, A relevant and accurate response based on user queries",
    backstory=(
        "You work at TelQuest International (https://www.telquestintl.com) and "
        "are now working on providing support to all telquest international customers."
        "You need to make sure that you provide the best support!"
        "Make sure to provide full complete answers, and make no assumptions."
    ),
    allow_delegation=False,
    memory=True,
    verbose=True
)

support_quality_assurance_agent = Agent(
    role="Support Quality Assurance Specialist",
    goal="Get recognition for providing the best support quality assurance in your team",
    backstory=(
        "You work at TelQuest International (https://telquestintl.com) and "
        "are now working with your team on a request from telquest customers ensuring that "
        "the support representative is providing the best support possible."
        "You need to make sure that the support representative is providing full"
        "complete answers, and make no assumptions."
    ),
    verbose=True
)

docs_scrape_tool = ScrapeWebsiteTool(website_url="https://www.telquestintl.com/search")

inquiry_resolution = Task(
    description=(
        "A customer just reached out with a super important ask:\n"
        "{inquiry}\n\n"
        "First remember the name of the customer"
        "Make sure to use everything you know to provide the best support possible."
        "You must strive to provide a complete and accurate response to the customer's inquiry."
    ),
    expected_output=(
        "A detailed, informative response to the customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references to everything you used to find the answer, "
        "including external data or solutions. Ensure the answer is complete, "
        "leaving no questions unanswered, and maintaining a helpful and friendly tone throughout."
        "We don't have formal conversations. Make sure it's a casual one."
        #"After you are done always ask customers if there is anything else they need."
    ),
    tools=[docs_scrape_tool],
    #human_input=True,
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for customer inquiry."
        "Ensure that the answer is comprehensive, accurate, and adheres to the high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry have been addressed thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to find the information, ensuring the response is well-supported and leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response ready to be sent to the customer.\n"
        "This response should fully address the customer's inquiry, incorporating all relevant feedback and improvements.\n"
        "Don't be too formal, we are a chill and cool company but maintain a friendly tone throughout."
        "Make sure the response is a livechat type of response not an email response"
    ),
    agent=support_quality_assurance_agent,
)


crew = Crew(
    agents=[support_agent],#, support_quality_assurance_agent],
    tasks=[inquiry_resolution], #, quality_assurance_review],
    verbose=2,
    
)

# Function to kickoff the process
def kickoff_chatbot_crew(user_input):
    # Generate context from chat history
    context = generate_context(st.session_state.chat_history)
    
    # Use the chat history and context in the inputs
    inputs = {'inquiry': user_input, 'context': context}
    result = crew.kickoff(inputs=inputs)
    
    
    # Update chat history
    update_chat_history(user_input, result)
    response = str(result) if result is not None else "Sorry, I couldn't process your request."
    
    return response
    

load_dotenv()

# Streamlit App Interface
st.set_page_config(page_title="Chatbot", page_icon=":speech_balloon:")

st.title("TelQuest International Customer Support Chatbot")
    
for message in st.session_state.chat_history:
    if "bot" in message:
        with st.chat_message("AI"):
            st.markdown(message["bot"])
    elif "user" in message:
        with st.chat_message("Human"):
            st.markdown(message["user"])

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append({"user": user_query})
    
    with st.chat_message("Human"):
        st.markdown(user_query)
        
    with st.chat_message("AI"):
        response = kickoff_chatbot_crew(user_query)
        st.markdown(response)
        
    st.session_state.chat_history.append({"bot": response})
