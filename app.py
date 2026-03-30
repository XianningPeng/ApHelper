import json
import os
from platform import java_ver
import streamlit as st
from data import pieChart, accuracyByUnitChart, overallAccuracy
from main import main
from LLM import analyze
from supabase import create_client, Client
import base64
from qwen import ocr

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)



def getQuestion(uploadedFile):

    encodedImage = base64.b64encode(uploadedFile.read()).decode("utf-8")
    extractedDict = ocr(encodedImage)
    questionInfo["text"] = extractedDict.get("question")
    questionInfo["choiceA"] = extractedDict.get("choiceA")
    questionInfo["choiceB"] = extractedDict.get("choiceB")
    questionInfo["choiceC"] = extractedDict.get("choiceC")
    questionInfo["choiceD"] = extractedDict.get("choiceD")
    questionInfo["choiceE"] = extractedDict.get("choiceE")
    return


def getChoice():

    correct_input = st.radio("What is the correct answer of this question?",
                             ["A", "B", "C", "D", "E"], index=None, key=f"correctAns_{i}")
    ans_input = st.radio("What is the your answer of this question?",
                         ["A", "B", "C", "D", "E"], index=None, key=f"ans_{i}")
    questionInfo["correct_input"] = correct_input
    questionInfo["ans_input"] = ans_input
    return






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


        inputOptions = st.radio(
            "pick a way to upload question",
            ["take a picture", "upload a picture", "input manually"],
            index=None,
            key=f"option{i}"
        )

        questionInfo ={}

        # text": "",
        #     "choiceA": "",
        #     "choiceB": "",
        #     "choiceC": "",
        #     "choiceD": "",
        #     "choiceE": "",
        #     "correct_input": "",
        #     "ans_input": "


        if inputOptions == "take a picture":
            uploadedFile = st.camera_input("Take a picture", disabled=False, key=f"camera{i}")
            try:
                getQuestion(uploadedFile)
                getChoice()
            except:
                st.write("")

        elif inputOptions == "upload a picture":
            uploadedFile = st.file_uploader("upload image of the question", type=["jpg", "jpeg", "png"], key=f"upload{i}")
            try:
                getQuestion(uploadedFile)
                getChoice()
            except:
                st.write("")

        elif inputOptions is not None:
            question_input = st.text_area("please put your question here:", key = f"question_{i}")            # "key" is necessary here.
            choice_a = st.text_input("Choice A", key=f"choice_a_{i}")
            choice_b = st.text_input("Choice B", key=f"choice_b_{i}")
            choice_c = st.text_input("Choice C", key=f"choice_c_{i}")
            choice_d = st.text_input("Choice D", key=f"choice_d_{i}")
            choice_e = st.text_input("Choice E", key=f"choice_e_{i}")

            # store into dict
            questionInfo["text"] = question_input
            questionInfo["choiceA"] = choice_a
            questionInfo["choiceB"] = choice_b
            questionInfo["choiceC"] = choice_c
            questionInfo["choiceD"] = choice_d
            questionInfo["choiceE"] = choice_e

            getChoice()


        if (len(questionInfo) == 8) and st.button("Submit", key = f"{i}button"):     # have to add this "submit" button, otherwise the app would automatically save questions when you click something
            overallAccuracy = main(userName,
                                   questionInfo["text"],
                                   questionInfo["choiceA"],
                                   questionInfo["choiceB"],
                                   questionInfo["choiceC"],
                                   questionInfo["choiceD"],
                                   questionInfo["choiceE"],
                                   questionInfo["correct_input"],
                                   questionInfo["ans_input"])
            st.write("Question classified and logged successfully.")



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


