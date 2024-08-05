from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, \
 ScrapeWebsiteTool, \
 WebsiteSearchTool

# Load environment variables from .env file
load_dotenv()

support_agent = Agent(
    role="Senior Support Representative",
  goal="Be the most friendly and helpful "
        "support representative in your team",
  backstory=(
    "You work at TelQuest International (https://www.telquestintl.com) and "
        " are now working on providing "
    "support to all telquest international customers."
    "You need to make sure that you provide the best support!"
    "Make sure to provide full complete answers, "
        " and make no assumptions."
  ),
  allow_delegation=False,
  verbose=True
)

support_quality_assurance_agent = Agent(
  role="Support Quality Assurance Specialist",
  goal="Get recognition for providing the "
    "best support quality assurance in your team",
  backstory=(
    "You work at TelQuest International (https://telquestintl.com) and "
        "are now working with your team "
    "on a request from telquest customers ensuring that "
        "the support representative is "
    "providing the best support possible.\n"
    "You need to make sure that the support representative "
        "is providing full"
    "complete answers, and make no assumptions."
  ),
  verbose=True
)

docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://www.telquestintl.com/search"
)

inquiry_resolution = Task(
    description=(
        "A customer just reached out with a super important ask:\n"
      "{inquiry}\n\n"
    "Make sure to use everything you know "
        "to provide the best support possible."
    "You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
      "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
    "leaving no questions unanswered, and maintain a helpful and friendly "
    "tone throughout. We don't formal conversation. Make sure its a casual one."
    ),
  tools=[docs_scrape_tool],
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for customers inquiry."
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
    "high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
    "thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
    "ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
    "relevant feedback and improvements.\n"
    "Don't be too formal, we are a chill and cool company "
      "but maintain a friendly tone throughout."
      "Make sure the response is a livechat type of response not an email response"
    ),
    agent=support_quality_assurance_agent,
)

crew = Crew(
  agents=[support_agent, support_quality_assurance_agent],
  tasks=[inquiry_resolution, quality_assurance_review],
  verbose=2,
  memory=True
)

inquiry = input("How can i help you today?")

inputs = {
    "inquiry": inquiry
   
}

result = crew.kickoff(inputs=inputs)

print(result)
