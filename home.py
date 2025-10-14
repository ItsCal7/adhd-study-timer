import streamlit as st

st.title("ADHD Study Timer")
st.write("I have 81-HDs (That's one more than most adhd people)")
st.write("I've recently developed a study technique:")
st.markdown("- 20 minutes studying one thing")
st.markdown("- 20 minutes studying another thing")
st.markdown("- 20 minutes of break")
st.markdown("- Continue the cycle")
st.write("This works with homework, cleaning, coding, and basically any other chore or task I have to do.")
st.write("So I thought I'd make a lil customizable timer app")
if st.button("Click here to get started"):
    st.switch_page("timerConfig.py")