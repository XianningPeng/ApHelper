import streamlit as st
from supabase import create_client, Client
from data import pieChart, accuracyByUnitChart, overallAccuracy
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



col1, col2 = st.columns(2)

with col1:
    # accuracy by unit
    st.header(f"Accuracy by Unit")
    data = accuracyByUnitChart(userName + ".json")
    st.bar_chart(data, x="Unit", y="Accuracy", sort=False)

with col2:
# total number of finished questions by unit
    st.header(f"Number of Questions in each unit")
    df = pieChart(userName + ".json")
    st.bar_chart(df, x="Unit", y="Frequency", x_label="Frequency(how many times they showed up in your questions)",
                 sort=False, horizontal=True)

if 'aiOverview' in st.session_state:
    st.write(st.session_state.aiOverview)

if st.button("**Check  out an** $AI Overview$"):
    with st.spinner("Wait for it...  It might take a while", show_time=True):
        content = analyze(userName)
    st.session_state['aiOverview'] = content
    st.divider()
    st.write(st.session_state.aiOverview)
    st.divider()

# check and download history
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