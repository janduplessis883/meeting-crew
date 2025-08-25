import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set your API key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

# Define the meeting content
meeting_transcript = """
**Meeting Transcript: Project Alpha Kick-off**

**Date:** August 25, 2025
**Attendees:** John (Project Manager), Sarah (Lead Developer), David (UX Designer)

**John:** Alright everyone, thanks for joining. The goal of this meeting is to officially kick off Project Alpha. As you know, this project is crucial for our Q4 goals. We need to be aligned on the scope, timeline, and our individual responsibilities.

**Sarah:** John, I've reviewed the initial requirements, and I have some concerns about the timeline. The two-month deadline seems very aggressive, especially with the new features we've discussed. I think we need to either scale back the scope or extend the deadline.

**David:** I agree with Sarah. From a UX perspective, creating a seamless user experience for all the proposed features will require significant time for user research, wireframing, and prototyping. Rushing this phase could lead to a product that doesn't meet user expectations.

**John:** I understand your concerns. The deadline is tight, but it's driven by market demands. What if we prioritize the core features for the initial launch and plan for a phased rollout of the secondary features? That way, we can still meet the deadline with a solid MVP.

**Sarah:** That sounds like a reasonable compromise. If we focus on the core functionalities, I'm confident we can deliver a high-quality product within the two-month timeframe. We'll need to clearly define what constitutes "core" versus "secondary."

**David:** I'm on board with that approach as well. It will allow me to focus on perfecting the user experience for the essential features. I'll start working on the user flow for the core features right away.

**John:** Excellent. I'll update the project plan to reflect this phased approach. Sarah, can you provide me with a list of the features you consider to be core by the end of the day? David, can you have the initial wireframes for the core user flow ready for review by the end of the week?

**Sarah:** Yes, I can get you that list.

**David:** I'll have the wireframes ready.

**John:** Great. Let's touch base again in a week to review our progress. Thanks, everyone.
"""

# Define the Meeting Minute Writer agent
minute_writer = Agent(
    role='Meeting Minute Writer',
    goal='Create a concise and accurate summary of the meeting, capturing key decisions and action items.',
    backstory='You are an expert in summarizing long and complex discussions into clear and actionable meeting minutes. You have a keen eye for detail and a talent for identifying the most critical information.',
    verbose=True,
    allow_delegation=False
)

# Define the Editor agent
editor = Agent(
    role='Editor',
    goal='Review and refine the meeting minutes to ensure they are clear, concise, and free of errors.',
    backstory='You are a meticulous editor with a passion for clarity and precision. You review documents to ensure they are well-written, easy to understand, and meet the highest standards of quality.',
    verbose=True,
    allow_delegation=False
)

# Define the writing task
writing_task = Task(
    description=f'Write a detailed summary of the following meeting transcript:\n\n{meeting_transcript}',
    expected_output='A well-structured summary of the meeting, including key discussion points, decisions, and a list of action items with assigned owners and deadlines.',
    agent=minute_writer
)

# Define the editing task
editing_task = Task(
    description='Review the meeting minutes for clarity, accuracy, and conciseness. Make any necessary edits to improve the overall quality of the document.',
    expected_output='A polished and professional set of meeting minutes that is ready for distribution.',
    agent=editor
)

# Create the crew
meeting_crew = Crew(
    agents=[minute_writer, editor],
    tasks=[writing_task, editing_task],
    process=Process.sequential,
    verbose=True
)

# Start the crew's work
result = meeting_crew.kickoff()

# Print the final result
print("######################")
print("Final Meeting Minutes:")
print(result)
