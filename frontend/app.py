import streamlit as st
from datetime import date
import uuid


class Task:
    def __init__(self, title, description, priority, status, due_date):
        self.id = str(uuid.uuid4()) # UNIQUE ID
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

    def delete_task(self, task_id):
        self.tasks[:] = [t for t in self.tasks if t.id != task_id]

    def update_status(self, task_id, new_status):
        for t in self.tasks:
            if t.id == task_id:
                t.status = new_status
                return True
        return False

    def update_priority(self, task_id, new_priority):
        for t in self.tasks:
            if t.id == task_id:
                t.priority = new_priority
                return True
        return False

    def get_tasks(self):
        return sorted(self.tasks, key=lambda t: t.priority)

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


# STREAMLIT UI

st.set_page_config(page_title="Smart Task Manager", layout="centered")
st.title("🧠 Smart Task Manager (Recruiter-Grade Python Project)")

manager = TaskManager()

# ---------------- ADD TASK ----------------
st.header("➕ Add Task")

title = st.text_input("Title")
description = st.text_area("Description")
priority = st.number_input("Priority (1 = Highest)", 1, 10, 1)
status = st.selectbox("Status", ["pending", "in-progress", "completed"])
due_date = st.date_input("Due Date")

if st.button("Add Task"):
    if not title.strip():
        st.error("Title is required")
    else:
        manager.add_task(Task(title, description, priority, status, due_date))
        st.success("Task added successfully")
        st.rerun()

# VIEW TASKS
st.header("📋 All Tasks")

tasks = manager.get_tasks()
if tasks:
    for t in tasks:
        st.write(t)
else:
    st.info("No tasks available")

# UPDATE STATUS
st.header("🔄 Update Task Status")

if tasks:
    task_map = {f"{t.title} ({t.status})": t.id for t in tasks}

    selected_task = st.selectbox("Select Task", list(task_map.keys()))
    new_status = st.selectbox("New Status", ["pending", "in-progress", "completed"])

    if st.button("Update Status"):
        manager.update_status(task_map[selected_task], new_status)
        st.success("Status updated")
        st.rerun()
else:
    st.info("No tasks to update")

# UPDATE PRIORITY
st.header("⬆ Update Task Priority")

if tasks:
    selected_task_p = st.selectbox(
        "Select Task for Priority Update",
        options=list(task_map.keys()),
        key="priority_select"
    )
    new_priority = st.number_input("New Priority", 1, 10)

    if st.button("Update Priority"):
        manager.update_priority(task_map[selected_task_p], new_priority)
        st.success("Priority updated")
        st.rerun()
else:
    st.info("No tasks to update")

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

keyword = st.text_input("Enter keyword")

if st.button("Recommend"):
    results = manager.recommend(keyword)
    if results:
        for r in results:
            st.write(r)
    else:
        st.info("No recommendations found")

# DELETE TASK
st.header("🗑 Delete Task")

if tasks:
    selected_task_d = st.selectbox(
        "Select Task to Delete",
        options=list(task_map.keys()),
        key="delete_select"
    )

    if st.button("Delete Task"):
        manager.delete_task(task_map[selected_task_d])
        st.warning("Task deleted")
        st.rerun()
else:
    st.info("No tasks to delete")
