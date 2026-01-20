import streamlit as st
from datetime import date

# ------------------ MODELS ------------------

class Task:
    def __init__(self, title, description, priority, status, due_date):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date

    def __str__(self):
        return f"[{self.status.upper()} | P{self.priority}] {self.title} (Due: {self.due_date})"


class TaskManager:
    def __init__(self):
        if "tasks" not in st.session_state:
            st.session_state.tasks = []

    @property
    def tasks(self):
        return st.session_state.tasks

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, title):
        self.tasks[:] = [t for t in self.tasks if t.title != title]

    def update_status(self, title, status):
        for t in self.tasks:
            if t.title == title:
                t.status = status

    def get_tasks(self):
        return sorted(self.tasks, key=lambda x: x.priority)

    def overdue_tasks(self):
        today = date.today()
        return [t for t in self.tasks if t.due_date < today and t.status != "completed"]

    def recommend(self, keyword):
        keyword_words = set(keyword.lower().split())
        results = []
        for t in self.tasks:
            desc_words = set(t.description.lower().split())
            similarity = len(keyword_words & desc_words) / max(len(keyword_words), 1)
            if similarity >= 0.3:
                results.append(t)
        return results


# ------------------ UI ------------------

st.set_page_config(page_title="Smart Task Manager", layout="centered")
st.title("🧠 Smart Task Manager (Python Project)")

manager = TaskManager()

# ADD TASK
st.header("➕ Add Task")
title = st.text_input("Title")
description = st.text_area("Description")
priority = st.number_input("Priority (1 = High)", 1, 10, 1)
status = st.selectbox("Status", ["pending", "in-progress", "completed"])
due_date = st.date_input("Due Date")

if st.button("Add Task"):
    if title:
        manager.add_task(Task(title, description, priority, status, due_date))
        st.success("Task added successfully")
    else:
        st.error("Title is required")

# VIEW TASKS
st.header("📋 All Tasks")
for task in manager.get_tasks():
    st.write(task)

# UPDATE STATUS
st.header("🔄 Update Status")
u_title = st.text_input("Task Title to Update")
u_status = st.selectbox("New Status", ["pending", "in-progress", "completed"])

if st.button("Update"):
    manager.update_status(u_title, u_status)
    st.success("Status updated")

# OVERDUE TASKS
st.header("⏰ Overdue Tasks")
overdue = manager.overdue_tasks()
if overdue:
    for t in overdue:
        st.warning(t)
else:
    st.info("No overdue tasks")

# RECOMMENDATIONS
st.header("✨ Task Recommendations")
keyword = st.text_input("Keyword")

if st.button("Recommend"):
    results = manager.recommend(keyword)
    if results:
        for r in results:
            st.write(r)
    else:
        st.info("No recommendations found")

# DELETE TASK
st.header("🗑 Delete Task")
d_title = st.text_input("Task Title to Delete")

if st.button("Delete"):
    manager.delete_task(d_title)
    st.warning("Task deleted")
