import streamlit as st



st.title("📘 AP Helper")
st.subheader("Your personal AP practice assistant")

st.markdown(
    """
    Welcome to **AP Helper** — a tool designed to help you practice smarter, 
    track your mistakes, and understand your progress by topic.

    Whether you are doing multiple-choice questions, reviewing old mistakes, 
    or checking your weak units, AP Helper helps you stay organized and improve efficiently.
    """
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("### What you can do")
    st.markdown(
        """
        - Upload or type in AP questions  
        - Record your answers  
        - Check whether you got them correct  
        - Track performance by unit  
        - Review your question history  
        - See which topics need more practice  
        """
    )

with col2:
    st.markdown("### Why use AP Helper?")
    st.markdown(
        """
        AP practice is not just about doing more questions.  
        It is about knowing:

        - **what you keep getting wrong**
        - **which units are weak**
        - **whether you are improving over time**

        AP Helper turns your practice into clear feedback.
        """
    )

st.divider()

st.markdown("### Get started")

col3, col4 = st.columns(2)

with col3:
    if st.button("🚀 Start Practicing", use_container_width=True):
        st.switch_page("input.py")

with col4:
    if st.button("📊 View History", use_container_width=True):
        st.switch_page("history.py")

st.divider()

st.caption("Built to make AP practice more structured, focused, and effective.")