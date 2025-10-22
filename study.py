import streamlit as st
import random, asyncio, base64

# region Initializing Session Variables
if 'todoList' not in st.session_state:
    st.session_state.todoList = ["Study Greek", "Java Project", "Clean Room"]
if 'activeItem' not in st.session_state:
    st.session_state.activeItem = 1

if 'timerLength' not in st.session_state:
    if st.session_state.debug:
        st.session_state.timerLength = 1
    else:
        st.session_state.timerLength = 20
if 'isTimerRunning' not in st.session_state:
    st.session_state.isTimerRunning = False

if 'breakNumber' not in st.session_state:
    st.session_state.breakNumber = 3
if "isBreak" not in st.session_state:
    st.session_state.isBreak = False
if "breakCounter" not in st.session_state:
    st.session_state.breakCounter = 1
if 'differentBreaks' not in st.session_state:
    st.session_state.differentBreaks = False
if 'breakLength' not in st.session_state:
    st.session_state.breakLength = st.session_state.timerLength

if "playCelebration" not in st.session_state:
    st.session_state.playCelebration = False
# endregion

# region Functions
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

        st.session_state.breakCounter += 1
        if st.session_state.breakCounter > st.session_state.breakNumber:
            st.session_state.breakCounter = 1

        if (st.session_state.breakCounter % st.session_state.breakNumber) == 0:
            st.session_state.isBreak = True
        else:
            st.session_state.isBreak = False

            st.session_state.activeItem += 1
            if st.session_state.activeItem > len(st.session_state.todoList):
                st.session_state.activeItem = 1
       
        st.session_state.playCelebration = True
        st.rerun()
# endregion

footer="""<style>
a:link , a:visited{
color: red;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: pink;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Got a suggestion? Found a Bug? <a style='display: block; text-align: center;' href="https://callumclark.hipporello.net/desk/form/8a9e8f60dc444875910c185284dac834" target="_blank">Tell Me</a></p>
</div>
"""

st.title("Study Time")

if st.session_state.playCelebration: #Play Celebration Music
    with st.empty():
        play_audio("heart_container.mp3")
    st.session_state.playCelebration = False

col1, col2 = st.columns(2, gap="small", vertical_alignment="center", border=True)

with st.sidebar: #Timer Config
    st.caption("Making Any Changes Will Restart the Timer")
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
    
    differentBreaks = st.checkbox("I want breaks to be a different length than normal cycles", value=st.session_state.differentBreaks)
    if differentBreaks:
        breakLength = st.slider("How long is each break?", 1, 60, st.session_state.breakLength)
        if breakLength == 1:
            st.write(breakLength, " minute")
        else:
            st.write(breakLength, "minutes")

    
    if st.button("Save Changes"):
        st.session_state.timerLength = timerLength
        st.session_state.breakNumber = breakNumber
        st.session_state.differentBreaks = differentBreaks

        if differentBreaks:
            st.session_state.breakLength = breakLength
        else:
            st.session_state.breakLength = st.session_state.timerLength

with st.empty(): #Timer and TodoList Display
    with col1:
        if st.button("Start Session"): # Timer Trigger
            st.session_state.isTimerRunning = True

        with col2: #List
            st.badge("Cycle Number: " + str(st.session_state.activeItem), color="blue")
            if st.session_state.isBreak:
                st.header("Break Time")
            else:
                if st.button("Randomize To-Do List Order"):
                    random.shuffle(st.session_state.todoList)
                    st.rerun()
                if st.session_state.isTimerRunning:
                    st.caption("Randomizing will restart the timer")
                st.divider()

                i = 0
                for item in st.session_state.todoList:
                    i += 1
                    if i==st.session_state.activeItem:
                        st.badge("Active", icon=":material/progress_activity:", color="green")
                    st.header(item, divider=True)
                    
                if st.button("Configure To-Do List"):
                    st.switch_page("listConfig.py")

        if st.session_state.isTimerRunning: #Timer Display
            if st.session_state.isBreak:
                asyncio.run(count_down(st.session_state.breakLength * 60))
            else:
                asyncio.run(count_down(st.session_state.timerLength * 60))
st.markdown(footer,unsafe_allow_html=True)