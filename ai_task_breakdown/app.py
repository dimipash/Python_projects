import os
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI
import streamlit as st

load_dotenv(find_dotenv())
client = OpenAI()


def generate_milestones(task_description):
    prompt = f"""
        Break down the following tasks into smaller milestones.
        \n\nTask:
        {task_description}
        \n\n Milestones:
        """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a efficient, task-driven and successful bussinessman",
                },
                {"role": "user", "content": f"{prompt}"},
            ],
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred while generating: {e}"


def app_console():
    print("Task Breakdown Generator")
    task_description = input("Enter the task you want to breakdown into steps: ")
    if task_description:
        print("\nGenerating milestones...")
        milestones = generate_milestones(task_description)
        if milestones:
            print("\nMilestones:")
            print(milestones)
        else:
            print("An error occurred while generating milestones.")
    else:
        print("Please enter a task description.")


def streamlit_app():
    st.title("Task Breakdown App")
    task_description = st.text_input("Enter the task you want to breakdown into steps")
    if st.button("Generate Milestones"):
        if task_description:
            milestones = generate_milestones(task_description)
            st.markdown("### Milestones")
            st.write(milestones)
        else:
            st.write("Please enter a task description")


def main():
    streamlit_app()
    app_console()


if __name__ == "__main__":
    main()
