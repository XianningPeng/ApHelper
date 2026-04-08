import streamlit as st
from supabase import create_client, Client
from data import pieChart, accuracyByUnitChart, overallAccuracy, count,accuracyByTime
from LLM import analyze
import json
import os

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


userName = st.session_state.userName


try:
    response = supabase.storage.from_("usersdata").download(userName + ".json")
except:
    st.header("You don't have any history. Please input some questions first!")
    st.stop()

overallAccuracy = overallAccuracy(userName + ".json")
st.header(f"Overall Accuracy:  ***{overallAccuracy}***")
st.markdown("Use this page to quickly understand your performance trends, your strongest units, and the areas that need more review.")


st.divider()
st.markdown("### Unit-level breakdown")
st.markdown("These two diagrams show **where your questions are coming from** and **how accurately you are answering them** across AP Calc BC units.")



col1, col2 = st.columns(2)

# accuracy by unit
with col1:
    st.header(f"Accuracy by Unit")
    st.markdown("This chart highlights **how well you perform in each unit**. Lower bars usually point to topics that need more targeted practice.")
    data = accuracyByUnitChart(userName + ".json")
    st.bar_chart(data, x="Unit", y="Accuracy", sort=False)

# total number of finished questions by unit
with col2:
    st.header(f"Number of Questions in each unit")
    st.markdown("This chart shows **how often each unit appears in your history**. It helps you tell the difference between a true weak spot and a unit with too little practice data.")
    df = pieChart(userName + ".json")
    st.bar_chart(df, x="Unit", y="Frequency", x_label="Frequency(how many times they showed up in your questions)",
                 sort=False, horizontal=True)

st.divider()
st.markdown("### Practice volume over time")
st.markdown("This section focuses on **consistency**. It shows how many questions you completed over time, which makes it easier to see whether your practice routine is stable.")
# number of questions finished by week
count(userName+".json")

st.divider()
st.markdown("### Accuracy trend over time")
st.markdown("This diagram shows **whether your accuracy is improving, dropping, or staying flat** as time goes on.")
accuracyByTime()

st.divider()


if 'aiOverview' in st.session_state:
    st.markdown("### AI Overview")
    st.markdown("This summary gives you a quick natural-language interpretation of your history and patterns.")
    st.write(st.session_state.aiOverview)

if st.button("**Check  out an** $AI Overview$"):
    with st.spinner("Wait for it...  It might take a while", show_time=True):
        content = analyze(userName)
    st.session_state['aiOverview'] = content
    st.divider()
    st.markdown("### AI Overview")
    st.markdown("This summary gives you a quick natural-language interpretation of your history and patterns.")
    st.write(st.session_state.aiOverview)
    st.divider()


# check and download history
st.markdown("### Full history")
st.markdown("Open this section to review every saved question and download your raw practice record.")
on = st.toggle("See full history and download it")
fileName = userName + ".json"

if on:
    responseLocal = supabase.storage.from_("usersdata").download(fileName)  # get the file
    jsonFile = json.loads(responseLocal)

    st.download_button("Download the file", responseLocal, f"{userName}.json")

    #display user's history question in
    for i in range(len(jsonFile)):
        st.divider()

        st.markdown(f"### {jsonFile[i]['text']}")
        for key, value in jsonFile[i].items():
            if key != "text":
                st.write(f"{key}: {value}")