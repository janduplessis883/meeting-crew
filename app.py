import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set your API key
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

st.title("Meeting Summarization Crew")
st.logo("crewai.png", size="large")

with st.sidebar:
    st.header("Editor Model")
    editor_model = st.selectbox(
        "Select the model for the editor agent:",
        ("deepseek/deepseek-r1-0528-qwen3-8b", "moonshotai/kimi-k2:free", "google/gemini-2.5-flash-lite")
    )

llm = LLM(
    model=f"openrouter/{editor_model}",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENROUTER_API_KEY')
)

# Date and attendees
meeting_date = st.date_input("Meeting Date")
attendees = st.multiselect(
    "Attendees",
    ["Jan", "Jenny", "Shuman", "Andrew", "Rhiannon", "Ardit", "Sally", "Helen", "Hanisha", "Jen", "Sinead"]
)

# Text area for the meeting transcript
transcript = st.text_area("Paste the meeting transcript here:", height=300)

if st.button("Run Crew"):
    if transcript:
        with st.spinner("The crew is working...", show_time=True):
            # Define the Meeting Minute Writer agent
            minute_writer = Agent(
                role='Senior Medical Meeting Minute Writer',
                goal='Create a concise and accurate summary of the meeting, capturing key decisions and action items.',
                backstory='You are an expert in summarizing long and complex discussions into clear and actionable meeting minutes. You have a keen eye for detail and a talent for identifying the most critical information. Summarize the meeting minutes under headings with buttel points and Descisions made followed by an action log, this is a GP Surgery meeting.',
                verbose=True,
                allow_delegation=False,
            )

            # Define the Editor agent
            editor = Agent(
                role='Senior Medical Editor',
                goal='Review and refine the meeting minutes to ensure they are clear, concise, and free of errors, and suited for a medical practice audience.',
                backstory='You are a meticulous editor with a passion for clarity and precision. You review documents to ensure they are well-written, easy to understand, and meet the highest standards of quality.',
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            # Define the writing task
            writing_task = Task(
                description=f'Write a detailed summary of the following meeting transcript that took place on {meeting_date} with the following attendees: {", ".join(attendees)}:\n\n{transcript}',
                expected_output='A well-structured summary of the meeting, including the date and attendees, key discussion points, decisions, and a list of action items with assigned owners and deadlines.',
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

            st.subheader("Final Meeting Minutes:")
            with st.container():
                st.markdown(result)
    else:
        st.warning("Please paste the meeting transcript before running the crew.")
