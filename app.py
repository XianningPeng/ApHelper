import json
import os
from platform import java_ver
import streamlit as st
from data import pieChart, accuracyByUnitChart, overallAccuracy
from main import main
from LLM import analyze
from supabase import create_client, Client

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)




st.title("AP Assistant")
st.subheader("– a tool that can help you ace the exams!", divider= "gray")

# input section
userName = st.text_input("Please put your name in the box")
examType = st.selectbox("***Which exam?***", ["AP Calculus BC", "others"],index = None)
if examType == "others": st.write("not supported yet"), st.stop()    # exams other than calc bc are not supported yet, quit app



options = ["Input more questions", "Check history"]
selection = st.pills("pick one", options, selection_mode="single", label_visibility = "hidden")



if selection == "Input more questions":

    st.divider()

    # the number of questions the user want to input
    numberInput = st.number_input(
        "How many questions do you want to input?",
        min_value = 1,
        max_value = 45,
        value=1,
        placeholder="Type a number..."
    )

    for i in range(numberInput):

        st.divider()
        question_input = st.text_area("please put your question here:", key = f"question_{i}")     # "key" is necessary here.
        correct_input = st.radio("What is the correct answer of this question?",
                              ["A", "B", "C", "D"], index = None, key = f"correctAns_{i}")
        ans_input = st.radio("What is the your answer of this question?",
                              ["A", "B", "C", "D"], index = None, key = f"ans_{i}")


        if (correct_input is not None and ans_input is not None) and st.button("Submit", key = f"{i}button"):     # have to add this "submit" button, otherwise the app would automatically save questions when you click something
            overallAccuracy = main(userName, question_input, correct_input, ans_input)                            # this is because streamlit reruns the entire python code when we make change




if selection == "Check history":

    st.divider()

    try:
        response = supabase.storage.from_("usersdata").download(userName +".json")
    except:
        st.header("You don't have any history. Please input some questions first!")
        st.stop()


    overallAccuracy = overallAccuracy(userName +".json")
    st.header(f"Overall Accuracy:  ***{overallAccuracy}***")

    # accuracy by unit
    st.header(f"Accuracy by Unit")
    data = accuracyByUnitChart(userName + ".json")
    st.bar_chart(data, x="Unit", y="Accuracy", sort=False)

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
        st.dataframe(jsonFile)

    selected = st.feedback("stars")
