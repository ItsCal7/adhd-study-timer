import streamlit as st

if 'timerLength' not in st.session_state:
    st.session_state.timerLength = 20
if 'breakNumber' not in st.session_state:
    st.session_state.breakNumber = 3
if 'differentBreaks' not in st.session_state:
    st.session_state.differentBreaks = False
if 'breakLength' not in st.session_state:
    st.session_state.breakLength = st.session_state.timerLength



st.title("Timer Config")

timerLength = st.slider("How long is each cycle?", 1, 60, st.session_state.timerLength)
if timerLength == 1:
    st.write(timerLength, " minute")
else:
    st.write(timerLength, "minutes")


breakNumber = st.number_input("How often do you want to take a break?", value=st.session_state.breakNumber, min_value=0, step=1)
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


if st.button("Continue Configuration"):
    st.session_state.timerLength = timerLength
    st.session_state.breakNumber = breakNumber
    st.session_state.differentBreaks = differentBreaks

    if differentBreaks:
        st.session_state.breakLength = breakLength
    else:
        st.session_state.breakLength = st.session_state.timerLength

    st.switch_page("listConfig.py")
st.caption("All this can be changed later")

