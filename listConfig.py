import streamlit as st
import random


if 'todoList' not in st.session_state:
    st.session_state.dataAvaiable = False
    st.session_state.todoList = []
else:
    st.session_state.dataAvaiable = True

if 'taskNumber' not in st.session_state:
    st.session_state.taskNumber = len(st.session_state.todoList)


st.title("To-do List")
taskList = []

if st.button("Add Task"):
    st.session_state.taskNumber += 1

for i in range(st.session_state.taskNumber):
    if i > len(st.session_state.todoList) - 1:
        st.session_state.dataAvaiable = False
    if st.session_state.dataAvaiable:
        task = st.text_input(f'Task {i+1}', key=f'task_{i}', value=st.session_state.todoList[i])
    else:
        task = st.text_input(f'Task {i+1}', key=f'task_{i}')
    taskList.append(task)

if st.session_state.taskNumber > 0:
    if st.button("Delete Task"):
        st.session_state.taskNumber -= 1
        taskList.pop()
        st.rerun()
        
    if st.button("Start Studying"):
        if '' in taskList:
            st.badge("Please fill out all fields", color="red")
        else:
            st.session_state.todoList = taskList
            st.switch_page("study.py")
    st.caption("All this can be changed later")
    
if st.session_state.debug:
    for taskName in taskList:
        st.title(taskName)
