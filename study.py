import streamlit as st
import random, asyncio, base64

if 'todoList' not in st.session_state:
    st.session_state.todoList = {"Study Greek": "", "Java Project": "", "Clean Room": ""}
if 'activeItem' not in st.session_state:
    st.session_state.activeItem = 1

if 'timerLength' not in st.session_state:
    st.session_state.timerLength = 1
if 'isTimerRunning' not in st.session_state:
    st.session_state.isTimerRunning = False

if 'breakNumber' not in st.session_state:
    st.session_state.breakNumber = 3
if "isBreak" not in st.session_state:
    st.session_state.isBreak = False
if "breakCounter" not in st.session_state:
    st.session_state.breakCounter = 1
if "activeTaskCounter" not in st.session_state:
    st.session_state.activeTaskCounter = 1

def play_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" style="display: none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

async def count_down(ts):
    with st.empty():
        while ts:
            mins, secs = divmod(ts, 60)
            time_now = '{:02d}:{:02d}'.format(mins, secs)
            st.title(f"{time_now}")
            r = await asyncio.sleep(1)
            ts -= 1
        time_now = '{:02d}:{:02d}'.format(0, 0)
        st.title(f"{time_now}")
        st.session_state.isTimerRunning = False
        with st.empty():
            play_audio("heart_container.mp3")

st.title("Study Time")
col1, col2 = st.columns(2, gap="small", vertical_alignment="center", border=True)


with col1:
    if st.button("Start Session"):
        st.session_state.isTimerRunning = True
        st.session_state.breakCounter += 1
        if st.session_state.breakCounter > st.session_state.breakNumber:
            st.session_state.breakCounter = 1


        if (st.session_state.breakCounter % st.session_state.breakNumber) == 0:
            st.session_state.isBreak = True
        else:
            st.session_state.isBreak = False

            st.session_state.activeTaskCounter += 1
            if st.session_state.activeTaskCounter > len(st.session_state.todoList):
                st.session_state.activeTaskCounter = 1

        asyncio.run(count_down(st.session_state.timerLength * 60))
        

with col2:
    if st.session_state.isBreak:
        st.header("Break Time")
    else:
        i = 0
        for item in st.session_state.todoList:
            i += 1
            if i==st.session_state.activeTaskCounter:
                st.badge("Active", icon=":material/progress_activity:", color="green")
            st.header(item, divider=True)
        if st.button("Randomize To-Do List Order"):
            items = list(st.session_state.todoList.items())
            random.shuffle(items)
            st.session_state.todoList = dict(items)
            st.rerun()
        if st.button("Configure To-Do List"):
            st.switch_page("listConfig.py")

with st.sidebar:
    st.caption("Making Any Changes Will Cancel Current Session")
    timerLength = st.slider("Cycle Length", 1, 60, st.session_state.timerLength)
    if timerLength == 1:
        st.write(timerLength, " minute")
    else:
        st.write(timerLength, "minutes")


    breakNumber = st.number_input("Break Frequency", value=st.session_state.breakNumber, min_value=0, step=1)
    if breakNumber == 0:
        st.write("No breaks")
    elif breakNumber == 1:
        st.write("Every cycle")
    else:
        st.write("Every ", breakNumber, " cycles")
    
    if st.button("Save Changes"):
        st.session_state.timerLength = timerLength
        st.session_state.breakNumber = breakNumber