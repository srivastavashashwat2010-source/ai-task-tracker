import streamlit as st
import pandas as pd
from datetime import datetime
from openai import OpenAI

# ---- AI Setup ----
client = OpenAI(api_key="YOUR_API_KEY")

# ---- Load Tasks ----
def load_tasks():
    try:
        return pd.read_csv("tasks.csv")
    except:
        return pd.DataFrame(columns=["Task", "Deadline", "Priority", "Status"])

def save_tasks(df):
    df.to_csv("tasks.csv", index=False)

tasks = load_tasks()

# ---- UI ----
st.set_page_config(page_title="AI Task Tracker", layout="wide")
st.title("📚 AI Student Task Tracker")

# ---- Add Task ----
st.sidebar.header("➕ Add New Task")

task_name = st.sidebar.text_input("Task Name")
deadline = st.sidebar.date_input("Deadline")
priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])

if st.sidebar.button("Add Task"):
    new_task = pd.DataFrame({
        "Task": [task_name],
        "Deadline": [deadline],
        "Priority": [priority],
        "Status": ["Pending"]
    })
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    save_tasks(tasks)
    st.success("Task Added!")

# ---- Display Tasks ----
st.subheader("📋 Your Tasks")
st.dataframe(tasks)

# ---- Mark Complete ----
task_to_complete = st.selectbox("Mark Task as Completed", tasks["Task"])

if st.button("Complete Task"):
    tasks.loc[tasks["Task"] == task_to_complete, "Status"] = "Done"
    save_tasks(tasks)
    st.success("Task Completed!")

# ---- AI Suggestions ----
st.subheader("🤖 AI Study Assistant")

user_input = st.text_area("Ask AI (e.g., break my task into steps)")

if st.button("Get AI Help"):
    if user_input:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful student assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a question!")

# ---- Analytics ----
st.subheader("📊 Progress")

completed = len(tasks[tasks["Status"] == "Done"])
total = len(tasks)

if total > 0:
    st.progress(completed / total)
    st.write(f"Completed: {completed}/{total}")