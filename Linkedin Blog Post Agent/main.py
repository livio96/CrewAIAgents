import requests
import json
from crewai import Agent, Task, Crew
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Custom tool to post to LinkedIn
def post_to_linkedin(content: str) -> str:
    url = "https://api.linkedin.com/v2/ugcPosts"

    payload = json.dumps({
        "author":
        "urn:li:person:kDspkQcU5h",  # Replace with your LinkedIn author URN
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    })

    headers = {
        'X-Restli-Protocol-Version':
        '2.0.0',
        'Content-Type':
        'application/json',
        'Authorization':
        'Bearer ACCESS_TOKEN'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        return "Post successfully created on LinkedIn."
    else:
        return f"Failed to create post: {response.text}"


# Agent that plans the content
planner = Agent(
    role="Content Planner",
    goal="Plan a very short content on {topic}",
    backstory=
    "You're working on planning a blog article about the topic: {topic}. "
    "You collect information that helps the audience learn something "
    "and make informed decisions. Your work is the basis for the Content Writer "
    "to write an article on this topic.",
    allow_delegation=False,
    verbose=True)

# Agent that writes the content and posts it on LinkedIn
writer = Agent(
    role="Content Writer",
    goal=
    "Write a very short insightful and factually accurate opinion piece about the topic: {topic} "
    "and post it to LinkedIn."
    "Make sure that the post doesn't exceed a length of 1000 characters.",
    backstory=
    "You're working on writing a new opinion piece about the topic: {topic}. "
    "Once the piece is ready, you will post it on LinkedIn.",
    allow_delegation=False,
    verbose=True)

# Task for planning content
plan = Task(
    description=
    ("1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
     "2. Identify the target audience, considering their interests and pain points.\n"
     "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
     "4. Include SEO keywords and relevant data or sources."),
    expected_output=
    "A comprehensive content plan document with an outline, audience analysis, "
    "SEO keywords, and resources."
    "Make sure the post is not longer than 1000 characters.",
    agent=planner,
)

# Task for writing the blog post and posting it on LinkedIn
write = Task(
    description=
    ("1. Use the content plan to craft a compelling blog post on {topic}.\n"
     "2. Incorporate SEO keywords naturally.\n"
     "3. Ensure the post is very short structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
     "4. Make sure the post is only 1000 characters long."
     "5. After writing the post, submit it to LinkedIn."),
    expected_output=
    "A very short blog post in markdown format, ready for publication.",
    agent=writer,
)

# Crew that manages the agents and tasks
crew = Crew(agents=[planner, writer], tasks=[plan, write], verbose=True)

# Input topic from the user
topic = input("Give me a topic to work on: ")

# Execute the crew process and kick off the tasks
crew_output = crew.kickoff(inputs={"topic": topic})

# Accessing the final output from the 'Content Writer' agent
writer_task_output = crew_output.tasks_output[
    1]  # Index of writer's task output
blog_post_content = writer_task_output.raw  # Use 'raw' to get the blog post content

# Use the LinkedIn tool to post the content if available
if blog_post_content:
    linkedin_result = post_to_linkedin(blog_post_content)
    print(f"Blog post content:\n{blog_post_content}\n")
    print(f"LinkedIn post result: {linkedin_result}")
else:
    print("Failed to retrieve the blog post content.")
